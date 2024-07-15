from django.core.management.base import BaseCommand
from AgentMap.models import HouseHoldDiscount, State, MedicareSupplementCarrier, HouseHoldDiscountKey
import time


def add_color_mapping_to_model():
    colorMapping = {
        "Alabama": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "NONE",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "Alaska": {
            "AARP": "SPOUSAL",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "Cigna Loyal American Life Insurance": "SPOUSAL",
            "Mutual of Omaha": "NONE",
            "United American": "NONE"
        },
        "Arizona": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "New Era": "SPOUSAL",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Arkansas": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna Health and Life Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "California": {
            "AARP": "SPOUSAL",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "Cigna Health and Life Insurance": "RM",
            "Elips Life Insurance": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "Colorado": {
            "AARP": "SPOUSAL",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Lumico": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Connecticut": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Aetna": "NONE",
            "Cigna National Health Insurance": "SPOUSAL",
            "Mutual of Omaha": "NONE",
            "United American": "NONE"
        },
        "Delaware": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "Cigna Health and Life Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "District of Columbia": {
            "Aetna": "SPOUSAL",
            "Cigna Loyal American Life Insurance": "SPOUSAL",
            "LifeShield National Insurance": "RM",
            "Mutual of Omaha": "NONE"
        },
        "Florida": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "SPOUSAL",
            "Ace Chubb": "SPOUSAL",
            "Aetna": "NONE",
            "Aflac": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "LifeShield National Insurance": "SPOUSAL",
            "New Era": "NONE",
            "Mutual of Omaha": "NONE",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Georgia": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "Hawaii": {
            "Cigna Loyal American Life Insurance": "NONE",
            "Mutual of Omaha": "NONE",
            "United American": "NONE"
        },
        "Idaho": {
            "AARP": "SPOUSAL",
            "Ace Chubb": "NONE",
            "Aetna": "NONE",
            "Aflac": "NONE",
            "Cigna Health and Life Insurance": "NONE",
            "Manhattan Life": "NONE",
            "Mutual of Omaha": "NONE",
            "United American": "NONE"
        },
        "Illinois": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "RM",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Iowa": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Indiana": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "SPOUSAL",
            "Ace Chubb": "SPOUSAL",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "American Financial Security": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "SPOUSAL",
            "LifeShield National Insurance": "RM",
            "New Era": "SPOUSAL",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Kansas": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Kentucky": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "SPOUSAL",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "SPOUSAL",
            "American Financial Security": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Louisiana": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "Philadelphia American Life Insurance": "SPOUSAL",
            "United American": "NONE",
        },
        "Maine": {
            "AARP": "SPOUSAL",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "Mutual of Omaha": "SPOUSAL",
            "United American": "NONE"
        },
        "Maryland": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Massachusetts": {
        },
        "Michigan": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "Philadelphia American Life Insurance": "SPOUSAL",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Minnesota": {
            "AARP": "SPOUSAL",
            "Aetna": "NONE",
            "Cigna Health and Life Insurance": "NONE",
            "Lumico": "NONE",
            "Mutual of Omaha": "NONE",
            "United American": "NONE"
        },
        "Mississippi": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "Missouri": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "MARRIED",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Montana": {
            "AARP": "SPOUSAL",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Cigna Health and Life Insurance": "RM",
            "Lumico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Nebraska": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Cigna Health and Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Nevada": {
            "AARP": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL"
        },
        "New Hampshire": {
            "AARP": "SPOUSAL",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "Cigna Health and Life Insurance": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "New Jersey": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "SPOUSAL",
            "Ace Chubb": "SPOUSAL",
            "Aetna": "SPOUSAL",
            "Aflac": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Lumico": "SPOUSAL",
            "LifeShield National Insurance": "SPOUSAL",
            "Manhattan Life": "SPOUSAL",
            "Mutual of Omaha": "SPOUSAL",
            "United American": "NONE"
        },
        "New Mexico": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna Health and Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Lumico": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "New York": {
            "AARP": "NONE",
            "Mutual of Omaha": "NONE"
        },
        "North Carolina": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "North Dakota": {
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "SPOUSAL",
            "Aetna": "NONE",
            "Aflac": "SPOUSAL",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Cigna Health and Life Insurance": "RM",
            "Elips Life Insurance": "SPOUSAL",
            "LifeShield National Insurance": "SPOUSAL",
            "Manhattan Life": "SPOUSAL",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Ohio": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "SPOUSAL",
            "Ace Chubb": "SPOUSAL",
            "Aetna": "SPOUSAL",
            "Aflac": "SPOUSAL",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "SPOUSAL",
            "Elips Life Insurance": "SPOUSAL",
            "LifeShield National Insurance": "SPOUSAL",
            "Manhattan Life": "SPOUSAL",
            "Medico": "SPOUSAL",
            "Mutual of Omaha": "SPOUSAL",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Oklahoma": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "SPOUSAL",
            "Ace Chubb": "SPOUSAL",
            "Aetna": "SPOUSAL",
            "Aflac": "SPOUSAL",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "SPOUSAL",
            "LifeShield National Insurance": "SPOUSAL",
            "New Era": "SPOUSAL",
            "Manhattan Life": "SPOUSAL",
            "Medico": "SPOUSAL",
            "Mutual of Omaha": "SPOUSAL",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Oregon": {
            "AARP": "SPOUSAL",
            "Aetna": "RM",
            "Aflac": "RM",
            "Cigna Health and Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Lumico": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "Pennsylvania": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "SPOUSAL",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "Cigna National Health Insurance": "MARRIED",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "SPOUSAL",
            "Medico": "MARRIED",
            "Mutual of Omaha": "MARRIED",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Rhode Island": {
            "AARP": "SPOUSAL",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "Cigna Health and Life Insurance": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "South Carolina": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "Philadelphia American Life Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "South Dakota": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "NONE",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "Philadelphia American Life Insurance": "SPOUSAL",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Tennessee": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "New Era": "NONE",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Texas": {
            "AARP": "SPOUSAL",
            "AARP UHICA": "RM",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "Philadelphia American Life Insurance": "SPOUSAL",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Utah": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "Vermont": {
            "AARP": "NONE",
            "Aetna": "NONE",
            "Aflac": "NONE",
            "Cigna Health and Life Insurance": "NONE",
            "Mutual of Omaha": "NONE",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Virginia": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Financial Security": "SPOUSAL",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "Elips Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        },
        "Washington": {
            "AARP": "SPOUSAL",
            "Cigna Health and Life Insurance": "SPOUSAL",
            "Elips Life Insurance": "SPOUSAL",
            "Medico": "SPOUSAL",
            "Mutual of Omaha": "SPOUSAL",
            "United American": "NONE"
        },
        "West Virginia": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Bankers Fidelity Atlantic American": "RM",
            "Cigna Health and Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Wisconsin": {
            "AARP": "SPOUSAL",
            "American Benefit Life": "RM",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna National Health Insurance": "RM",
            "Elips Life Insurance": "RM",
            "Manhattan Life": "RM",
            "Medico": "RM",
            "Mutual of Omaha": "RM",
            "WPS Health Insurance": "SPOUSAL",
            "United American": "NONE"
        },
        "Wyoming": {
            "AARP": "SPOUSAL",
            "Ace Chubb": "RM",
            "Aetna": "SPOUSAL",
            "Aflac": "RM",
            "American Home Life": "SPOUSAL",
            "Cigna Health and Life Insurance": "RM",
            "LifeShield National Insurance": "RM",
            "Manhattan Life": "RM",
            "Mutual of Omaha": "RM",
            "United American": "NONE"
        }
    }

    ColorKey = {
        "SPOUSAL": "oklch(78.19% 0.072 202.61)",
        "NONE": "oklch(76.85% 0.086 33.54)",
        "RM": "oklch(87.95% 0.083 85.69)",
        "MARRIED": "oklch(76.52% 0.083 284.28)"
    }

    for state, companies in colorMapping.items():
        state_id = State.objects.get(full_state=state)
        for carrier, color in companies.items():
            # Get the company object
            try:
                carrier_id = MedicareSupplementCarrier.objects.get(carrier_name=carrier)
            except MedicareSupplementCarrier.DoesNotExist:
                print(f"Company {carrier} does not exist in the database.")
                carrier_id = None
                time.sleep(50)

            print(f"State: {state}, Carrier: {carrier}, Color: {color}")

            # decode the color
            color = ColorKey[color]

            # Get the color object
            discount_id = HouseHoldDiscountKey.objects.get(color=color)

            print(f"State ID: {state_id}, Carrier ID: {carrier_id}, Discount ID: {discount_id}")

            # Check if an entry with the same state and company already exists
            existing_entry = HouseHoldDiscount.objects.filter(state_id=state_id, carrier_id=carrier_id).first()
            if existing_entry is None:
                # Create a new HouseHoldDiscount object

                HouseHoldDiscount.objects.get_or_create(
                    state=state_id,
                    carrier=carrier_id,
                    discount=discount_id
                )
            else:
                print(f"Entry for state {state} and company {carrier} already exists.")


class Command(BaseCommand):
    help = 'Add color mapping to the HouseHoldDiscounts model'

    def handle(self, *args, **options):
        add_color_mapping_to_model()
        return 0
