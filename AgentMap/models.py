from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Form(models.Model):
    company = models.CharField(max_length=30)
    full_company = models.CharField(max_length=200, default="N")
    state = models.CharField(max_length=2)
    form_type = models.CharField(max_length=200)
    full_form_type = models.CharField(max_length=200, default="N")
    date = models.CharField(max_length=4, default="None")
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.company + " - " + self.state + " - " + self.form_type


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class LicensedState(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    state = models.CharField(max_length=2)
    color = models.CharField(max_length=7, default="#0692e1")

    def __str__(self):
        return self.agent.user.username + " - " + self.state + " - " + self.color
