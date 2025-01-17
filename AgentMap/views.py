import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import SuspiciousOperation
from django.http import FileResponse, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta, datetime
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_GET
from .models import Agent, HouseHoldDiscountKey, HouseHoldDiscount, State, PDF, Drug, AcceptanceRule, AgentActivity, Carrier, FormType
from .forms import LoginForm
from django.middleware.csrf import get_token
import json
import os


# This view is the login view for the AgentMap project.
def login_view(request):
    # If the user is already logged in, redirect them to the agent map page
    if request.user.is_authenticated:
        AgentActivity.objects.create(
            agent=request.user.agent,
            action='login',
            details={}
        )
        return redirect('Home')

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
                AgentActivity.objects.create(
                    agent=user.agent,
                    action='login',
                    details={}
                )
                return redirect('Home')  # redirect the user to the agent map page
    else:
        # if the request is not a POST request, create a new login form
        form = LoginForm()
    # render the login.html page with the form
    return render(request, 'login.html', {'form': form})


# This view will log the user out of the system
def logout_view(request):
    AgentActivity.objects.create(
        agent=request.user.agent,
        action='logout',
        details={}
    )
    logout(request)  # log the user out
    return redirect('Login')  # redirect the user to the login page

# This view will open the home page for the AgentMap project
@login_required(login_url='/login/')
def home(request):
    # We want to get the current agent based on the user
    agent = request.user.agent
    username = request.user.username
    print(f'Agent: {agent}')
    print(f'Username: {username}')

    # We want to get the states that the agent is licensed in
    licensed_states = agent.licensed_states.all()
    print(f'Licensed States: {licensed_states}')

    # Get the discount Keys
    discount_keys = HouseHoldDiscountKey.objects.all()

    if agent.user.is_superuser:
        # print(f'{agent} is a superuser, Loading all agents licensed states')
        all_licenses = {}  # Initialize as a dictionary
        for current_agent in Agent.objects.all():
            if current_agent.user.username == 'admin':
                continue
            for agent_license in current_agent.licensed_states.all():
                agent_name = agent_license.agent.user.username[0].upper() + agent_license.agent.user.username[1:]
                state_code = agent_license.state.state_code
                if state_code not in all_licenses:
                    all_licenses[state_code] = []  # Initialize as a list
                all_licenses[state_code].append(agent_name)  # Append agent_name to the list
        # print(f'All Licenses: {all_licenses}')
    else:
        # print(f'{agent} is not a superuser, Loading only their licensed states')
        all_licenses = {}

    # Get the Discount Key Legend
    discount_keys = HouseHoldDiscountKey.objects.all()

    # Set the MapLayer template variable to the MedicareSupplement Layer
    map_layer = 'MapLayer.html'
    product_type = 'MS'
    AEP = True

    if username == 'daltonB':
        aep_sets = {}
    elif AEP:
        aep_sets = {
            'kristinD': (
                'AL', 'AR', 'AZ', 'IA', 'IL', 'IN', 'MT', 'ND', 'NJ',
                'OH', 'SD', 'UT', 'VA', 'WY', 'WV'
            ),
            'rhondaL': (
                'CO', 'GA', 'ID', 'NC', 'NM', 'NV', 'PA', 'VT', 'FL',
                'KS', 'KY', 'LA', 'MD', 'MO', 'MS', 'NE', 'OK', 'OR',
                'SC', 'TN', 'TX', 'WA',
            ),
            'Both': (
                'CA', 'TX', 'OR'
            )
        }
    else:
        aep_sets = {}

    # pack the variables into the context dictionary
    context = {
        'all_licenses': all_licenses,
        'licensed_states': licensed_states,
        'map_layer': map_layer,
        'discount_keys': discount_keys,
        'aep_sets': aep_sets,
        'all_states': State.objects.all(),
        'product_type': product_type,
        'full_product_type': 'Medicare Supplement',
        'theme': request.session.get('theme', 'light')
    }
    context.update({'theme': request.session.get('theme', 'light')})
    print(context)
    return render(request, 'home.html', context=context)

