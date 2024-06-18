from collections import defaultdict

from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import FileResponse, HttpResponse, JsonResponse
from django.core import serializers
from .forms import LoginForm, UserRegistrationForm
from .models import Form, LicensedState, State, HouseHoldDiscountKey, HouseHoldDiscount, AcceptanceRule
from datetime import timedelta
import os


# This function will render the register.html page
def register_view(request):

    # if the request is a POST request, check if the form is valid
    if request.method == 'POST':

        # create a new user registration form with the POST data
        form = UserRegistrationForm(request.POST)

        # if the form is valid, save the form and redirect the user to the login page
        if form.is_valid():
            form.save()
            return redirect('Login')
    # if the request is not a POST request, create a new user registration form
    else:
        form = UserRegistrationForm()  # Serve them the registration form
    return render(request, 'register.html', {'form': form})  # render the register.html page with the form


# this function will render the login.html page
def login_view(request):

    # If the user is already logged in, redirect them to the agent map page
    if request.user.is_authenticated:
        return redirect('AgentMap')

    # if the request is a POST request, check if the form is valid
    if request.method == 'POST':
        # create a new login form with the POST data
        form = LoginForm(request.POST)
        # if the form is valid, authenticate the user and log them in
        if form.is_valid():
            # authenticate the user
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # if the user is not None, log them in
            if user is not None:
                login(request, user)
                return redirect('AgentMap')  # redirect the user to the agent map page
    else:
        # if the request is not a POST request, create a new login form
        form = LoginForm()
    # render the login.html page with the form
    return render(request, 'login.html', {'form': form})


# This function will log the user out and redirect them to the login page
def logout_view(request):
    logout(request)  # log the user out
    return redirect('Login')  # redirect the user to the login page


# This function will render the map.html page
@login_required
def agent_map(request):

    agents_in_states = {}
    # Get all the states that the agent is licensed in
    licensed_states = LicensedState.objects.filter(agent__user=request.user)
    print(f'Licensed states: {licensed_states}')  # Debugging line

    # Get all the discounts + keys
    discount_keys = HouseHoldDiscountKey.objects.all()

    # Check if the logged-in user is 'admin'
    if request.user.username == 'admin':
        print('Admin is logged in')
        # Get all the states
        licenses = LicensedState.objects.all().select_related('agent', 'state')  # Include 'state' in select_related

        agents_in_states = {}
        for license in licenses:
            state_code = license.state.state_code  # Assuming 'name' is the field that holds the state code
            if state_code not in agents_in_states:
                agents_in_states[state_code] = []
            if license.agent.user.username != 'admin' and license.agent not in agents_in_states[state_code]:
                agent_name = license.agent.user.username[0].upper() + license.agent.user.username[1:]
                agents_in_states[state_code].append(agent_name)
            # Sort agents_in_states by alphabetical order
            agents_in_states[state_code].sort()
        # print(f'Agents in states: {agents_in_states}')  # Debugging line

    context = {
        'licensed_states': licensed_states,
        'agents_in_states': agents_in_states,
        'discount_keys': discount_keys,
    }

    return render(request, 'map.html', context=context)


