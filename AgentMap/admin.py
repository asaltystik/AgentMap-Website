from django.contrib import admin
from AgentMap.models import (State, Carrier, FormType, PDF,
                             Agent, AgentLicensedState, Drug, MedicalCondition,
                             AcceptanceRule, HouseHoldDiscountKey,
                             HouseHoldDiscount, AgentActivity)


# Register your models here.
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(Carrier)
class MedicareSupplementCarrierAdmin(admin.ModelAdmin):
    pass


@admin.register(FormType)
class FormTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    pass


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    pass


@admin.register(AgentLicensedState)
class AgentLicensedStateAdmin(admin.ModelAdmin):
    pass


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    pass


@admin.register(MedicalCondition)
class MedicalConditionAdmin(admin.ModelAdmin):
    pass


@admin.register(HouseHoldDiscountKey)
class HouseHoldDiscountKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(HouseHoldDiscount)
class HouseHoldDiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(AcceptanceRule)
class AcceptanceRuleAdmin(admin.ModelAdmin):
    pass

@admin.register(AgentActivity)
class AgentActivityAdmin(admin.ModelAdmin):
    list_display = ('agent', 'action', 'details', 'timestamp')
    readonly_fields = ('agent', 'action', 'details', 'timestamp')