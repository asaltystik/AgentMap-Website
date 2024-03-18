from django.contrib import admin

from AgentMap.models import Form


# Register your models here.
@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass