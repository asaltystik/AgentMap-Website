from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import FileResponse
from .forms import LoginForm, UserRegistrationForm
from .models import Form, LicensedState
import os

StateDict = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut",
    "DC": "District of Columbia", "DE": "Delaware", "FL": "Florida",
    "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
    "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
    "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming",
}


# This function will render the register.html page
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# this function will render the login.html page
def login_view(request):
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
                return redirect('AgentMap')
    else:
        # if the request is not a POST request, create a new login form
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# This function will log the user out and redirect them to the login page
def logout_view(request):
    logout(request)
    return redirect('Login')


# This function will render the map.html page
@login_required
def agent_map(request):
    # Get all the states that the agent is licensed in
    licensed_states = LicensedState.objects.filter(agent__user=request.user)
    return render(request, 'map.html', {'licensed_states': licensed_states})


@login_required
# This function will get all the companies in the given state
def get_companies(request, state_code):
    # Get all the forms in the given state
    forms = Form.objects.filter(state=state_code).order_by('company')

    # Get the un-abbreviated state name using the state code and the StateDict
    state = StateDict[state_code]

    # Get the current date
    current_date = timezone.now().date()

    try:
        licenses = LicensedState.objects.filter(agent__user=request.user)
        license_number = licenses.get(state=state_code).licenseNumber
        expiration = licenses.get(state=state_code).expiration

        # Check if the expiration date is in the same month and year as the
        # current date
        is_expiring_soon = (expiration.year == current_date.year and
                            expiration.month == current_date.month) \
            if expiration else False
        return render(request, "companies.html", {"state": state, "forms": forms,
                                                  "license_number": license_number, "expiration": expiration,
                                                  "is_expiring_soon": is_expiring_soon})
    except LicensedState.DoesNotExist:
        return render(request, "companies.html", {"state": state, "forms": forms})


# This function handles opening the pdf file server side and sending it to the client
@xframe_options_exempt
def view_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    file_path = form.file_path
    # if os is windows, replace the backslashes with forward slashes
    if os.name == 'nt':
        file_path = file_path.replace('\\', '/')
    file_path = "static/Companies/" + file_path
    if not file_path.startswith('static/'):
        raise SuspiciousOperation('Attempted directory traversal')

    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response
