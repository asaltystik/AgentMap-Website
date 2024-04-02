from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import Count
from calendar import monthrange
from django.utils import timezone
from AgentMap.models import LicensedState, Agent


class Command(BaseCommand):
    help = ("Warns agents of upcoming license expirations by sending an email"
            " to the agent's email address.")

    def handle(self, *args, **kwargs):
        # Get the current date and the last day of the current month
        current_date = timezone.now().date()
        _, last_day = monthrange(current_date.year, current_date.month)
        end_of_month = current_date.replace(day=last_day)

        # Query the LicensedState model for any licenses expiring within the current month
        expiring_licenses = LicensedState.objects.filter(expiration__range=(current_date, end_of_month))

        # Group the results by agent
        agents = expiring_licenses.values('agent').annotate(num_expiring=Count('id'))

        # For each unique agent, gather all their upcoming expirations and send an email
        for agent in agents:
            agent_obj = Agent.objects.get(id=agent['agent'])
            agent_expirations = expiring_licenses.filter(agent=agent_obj)
            expirations_str = "\n".join([f"License {exp.licenseNumber}"
                                         f" in state {exp.state}"
                                         f" expires on {exp.expiration}"
                                         for exp in agent_expirations])
            send_mail(
                'License Expiration Notice',
                f'You have {agent["num_expiring"]} license(s) expiring'
                f' this month:\n{expirations_str}',
                'carick@securecare65.com',
                [agent_obj.user.email],
                fail_silently=False,
            )
        print(f'{len(agents)} agents notified of upcoming license expirations.')