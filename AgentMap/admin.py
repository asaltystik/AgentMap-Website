from django.contrib import admin

from AgentMap.models import Agent, Form, LicensedState


# Registration of the models in the admin site
@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    pass


@admin.register(LicensedState)
class LicensedStateAdmin(admin.ModelAdmin):
    pass
