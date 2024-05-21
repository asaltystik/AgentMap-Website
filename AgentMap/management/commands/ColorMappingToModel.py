from django.core.management.base import BaseCommand
from AgentMap.models import HouseHoldDiscounts, State, MedicareSupplementAgencies, HouseHoldDiscountKey
import time


def add_color_mapping_to_model():
    colorMapping = {
        "Alabama": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "red",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "Alaska": {
            "AARP": "green",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "Cigna Loyal American Life Insurance": "green",
            "Mutual of Omaha": "red",
            "United American": "red"
        },
        "Arizona": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Bankers Fidelity Atlantic American": "grey",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "New Era": "green",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Arkansas": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Bankers Fidelity Atlantic American": "grey",
            "Cigna Health and Life Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "California": {
            "AARP": "green",
            "Aetna": "green",
            "Aflac": "grey",
            "Cigna Health and Life Insurance": "grey",
            "Elips Life Insurance": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "Colorado": {
            "AARP": "green",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Lumico": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Connecticut": {
            "AARP": "green",
            "Aetna": "red",
            "Cigna National Health Insurance": "green",
            "Mutual of Omaha": "red",
            "United American": "red"
        },
        "Delaware": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "Cigna Health and Life Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "District of Columbia": {
            "Aetna": "green",
            "Cigna Loyal American Life Insurance": "green",
            "LifeShield National Insurance": "grey",
            "Mutual of Omaha": "red"
        },
        "Florida": {
            "AARP": "green",
            "American Benefit Life": "green",
            "Ace Chubb": "green",
            "Aetna": "red",
            "Aflac": "green",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "green",
            "LifeShield National Insurance": "green",
            "New Era": "red",
            "Mutual of Omaha": "red",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Georgia": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Bankers Fidelity Atlantic American": "grey",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "Hawaii": {
            "Cigna Loyal American Life Insurance": "red",
            "Mutual of Omaha": "red",
            "United American": "red"
        },
        "Idaho": {
            "AARP": "green",
            "Ace Chubb": "red",
            "Aetna": "red",
            "Aflac": "red",
            "Cigna Health and Life Insurance": "red",
            "Manhattan Life": "red",
            "Mutual of Omaha": "red",
            "United American": "red"
        },
        "Illinois": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "grey",
            "Cigna National Health Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Iowa": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "green",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Indiana": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "green",
            "Ace Chubb": "green",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "American Financial Security": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "green",
            "LifeShield National Insurance": "grey",
            "New Era": "green",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Kansas": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Kentucky": {
            "AARP": "green",
            "American Benefit Life": "green",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "green",
            "American Financial Security": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Louisiana": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "Philadelphia American Life Insurance": "green",
            "United American": "red",
        },
        "Maine": {
            "AARP": "green",
            "Cigna Health and Life Insurance": "green",
            "Mutual of Omaha": "green",
            "United American": "red"
        },
        "Maryland": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Massachusetts": {
        },
        "Michigan": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "Philadelphia American Life Insurance": "green",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Minnesota": {
            "AARP": "green",
            "Aetna": "red",
            "Cigna Health and Life Insurance": "red",
            "Lumico": "red",
            "Mutual of Omaha": "red",
            "United American": "red"
        },
        "Mississippi": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Bankers Fidelity Atlantic American": "grey",
            "Cigna Health and Life Insurance": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "Missouri": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Cigna Health and Life Insurance": "green",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "#8576FF",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Montana": {
            "AARP": "green",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "grey",
            "Lumico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Nebraska": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Nevada": {
            "AARP": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green"
        },
        "New Hampshire": {
            "AARP": "green",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "Cigna Health and Life Insurance": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "New Jersey": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "green",
            "Ace Chubb": "green",
            "Aetna": "green",
            "Aflac": "green",
            "Cigna Health and Life Insurance": "green",
            "Cigna National Health Insurance": "grey",
            "Lumico": "green",
            "LifeShield National Insurance": "green",
            "Manhattan Life": "green",
            "Mutual of Omaha": "green",
            "United American": "red"
        },
        "New Mexico": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Bankers Fidelity Atlantic American": "grey",
            "Cigna Health and Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Lumico": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "New York": {
            "AARP": "red",
            "Mutual of Omaha": "red"
        },
        "North Carolina": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Bankers Fidelity Atlantic American": "grey",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "North Dakota": {
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "green",
            "Aetna": "red",
            "Aflac": "green",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "grey",
            "Elips Life Insurance": "green",
            "LifeShield National Insurance": "green",
            "Manhattan Life": "green",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Ohio": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "green",
            "Ace Chubb": "green",
            "Aetna": "green",
            "Aflac": "green",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna National Health Insurance": "green",
            "Elips Life Insurance": "green",
            "LifeShield National Insurance": "green",
            "Manhattan Life": "green",
            "Medico": "green",
            "Mutual of Omaha": "green",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Oklahoma": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "green",
            "Ace Chubb": "green",
            "Aetna": "green",
            "Aflac": "green",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna National Health Insurance": "green",
            "LifeShield National Insurance": "green",
            "New Era": "green",
            "Manhattan Life": "green",
            "Medico": "green",
            "Mutual of Omaha": "green",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Oregon": {
            "AARP": "green",
            "Aetna": "grey",
            "Aflac": "grey",
            "Cigna Health and Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Lumico": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "Pennsylvania": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "green",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "Cigna National Health Insurance": "#8576FF",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "green",
            "Medico": "#8576FF",
            "Mutual of Omaha": "#8576FF",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Rhode Island": {
            "AARP": "green",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "Cigna Health and Life Insurance": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "South Carolina": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "Philadelphia American Life Insurance": "green",
            "United American": "red"
        },
        "South Dakota": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "red",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "Philadelphia American Life Insurance": "green",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Tennessee": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "New Era": "red",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Texas": {
            "AARP": "green",
            "AARP UHICA": "grey",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Bankers Fidelity Atlantic American": "grey",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "Philadelphia American Life Insurance": "green",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Utah": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "Vermont": {
            "AARP": "red",
            "Aetna": "red",
            "Aflac": "red",
            "Cigna Health and Life Insurance": "red",
            "Mutual of Omaha": "red",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Virginia": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Financial Security": "green",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "green",
            "Elips Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        },
        "Washington": {
            "AARP": "green",
            "Cigna Health and Life Insurance": "green",
            "Elips Life Insurance": "green",
            "Medico": "green",
            "Mutual of Omaha": "green",
            "United American": "red"
        },
        "West Virginia": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Wisconsin": {
            "AARP": "green",
            "American Benefit Life": "grey",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna National Health Insurance": "grey",
            "Elips Life Insurance": "grey",
            "Manhattan Life": "grey",
            "Medico": "grey",
            "Mutual of Omaha": "grey",
            "WPS Health Insurance": "green",
            "United American": "red"
        },
        "Wyoming": {
            "AARP": "green",
            "Ace Chubb": "grey",
            "Aetna": "green",
            "Aflac": "grey",
            "American Home Life": "green",
            "Cigna Health and Life Insurance": "grey",
            "LifeShield National Insurance": "grey",
            "Manhattan Life": "grey",
            "Mutual of Omaha": "grey",
            "United American": "red"
        }
    }

    ColorKey = {
        "green": "#008000",
        "red": "#ff0000",
        "grey": "#808080",
        "#8576FF": "#8576FF"
    }

    for state, companies in colorMapping.items():
        state_id = State.objects.get(full_state=state)
        for agency, color in companies.items():
            # Get the company object
            try:
                agency_id = MedicareSupplementAgencies.objects.get(agency_name=agency)
            except MedicareSupplementAgencies.DoesNotExist:
                print(f"Company {agency} does not exist in the database.")
                time.sleep(50)

            print(f"State: {state}, Company: {agency}, Color: {color}")

            # decode the color
            color = ColorKey[color]

            # Get the color object
            discount_id = HouseHoldDiscountKey.objects.get(color=color)

            print(f"State ID: {state_id}, Agency ID: {agency_id}, Discount ID: {discount_id}")

            # Check if an entry with the same state and company already exists
            existing_entry = HouseHoldDiscounts.objects.filter(state_id=state_id, agency_id=agency_id).first()
            if existing_entry is None:
                # Create a new HouseHoldDiscount object

                HouseHoldDiscounts.objects.get_or_create(
                    state=state_id,
                    agency=agency_id,
                    discount=discount_id
                )
            else:
                print(f"Entry for state {state} and company {agency} already exists.")


class Command(BaseCommand):
    help = 'Add color mapping to the HouseHoldDiscounts model'

    def handle(self, *args, **options):
        add_color_mapping_to_model()
        return 0
