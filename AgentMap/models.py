from django.db import models
from django.contrib.auth.models import User


class State(models.Model):
    state_code = models.CharField(max_length=3)  # The state abbreviation
    full_state = models.CharField(max_length=200)  # The full state name

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return self.state_code


# This model represents a company that provides medicare supplement insurance
class MedicareSupplementAgencies(models.Model):
    agency_name = models.CharField(max_length=200)  # The name of the agency
    abbreviation = models.CharField(max_length=20, default="")  # The abbreviation of the agency
    app_url = models.CharField(max_length=900, default="")  # The url to the application

    class Meta:
        verbose_name_plural = "Medicare Supplement Agencies"

    def __str__(self):
        return self.agency_name


# This model will be used to store the different types of forms that are available
class FormTypes(models.Model):
    form_type = models.CharField(max_length=200)  # The abbreviated form type
    full_form_type = models.CharField(max_length=200)  # The full form type

    class Meta:
        verbose_name_plural = "Form Types"

    def __str__(self):
        return self.form_type


# This model represents a pdf file that has been uploaded to the server.
class Form(models.Model):
    company = models.ForeignKey(MedicareSupplementAgencies, related_name='forms', on_delete=models.CASCADE)  # The abbreviated company name
    state = models.ForeignKey(State, on_delete=models.CASCADE)  # the state abbreviation
    form_info = models.ForeignKey(FormTypes, on_delete=models.CASCADE)  # the form type
    date = models.CharField(max_length=8, default="None")  # The date the form is valid for
    file_path = models.CharField(max_length=255)  # the relative path to the file

    # This function returns a string representation of the form object
    def __str__(self):
        return self.company.agency_name + " - " + self.state.state_code + " - " + self.form_info.form_type


# This model represents a user that is an agent
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # This function returns a string representation of the agent object
    def __str__(self):
        return self.user.username  # This is just the username of the agent


# This model represents a state that an agent is licensed in
class LicensedState(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)  # The agent that is licensed
    state = models.ForeignKey(State, on_delete=models.CASCADE)  # The state that the agent is licensed in
    licenseNumber = models.CharField(max_length=20, default="N/A")  # The license number
    expiration = models.DateField(default="2024-01-01")  # The expiration date of the license

    # This function returns a string representation of the licensed state object
    def __str__(self):
        return self.agent.user.username + " - " + self.state.state_code + " - " + self.expiration.strftime('%m/%d/%Y')


# This model represents a Drug
class Drugs(models.Model):
    drug_name = models.CharField(max_length=200)  # The name of the drug
    drug_classification = models.CharField(max_length=200, blank=True)  # The classification of the drug

    def __str__(self):
        return self.drug_name

    class Meta:
        verbose_name_plural = "Drugs"


# This model represents a Medical Condition
class MedicalConditions(models.Model):
    condition_name = models.CharField(max_length=200)  # The name of the condition

    class Meta:
        verbose_name_plural = "Medical Conditions"

    def __str__(self):
        return self.condition_name


# This model will contain the Acceptance rules companies given a drug, and condition
class AcceptanceRules(models.Model):
    agency = models.ForeignKey(MedicareSupplementAgencies, on_delete=models.CASCADE)  # The agency that accepts the drug
    drug = models.ForeignKey(Drugs, on_delete=models.CASCADE)  # The drug that is accepted
    condition = models.ForeignKey(MedicalConditions, default=0, on_delete=models.CASCADE)  # The condition that is accepted
    is_accepted = models.BooleanField(default=False)  # Whether the agency accepts the drug for the condition

    class Meta:
        verbose_name_plural = "Acceptance Rules"

    def __str__(self):
        return self.agency.agency_name + " - " + self.drug.drug_name + " - " + self.condition.condition_name + " - " + str(self.is_accepted)


# This model will contain the HouseHoldDiscount colors
class HouseHoldDiscountKey(models.Model):
    discount_type = models.CharField(max_length=200)  # The type of discount
    description = models.CharField(max_length=999)  # The description of the discount
    color = models.CharField(max_length=20)  # The color of the discount

    class Meta:
        verbose_name_plural = "HouseHold Discount Keys"

    def __str__(self):
        return self.discount_type + " - " + self.color


# This model will contain the State by State Household Discounts
class HouseHoldDiscounts(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)  # The state that the discount is for
    agency = models.ForeignKey(MedicareSupplementAgencies, on_delete=models.CASCADE)  # The company that the discount is for
    discount = models.ForeignKey(HouseHoldDiscountKey, on_delete=models.CASCADE)  # The discount that is available

    class Meta:
        verbose_name_plural = "HouseHold Discounts"

    def __str__(self):
        return self.state.state_code + " - " + self.agency.agency_name + " - " + self.discount.discount_type
