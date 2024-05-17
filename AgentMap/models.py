from django.db import models
from django.contrib.auth.models import User


# This model represents a pdf file that has been uploaded to the server.
class Form(models.Model):
    company = models.CharField(max_length=30)  # The abbreviated company name
    full_company = models.CharField(max_length=200, default="N")  # The full company name
    state = models.CharField(max_length=2)  # the state abbreviation
    form_type = models.CharField(max_length=200)  # The abbreviated form type
    full_form_type = models.CharField(max_length=200, default="N")  # The full form type
    date = models.CharField(max_length=8, default="None")  # The date the form is valid for
    file_path = models.CharField(max_length=255)  # the relative path to the file

    # This function returns a string representation of the form object
    def __str__(self):
        return self.company + " - " + self.state + " - " + self.form_type


# This model represents a user that is an agent
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # This function returns a string representation of the agent object
    def __str__(self):
        return self.user.username  # This is just the username of the agent


# This model represents a state that an agent is licensed in
class LicensedState(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)  # The agent that is licensed
    state = models.CharField(max_length=2)  # The state abbreviation
    licenseNumber = models.CharField(max_length=20, default="N/A")  # The license number
    expiration = models.DateField(default="2024-01-01")  # The expiration date of the license
    color = models.CharField(max_length=7, default="#0692e1")  # The color of the state on the map

    # This function returns a string representation of the licensed state object
    def __str__(self):
        return self.agent.user.username + " - " + self.state + " - " + self.expiration.strftime('%m/%d/%Y')


# This model represents a company that provides medicare supplement insurance
class MedicareSupplementAgencies(models.Model):
    agency_name = models.CharField(max_length=200)  # The name of the agency
    abbreviation = models.CharField(max_length=20, default="")  # The abbreviation of the agency

    class Meta:
        verbose_name_plural = "Medicare Supplement Agencies"

    def __str__(self):
        return self.agency_name


# This model represents a Drug
class Drugs(models.Model):
    drug_name = models.CharField(max_length=200)  # The name of the drug
    drug_classification = models.CharField(max_length=200)  # The classification of the drug

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
    acceptance = models.BooleanField(default=False)  # Whether the agency accepts the drug for the condition

    class Meta:
        verbose_name_plural = "Acceptance Rules"

    def __str__(self):
        return self.agency.agency_name + " - " + self.drug.drug_name + " - " + self.condition.condition_name
