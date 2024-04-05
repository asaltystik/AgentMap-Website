from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from AgentMap.models import LicensedState, Agent


class Command(BaseCommand):
    help = ("Warns agents of upcoming license expirations by sending an email"
            " to the agent's email address.")

    def handle(self, *args, **kwargs):
        # Get the current date and the last day of the current month
        current_date = timezone.now().date()  # Today's date
        end_date = current_date + timedelta(days=31)  # Doing 31 days to cover the 7 months with 31 days.
        # Ignoring the case of a leap year cause the next one is 4 years away.

        # Query the LicensedState model for any licenses expiring within the current month
        expiring_licenses = LicensedState.objects.filter(expiration__range=(current_date, end_date))

        # Group the results by agent
        agents = expiring_licenses.values('agent').annotate(num_expiring=Count('id'))

        # For each unique agent, gather all their upcoming expirations and send an email
        for agent in agents:
            agent_obj = Agent.objects.get(id=agent['agent'])
            agent_expirations = expiring_licenses.filter(agent=agent_obj)
            expirations_str = "\n".join([f"License {expiring_license.licenseNumber}"
                                         f" in state {expiring_license.state}"
                                         f" expires on {expiring_license.expiration.strftime('%m/%d/%Y')}"
                                         for expiring_license in agent_expirations])
            send_mail(
                'License Expiration Notice',
                f'You have {agent["num_expiring"]} license(s) expiring'
                f' this month:\n{expirations_str}',
                'carick@securecare65.com',
                [agent_obj.user.email],
                fail_silently=False,
            )
        print(f'{len(agents)} agent(s) notified of upcoming license expirations.')
        print(f'Agents notified:\n {"\n".join([Agent.objects.get(id=agent['agent']).user.email for agent in agents])}\n')