# This view is the main view for the AgentMap project.
@login_required(login_url='/login/')
def agent_map(request, product_type):

    # We want to get the current agent based on the user
    agent = request.user.agent
    # print(f'Agent: {agent}')

    # We want to get the states that the agent is licensed in
    licensed_states = agent.licensed_states.all()
    print(f'Licensed States: {licensed_states}')

    # Get the discount Keys
    discount_keys = HouseHoldDiscountKey.objects.all()

    if agent.user.is_superuser:
        # print(f'{agent} is a superuser, Loading all agents licensed states')
        all_licenses = {}  # Initialize as a dictionary
        for current_agent in Agent.objects.all():
            if current_agent.user.username == 'admin':
                continue
            for agent_license in current_agent.licensed_states.all():
                agent_name = agent_license.agent.user.username[0].upper() + agent_license.agent.user.username[1:]
                state_code = agent_license.state.state_code
                if state_code not in all_licenses:
                    all_licenses[state_code] = []  # Initialize as a list
                all_licenses[state_code].append(agent_name)  # Append agent_name to the list
        # print(f'All Licenses: {all_licenses}')
    else:
        # print(f'{agent} is not a superuser, Loading only their licensed states')
        all_licenses = {}

    # Get the Discount Key Legend
    discount_keys = HouseHoldDiscountKey.objects.all()

    # create full_product_type dictionary
    full_product_type = {
        'MS': 'Medicare Supplement',
        'DVH': 'Dental Vision Hearing',
        'FE': 'Final Expense',
        'HI': 'Hospital Indemnity',
        'HHC': 'Home Health Care',
        'Cancer': 'Cancer'
    }

    # pack the variables into the context dictionary
    context = {
        'all_licenses': all_licenses,
        'licensed_states': licensed_states,
        'discount_keys': discount_keys,
        'product_type': product_type,
        'full_product_type': full_product_type[product_type]
        }
    print(context)
    return render(request, 'MapLayer.html', context=context)


# This view will render the Medicare Get_Companies
@login_required(login_url='/login/')
def get_companies(request, product_type, state_code):
    # Birthday Rule States
    birthday_rule_states = [
        "California", "Idaho", "Kentucky", "Maryland", "Missouri",
        "Nevada", "Oklahoma", "Oregon", "Washington"
    ]

    state_dictionary = {
        state_obj.state_code: state_obj.full_state for state_obj in State.objects.all()
    }


    # Get all the pdf's for the state
    pdfs = PDF.objects.filter(state__state_code=state_code).order_by('carrier')
    # for pdf in pdfs:
    #     print(pdf.id)

    state = state_dictionary[state_code]

    discounts = HouseHoldDiscount.objects.filter(state__state_code=state_code).order_by('carrier')

    current_date = timezone.now().date()

    # Get the Agents License Number and Expiration date for the given state
    agent = request.user.agent
    print(f'Agent: {agent}')
    # Get the most up to date license for the agent in the given state
    agent_license = agent.licensed_states.filter(state__state_code=state_code).order_by('expiration').last()
    print(f'Agent License: {agent_license}')
    if agent_license is not None:
        agent_license_num = agent_license.licenseNumber
        expiration = agent_license.expiration
        is_expiring_soon = (expiration - current_date <= timedelta(days=31))\
            if expiration else False
        days_until_expiration = (expiration - current_date).days \
            if expiration else 9999  # Set to huge number since NaN is not valid
    else:
        admin_acc = Agent.objects.filter(user__username='admin').first()
        print(f'Admin Account: {admin_acc}')
        admin_license = admin_acc.licensed_states.filter(state__state_code=state_code).order_by('expiration').last()
        agent_license_num = "Corp# " + admin_license.licenseNumber if admin_license else None
        expiration = None
        is_expiring_soon = False
        days_until_expiration = 9999  # Set to huge number since NaN is not valid

    context = {
        'state': state,
        'product_type': product_type,
        'pdfs': pdfs,
        'discounts': discounts,
        'agent_license_num': agent_license_num,
        'expiration': expiration,
        'is_expiring_soon': is_expiring_soon,
        'days_until_expiration': days_until_expiration,
        'birthday_rule_states': birthday_rule_states,
    }
    print(agent_license_num)

    AgentActivity.objects.create(
        agent=agent,
        action='get_companies',
        details={
            "Product Type": product_type,
            "State": state_code
        }
    )

    return render(request, 'Infobox.html', context=context)


