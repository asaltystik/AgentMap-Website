"""
URL configuration for AgentMap_MultiLayer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from AgentMap import views as agent_map_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', agent_map_view.home, name='Home'),
    path('agent_map/<str:product_type>/', agent_map_view.agent_map, name='AgentMapLayer'),
    path('get_companies/<str:product_type>/<str:state_code>/', agent_map_view.get_companies, name='get_companies'),
    path('view_pdf/<int:pdf_id>/', agent_map_view.view_pdf, name='view_pdf'),
    path('birthday_rules/<str:state>', agent_map_view.birthday_rules, name='birthday_rules'),
    path('clientMap/', agent_map_view.client_map, name='ClientMap'),
    path('declined_drugs/', agent_map_view.declinable_drug_list, name='Declined Drug Search'),
    path('add_drug/', agent_map_view.add_drug, name='Add Drug'),
    path('delete_drug/', agent_map_view.delete_drug, name='Delete Drug'),
    path('clear_drugs/', agent_map_view.clear_drugs, name='Clear Drugs'),
    path('get_drug_names/', agent_map_view.get_drug_names, name='Get Drug Names'),
    path('rebate_calculator/', agent_map_view.rebate_calculator, name='RebateCalculator'),
    path('login/', agent_map_view.login_view, name='Login'),
    path('logout/', agent_map_view.logout_view, name='Logout'),
]
