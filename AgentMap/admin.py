from django.contrib import admin

from AgentMap.models import (Agent, Form, LicensedState,
                             MedicareSupplementCarrier,
                             Drug, MedicalCondition,
                             FormType, State,
                             HouseHoldDiscountKey,
                             HouseHoldDiscount,
                             AcceptanceRule
                             )


# Registration of the Form model in the admin site
@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


# Registration of the Agent model in the admin site
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    pass


# Registration of the LicensedState model in the admin site
@admin.register(LicensedState)
class LicensedStateAdmin(admin.ModelAdmin):
    pass


# Registration of the MedicareSupplementAgencies model in the admin site
@admin.register(MedicareSupplementCarrier)
class MedicareSupplementCarriersAdmin(admin.ModelAdmin):
    pass


# Registration of the Drugs model in the admin site
@admin.register(Drug)
class DrugsAdmin(admin.ModelAdmin):
    pass


# Registration of the MedicalConditions model in the admin site
@admin.register(MedicalCondition)
class MedicalConditionsAdmin(admin.ModelAdmin):
    pass


@admin.register(FormType)
class FormTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(HouseHoldDiscountKey)
class HouseholdDiscountKeysAdmin(admin.ModelAdmin):
    pass


@admin.register(HouseHoldDiscount)
class HouseholdDiscountsAdmin(admin.ModelAdmin):
    pass

@admin.register(AcceptanceRule)
class AcceptanceRulesAdmin(admin.ModelAdmin):
    pass