@xframe_options_exempt
# This view will render the Medicare Supplement View_PDF
def view_pdf(request, pdf_id):
    print(f'PDF ID: {pdf_id}')
    pdf = get_object_or_404(PDF, id=pdf_id)
    print(f'PDF: {pdf}')

    file_path = pdf.file_path

    if os.name == 'nt':
        file_path = file_path.replace('\\', '/')

    if not file_path.startswith("static/Companies"):
        index = file_path.index("static/Companies")
        file_path = file_path[index:]
    elif "static/Companies" not in file_path:
        file_path = "static/Companies/" + file_path
    else:
        file_path = file_path

    if not file_path.startswith('static/'):
        raise SuspiciousOperation("Attempted Directory Traversal")

    AgentActivity.objects.create(
        agent=request.user.agent,
        action='view_pdf',
        details={
            "Carrier": pdf.carrier.carrier_name,
            "State": pdf.state.state_code,
            "Form Type": pdf.form_info.form_type
        }
    )

    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
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

    # translate the full staten name to the state code
    state_code = State.objects.get(full_state=state).state_code

    AgentActivity.objects.create(
        agent=request.user.agent,
        action='birthday_rules',
        details={
            "State": state_code
        }
    )

    # Create a response with the HTML content
    response = HttpResponse(html_content, content_type='text/html')

    return response


# This view will return a interactive map of the US with the clients coordinates are marked on the map
@login_required
@xframe_options_exempt
def client_map(request):
    return render(request, 'client_combined_map.html')


# This view will send the user to the Declinable Drug List Page
@login_required
def declinable_drug_list(request):
    # We will need to pack the data into a context dictionary to pass to the render
    # set the session to an empty list to make sure it gets cleared out anytime declinable drugs gets loaded
    request.session['last_response'] = []
    acceptanceRules = AcceptanceRule.objects.all()
    context = {
        'acceptanceRules': acceptanceRules,
    }
    AgentActivity.objects.create(
        agent=request.user.agent,
        action='declinable_drug_list',
        details={}
    )
    return render(request, 'declinable_drug_list.html', context=context)


# This function will add the drug to the last response
def add_drug(request):
    # Get the drug name from the POST parameters
    drug_name = request.POST.get('drug_name')

    # Fetch the AcceptanceRule objects that match the added drug
    matching_rules = AcceptanceRule.objects.filter(drug__drug_name__iexact=drug_name)

    # Prepare the matching rules data I want to change is_accepted True/False to be "Allowed" "Declined"
    matching_rules_data = []
    for rule in matching_rules:
        matching_rules_data.append({
            'carrier_name': rule.carrier.carrier_name,
            'drug_name': drug_name,
            'condition_name': rule.condition.condition_name,
            'is_accepted': 'Allowed' if rule.is_accepted else 'Declined',
        })

    # Get the last JsonResponse from the session if it exists
    last_response = request.session.get('last_response', [])
    # print(last_response)

    # check if the matching_rules_data contains any rows from the last_response
    # if it does, we do not want to add it to the matching_rules_data
    for last_row in last_response:
        for row in matching_rules_data:
            if last_row == row:
                matching_rules_data.remove(row)

    # Add the last response to the current matching rules data
    matching_rules_data.extend(last_response)
    # print(matching_rules_data)

    # Store the current response in the session for use in the next request
    request.session['last_response'] = matching_rules_data

    print(request.session['last_response'])

    return JsonResponse({
        'matching_rules': matching_rules_data,
    })


# This function will delete the drug from the last response
def delete_drug(request):
    # When the user clicks on the given drug, we will remove it from that drug-list
    drug_name = request.POST.get('drug_name')

    # Get the last_response list from the session
    last_response = request.session.get('last_response', [])

    # Filter the list to remove the rows that have the drug name
    filtered_response = [row for row in last_response if row['drug_name'] != drug_name]

    # Set the filtered list as the new last_response in the session
    request.session['last_response'] = filtered_response

    # Return the drug name as JSON
    return JsonResponse({'drug_name': drug_name})


