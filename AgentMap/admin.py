from django.contrib import admin

from AgentMap.models import (Agent, Form, LicensedState,
                             MedicareSupplementAgencies,
                             Drugs, MedicalConditions,
                             FormTypes, State,
                             HouseHoldDiscountKey,
                             HouseHoldDiscounts,
                             AcceptanceRules
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
@admin.register(MedicareSupplementAgencies)
class MedicareSupplementAgenciesAdmin(admin.ModelAdmin):
    pass


# Registration of the Drugs model in the admin site
@admin.register(Drugs)
class DrugsAdmin(admin.ModelAdmin):
    pass


# Registration of the MedicalConditions model in the admin site
@admin.register(MedicalConditions)
class MedicalConditionsAdmin(admin.ModelAdmin):
    pass


@admin.register(FormTypes)
class FormTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(HouseHoldDiscountKey)
class HouseholdDiscountKeysAdmin(admin.ModelAdmin):
    pass


@admin.register(HouseHoldDiscounts)
class HouseholdDiscountsAdmin(admin.ModelAdmin):
    pass

@admin.register(AcceptanceRules)
class AcceptanceRulesAdmin(admin.ModelAdmin):
    pass