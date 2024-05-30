"""
URL configuration for djangoMap project.

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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('AgentMap/', include('AgentMap.urls')),  # Include the urls found in AgentMap.urls
    path('get_companies/<str:state_code>/', agent_map_view.get_companies, name='get_companies'),
    path('view_form/<int:form_id>/', agent_map_view.view_form, name='view_form'),
    path('admin/', admin.site.urls),
    path('', agent_map_view.agent_map, name='AgentMap'),
    path('login/', agent_map_view.login_view, name='Login'),
    path('logout/', agent_map_view.logout_view, name='Logout'),
    path('register/', agent_map_view.register_view, name='Register'),
    path('birthday_rules/<str:state>', agent_map_view.birthday_rules, name='birthday_rules'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)