# This function will clear the drugs from the last response
def clear_drugs(request):
    # Reload the session completely
    request.session['last_response'] = []
    # load the declined drug list page
    return redirect('Declined Drug Search')


# This function will return a list of drug names that start with the given query
def get_drug_names(request):
    # Get the drug name query from the GET parameter 'drug_name'
    query = request.GET.get('drug_name', '')
    # Filter the drugs that start with the query
    drugs = Drug.objects.filter(drug_name__istartswith=query).values_list('drug_name', flat=True)
    # Return the drugs as a JSON Response
    return JsonResponse(list(drugs), safe=False)


def rebate_calculator(request):
    AgentActivity.objects.create(
        agent=request.user.agent,
        action='rebate_calculator',
        details={}
    )
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get the POST data from the request
        post_data = request.POST
        print(post_data)

        drug_type = post_data.getlist('drug-type')
        fills_per_year = post_data.getlist('fills-per-year')

        # Remove any empty strings from the end of the lists, gets added by adding a new row which is annoying
        if fills_per_year[-1] == '':
            fills_per_year.pop()

        # check to make sure the drug type and fills per month are the same length
        if len(drug_type) != len(fills_per_year):
            return JsonResponse({'error': 'Drug Type and Fills Per Month must be the same length'})

        print(f'Drug Type: {drug_type}')
        print(f'Fills Per Month: {fills_per_year}')
        print(f'Generic Count: {drug_type.count("generic")}')
        print(f'Branded Count: {drug_type.count("branded")}')

        # Initialize the results list
        results = []
        gtl_total = 0
        hn_total = 0
        sl_total = 0
        unl_total = 0

        for i in range(len(drug_type)):

            # Get the drug type and fills per month values for the current index
            current_drug_type = drug_type[i]
            current_fills_per_month = fills_per_year[i]
            if current_drug_type == 'generic':
                gtl_total += 10 * int(current_fills_per_month)
                hn_total += 15 * int(current_fills_per_month)
                sl_total += 10 * int(current_fills_per_month)
                unl_total += 10 * int(current_fills_per_month)
            elif current_drug_type == 'branded':
                gtl_total += 25 * int(current_fills_per_month)
                hn_total += 30 * int(current_fills_per_month)
                sl_total += 25 * int(current_fills_per_month)
                unl_total += 25 * int(current_fills_per_month)

        # Print the totals for each carrier + the count of each drug type
        print(f'GTL Total: {gtl_total}')
        print(f'HN Total: {hn_total}')
        print(f'SL Total: {sl_total}')
        print(f'UNL Total: {unl_total}')

        results = [
            {
                'carrier': 'GTL',
                'bronze': min(300, gtl_total),
                'silver': min(600, gtl_total),
                'gold': min(900, gtl_total),
            },
            {
                'carrier': 'United Life',
                'bronze': min(300, unl_total),
                'silver': min(600, unl_total),
                'gold': min(900, unl_total),
            },
            {
                'carrier': 'Heartland National',
                'bronze': min(360, hn_total),
                'silver': min(720, hn_total),
                'gold': min(720, hn_total),
            },
            {
                'carrier': 'Standard Life',
                'bronze': min(300, sl_total),
                'silver': min(600, sl_total),
                'gold': min(600, sl_total),
            },
        ]
        return JsonResponse({'results': results})
    elif request.method == 'POST':
        # Handle form submission for non-AJAX requests
        print('Non-AJAX POST Request')
        results = [
            {
                'carrier': 'GTL Max rebates',
                'bronze': 300,
                'silver': 600,
                'gold': 900,
            },
            {
                'carrier:': 'UNL Max rebates',
                'bronze': 300,
                'silver': 600,
                'gold': 900,
            },
            {
                'carrier': 'HN Max rebates',
                'bronze': 360,
                'silver': 720,
                'gold': 720,
            },
            {
                'carrier': 'SL Max rebates',
                'bronze': 300,
                'silver': 600,
                'gold': 600,
            },
        ]
        return render(request, 'RebateCalculator.html', {'results': results})
    return render(request, 'RebateCalculator.html')


