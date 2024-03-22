from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
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


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('AgentMap')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('Login')


# This function will render the map.html page
@login_required
def agent_map(request):
    licensed_states = LicensedState.objects.filter(agent__user=request.user)
    return render(request, 'map.html', {'licensed_states': licensed_states})


@login_required
# This function will get all the companies in the given state
def get_companies(request, state_code):
    forms = Form.objects.filter(state=state_code).order_by('company')
    # print("Forms: ", forms)
    state = StateDict[state_code]
    return render(request, "companies.html", {"state": state, "forms": forms})


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
