from django.db import models
from django.contrib.auth.models import User


# This model represents a state
class State(models.Model):
    state_code = models.CharField(max_length=3)  # The state abbreviation
    full_state = models.CharField(max_length=200)  # The full state name

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return self.state_code


# This model represents a company that provides a service we sign our customers up for
class Carrier(models.Model):
    carrier_name = models.CharField(max_length=200)  # The name of the agency
    abbreviation = models.CharField(max_length=20, default="")  # The abbreviation of the agency
    app_url = models.CharField(max_length=900, default="")  # The url to the application

    class Meta:
        verbose_name_plural = "Carriers"

    def __str__(self):
        return self.carrier_name


# This model will be used to store the different types of forms that are available
class FormType(models.Model):
    form_type = models.CharField(max_length=200)  # The abbreviated form type
    full_form_type = models.CharField(max_length=200)  # The full form type

    class Meta:
        verbose_name_plural = "Form Types"

    def __str__(self):
        return self.form_type


# This model represents a pdf file that has been uploaded to the server db.
class PDF(models.Model):
    carrier = models.ForeignKey(Carrier, related_name='pdfs', on_delete=models.CASCADE)  # The abbreviated company name
    state = models.ForeignKey(State, on_delete=models.CASCADE)  # the state abbreviation
    form_info = models.ForeignKey(FormType, on_delete=models.CASCADE)  # the form type
    date = models.CharField(max_length=20, default="", blank=True)  # The date the form is valid for
    file_path = models.CharField(max_length=255)  # the relative path to the file

    # This function returns a string representation of the form object
    def __str__(self):
        return self.carrier.carrier_name + " - " + self.state.state_code + " - " + self.form_info.form_type


# This Model represents a user that is an agent
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # This function returns a string representation of the agent object
    def __str__(self):
        return self.user.username  # This is just the username of the agent


# This model represents an agents licensed state
class AgentLicensedState(models.Model):
    agent = models.ForeignKey(Agent, related_name='licensed_states', on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    licenseNumber = models.CharField(max_length=200, blank=True)
    expiration = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Agent Licensed States"

    def __str__(self):
        return self.agent.user.username + " - " + self.state.state_code


# This model represents a drug
class Drug(models.Model):
    drug_name = models.CharField(max_length=200)  # The name of the drug
    drug_classification = models.CharField(max_length=200, blank=True)  # The classification of the drug

    def __str__(self):
        return self.drug_name

    class Meta:
        verbose_name_plural = "Drugs"


# This model represents a Medical Condition
class MedicalCondition(models.Model):
    condition_name = models.CharField(max_length=200)  # The name of the condition
    condition_description = models.TextField(blank=True)  # The description of the condition

    def __str__(self):
        return self.condition_name

    class Meta:
        verbose_name_plural = "Medical Conditions"


# This model represents a rule for a carrier to accept a drug for a medical condition
class AcceptanceRule(models.Model):
    carrier = models.ForeignKey(Carrier, related_name='acceptance_rules', on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, related_name='acceptance_rules', on_delete=models.CASCADE)
    condition = models.ForeignKey(MedicalCondition, related_name='acceptance_rules', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Acceptance Rules"

    def __str__(self):
        return self.carrier.carrier_name + " - " + self.drug.drug_name + " - " + self.condition.condition_name + " - " + str(self.is_accpeted)


# This model represents an entry for the Household Discount Key legend
class HouseHoldDiscountKey(models.Model):
    discount_type = models.CharField(max_length=200)  # The type of discount
    description = models.CharField(max_length=999)  # The description of the discount
    color = models.CharField(max_length=100)  # The color of the discount

    class Meta:
        verbose_name_plural = "HouseHold Discount Keys"

    def __str__(self):
        return self.discount_type + " - " + self.color


# This model represents a carrier's household discount for a given state
class HouseHoldDiscount(models.Model):
    state = models.ForeignKey(State, related_name='household_discounts', on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, related_name='household_discounts', on_delete=models.CASCADE)
    discount = models.ForeignKey(HouseHoldDiscountKey, related_name='household_discounts', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "HouseHold Discounts"

    def __str__(self):
        return self.carrier.carrier_name + " - " + self.state.state_code + " - " + self.discount.discount_type