@login_required
# This function will get all the companies in the given state
def get_companies(request, state_code):
    # Birthday rule states
    birthday_rule_states = [
        "California", "Idaho", "Kentucky", "Maryland", "Missouri",
        "Nevada", "Oklahoma", "Oregon", "Washington"
    ]

    # Dictionary to convert state abbreviations to full state names
    state_dictionary = {
        state_obj.state_code: state_obj.full_state for state_obj in State.objects.all()
    }

    # Get all the forms in the given state
    forms = Form.objects.filter(state__state_code=state_code).order_by('carrier')

    # Get the un-abbreviated state name using the state code and the StateDict
    state = state_dictionary[state_code]

    discounts = HouseHoldDiscount.objects.filter(state__state_code=state_code).order_by('carrier')
    # Get the current date
    current_date = timezone.now().date()

    # Try to get the license number and expiration date for the given state
    try:
        # Get all the licenses for the agent
        licenses = LicensedState.objects.filter(agent__user=request.user)
        # Get the state license for the given state and the farthest
        # expiration date for the given state
        state_license = licenses.filter(state__state_code=state_code).order_by('expiration').last()
        if state_license is not None:
            license_number = state_license.licenseNumber
            expiration = state_license.expiration
            # Check if the expiration date is upcoming in the next 31 days
            is_expiring_soon = (expiration - current_date <= timedelta(days=31))\
                if expiration else False
            # Im sure future me won't have to deal with this... Sorry, Not sorry.
            days_until_expiration = (expiration - current_date).days \
                if expiration else 9999  # Set to huge number since NaN is not valid
        else:
            # If the agent is not licensed in the given state, Take the admin license and expiration date
            admin_license = LicensedState.objects.filter(agent__user__username='admin', state__state_code=state_code).first()
            license_number = "Corp# " + admin_license.licenseNumber if admin_license else None
            expiration = None
            is_expiring_soon = False
            days_until_expiration = 9999 # Huge number since NaN is not valid


        # Context
        context = {
            "state": state,  # packing the state name into context
            "forms": forms,  # packing the forms into context
            "discounts": discounts,  # packing the discounts into context
            "license_number": license_number,  # packing the license number into context
            "expiration": expiration,  # packing the expiration date into context
            "is_expiring_soon": is_expiring_soon,  # packing the is_expiring_soon boolean into context
            "days_until_expiration": days_until_expiration,  # packing the days until expiration into context
            "birthday_rule_states": birthday_rule_states,  # packing the birthday_rule_states into context
        }

        # Render the companies.html page with the given state, forms, license number, expiration date,
        # and is_expiring_soon
        return render(request, "companies.html", context)
    # If the agent is not licensed in the given state, render the companies.html page with the given state and forms
    except LicensedState.DoesNotExist:

        # Get the user named admin license number and expiration date for this state
        admin_license = LicensedState.objects.filter(agent__user__username='admin', state=state_code).first()

        # Context
        context = {
            "state": state,  # packing the state name into context
            "forms": forms,  # packing the forms into context
            "discounts": discounts,  # packing the discounts into context
            "license_number": admin_license.licenseNumber if admin_license else None,
            "expiration": admin_license.expiration if admin_license else None,
            "days_until_expiration": 9999,  # Setting this to huge number since nan is not supported
            "birthday_rule_states": birthday_rule_states,  # packing the birthday_rule_states into context
        }
        print(context)

        # Render the companies.html page with the given state and forms
        return render(request, "companies.html", context)


# This function handles opening the pdf file server side and sending it to the client
@xframe_options_exempt
@login_required
def view_form(request, form_id):

    # Get the form with the given id
    form = get_object_or_404(Form, id=form_id)

    # Get the file path of the form
    file_path = form.file_path

    # if os is windows, replace the backslashes with forward slashes
    if os.name == 'nt':
        # in the future this will be replaced. Windows is not what this server is going to be running on in production
        file_path = file_path.replace('\\', '/')  # Fuck windows \\ should just be /

    # Get the file_path
    # if filepath doesnt contain static/Companies/
    if not file_path.startswith("static/Companies"):
        # file_path does not start with static/Companies
        index = file_path.index("static/Companies")  # Remove the ../.. from the rel path
        file_path = file_path[index:]
    elif "static/Companies" not in file_path:
        file_path = "static/Companies" + file_path  # Simple append to the beginning of the string
    else:
        file_path = file_path  # File_path should be ok as is

    # if the file path does not start with 'static/', raise a SuspiciousOperation
    if not file_path.startswith('static/'):
        raise SuspiciousOperation('Attempted directory traversal')  # Raise a suspicious operation

    # Open the file and send it to the client
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response

# This function handles opening the txt file server side and sending it to the client@xframe_options_exempt
@xframe_options_exempt
@login_required
def birthday_rules(request, state):
    # Define the path to the text file
    file_path = f'static/birthday_rules/{state}.txt'

    # Open the file and read its content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Wrap the file content in HTML tags and apply CSS styling
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        body {{
            background-color: #ffffff;
            color: #000000;
            font-family: Arial, sans-serif;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            height: 100vh;
        }}
        p {{
            white-space: pre-wrap;       /* css-3 */
            white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
            white-space: -pre-wrap;      /* Opera 4-6 */
            white-space: -o-pre-wrap;    /* Opera 7 */
            word-wrap: break-word;       /* Internet Explorer 5.5+ */
            text-align: justify;
        }}
        </style>
    </head>
    <body>
        <p>{file_content}</p>
    </body>
    </html>
    """

    # Create a response with the HTML content
    response = HttpResponse(html_content, content_type='text/html')

    return response


# This view will return a interactive map of the US with the clients coordinates are marked on the map
@login_required
def client_map(request):
    return render(request, 'client_combined_map.html')

# This view will send the user to the Declinable Drug List Page
@login_required
def declinable_drug_list(request):
    # We will need to pack the data into a context dictionary to pass to the render
    acceptanceRules = AcceptanceRule.objects.all()
    context = {
        'acceptanceRules': acceptanceRules
    }
    return render(request, 'declinable_drug_list.html', context=context)