@login_required
def toggle_theme(request):
    # Get current theme from session or default to 'light'
    current_theme = request.session.get('theme', 'light')
    # Toggle theme
    new_theme = 'dark' if current_theme == 'light' else 'light'
    # Save to session
    request.session['theme'] = new_theme

    csrf_token = get_token(request)

    AgentActivity.objects.create(
        agent=request.user.agent,
        action='toggle_theme',
        details={
            "current_theme": current_theme,
        }
    )

    return HttpResponse(f"""
            <script>
                document.cookie = "csrftoken={csrf_token}; path=/";
                window.location.reload();
            </script>
        """)


# This function will handle the analytics for the agentMap
def analytics_view(request):
    agents = Agent.objects.all()
    actions = AgentActivity.objects.values_list('action', flat=True).distinct()
    excludedStates = ['ENT', 'PR']
    states = State.objects.exclude(state_code__in=excludedStates)
    product_types = ['MS', 'DVH', 'FE', 'HI', 'HHC', 'Cancer']
    form_types = FormType.objects.all()

    context = {
        'agents': agents,
        'actions': actions,
        'states': states,
        'product_types': product_types,
        'form_types': form_types,
    }
    return render(request, 'analytics.html', context)

def get_filtered_data(request):
    agent_ids = request.GET.get('agents')
    action = request.GET.get('action')
    state = request.GET.get('state')
    product_type = request.GET.get('product_types')
    form_type = request.GET.get('form_type')
    time_period = request.GET.get('period')
    print(f'Agent IDs: {agent_ids}')
    print(f'States: {state}')
    print(f'Time Period: {time_period}')

    activities = AgentActivity.objects.all()
    activities = activities.order_by('timestamp')

    # Exclude irrelevant actions
    activities = activities.exclude(action__in=['toggle_theme', 'login', 'logout'])

    if agent_ids:
        agent_ids_list = agent_ids.split(',')
        print(f'Agent IDs List: {agent_ids_list}')
        try:
            agent_ids_list = [Agent.objects.get(user__username=agent_id).id for agent_id in agent_ids_list]
            print(f'Agent IDs List after conversion: {agent_ids_list}')
            activities = activities.filter(agent_id__in=agent_ids_list)
        except Agent.DoesNotExist as e:
            print(f'Error: {e}')
            activities = activities.none()
    if action:
        activities = activities.filter(action=action)
    # if state:
    #     activities = activities.filter(details__icontains=f'"State": "{state}"')
    # if product_type:
    #     activities = activities.filter(details__icontains=f'"Product Type": "{product_type}"')
    # if form_type:
    #     activities = activities.filter(details__icontains=f'"Form Type": "{form_type}"')

    print(activities)

    if time_period:
        now = timezone.now()
        if time_period == '1':
            start_time = now - timedelta(hours=1)
        elif time_period == '24':
            start_time = now - timedelta(days=1)
        elif time_period == '168':
            start_time = now - timedelta(weeks=1)
        elif time_period == '696':
            start_time = now - timedelta(days=30)
        elif time_period == '2016':
            start_time = now - timedelta(days=90)
        elif time_period == '8064':
            start_time = now - timedelta(days=365)
        activities = activities.filter(timestamp__gte=start_time)

    data = {
        'datasets': []
    }

    agent_datasets = {}
    est = pytz.timezone('US/Eastern')

    for activity in activities:
        agent = activity.agent.user.username
        if agent not in agent_datasets:
            agent_datasets[agent] = {
                'name': agent,
                'activity': []
            }
        est_date = activity.timestamp.astimezone(est)
        agent_datasets[agent]['activity'].append({
            'date': est_date.strftime('%Y-%m-%d %H:%M:%S'),
            'action': activity.action
        })

    data['datasets'] = list(agent_datasets.values())
    return JsonResponse(data)