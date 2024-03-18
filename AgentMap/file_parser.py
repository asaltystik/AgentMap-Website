import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestingSVG.settings')  # replace 'myproject.settings' with your project's settings
django.setup()
from AgentMap.models import Form


FORM_TYPE_DICT = {
    "DVH+_APP": "Dental, Vision, Hearing Plus Application",
    "DVH+_OC": "Dental, Vision, Hearing Plus Outline ",
    "DVH+_BR": "Dental, Vision, Hearing Plus Brochure",
    "DVH_APP": "Dental, Vision, Hearing Plus Application",
    "MS_COMBO": "Medicare Supplement Combo Application",
    "MS_APP": "Medicare Supplement Application",
    "MS_BR": "Medicare Supplement Brochure",
    "OC": "Medicare Supplement Outline of Coverage",
    "BR": "Medicare Supplement Brochure",
    "HHD": "Medicare Supplement HouseHold Discount",
    "HANDBOOK": "Underwriting Handbook",
    "RP": "Medicare Supplement Replacement Form",
    "COMBO": "Medicare Supplement & DVH+ Application",
    "MS": "Medicare Supplement",
}

CompanyDict = {
    "AARP": "AARP",
    "AARP-UHICA": "AARP United HealthCare Insurance Company of America",
    "ABL": "American Benefit Life",
    "ACE": "Ace Chubb",
    "AETNA": "Aetna",
    "AFLAC": "Aflac",
    "AFS": "American Financial Security",
    "AMHL": "American Home Life",
    "BFAM": "Bankers Fidelity Atlantic American",
    "CIGNA-CHLIC": "Cigna Health and Life Insurance Company",
    "CIGNA-CNHIC": "Cigna National Health Insurance Company",
    "CIGNA-LOYAL": "Cigna Loyal American Life Insurance Company",
    "LUMICO": "Lumico",
    "ELIPS": "Elips Life Insurance Company",
    "LIFES": "LifeShield National Insurance Company",
    "NEWERA": "New Era",
    "MAN": "Manhattan Life",
    "MEDICO": "Medico",
    "MOO": "Mutual of Omaha",
    "PHILAM": "Philadelphia American Life Insurance Company",
    "WPS": "WPS Health Insurance"
}


def parse_filenames(directory):
    total = 0
    # Walk through the directory and get the filenames
    for root, dirs, files in os.walk(directory):
        total = total + len(files)
        for file in files:
            print(file)
            if file.endswith('.pdf'):
                parts = file.split('_', 2)  # Split the filename at the first underscore
                print("Parts: ", parts)
                if len(parts) == 3:
                    company, state, form_type = parts
                    form_type = form_type.replace('.pdf', '')  # Remove the file extension from the form type
                    # If the form_type has an - in it, split it at the - and take the first part for the form_type and
                    # the second part for the date
                    if '-' in form_type:
                        form_type, date = form_type.split('-')
                        print(f"Form Type: {form_type}, Date: {date}")
                    else:
                        date = "None"
                    file_path = os.path.join(root, file)
                    # print(f"Company: {company}, State: {state}, Form Type: {form_type}, File Path: {file_path}")
                    file_path = os.path.relpath(file_path, 'C:\\Users\\Noricum\\Desktop\\WebApps\\TestingSVG\\static\\Companies')
                    file_path = file_path.replace('\\', '/')
                    # print("relative path: ", file_path)
                    full_form_type = FORM_TYPE_DICT[form_type] if form_type in FORM_TYPE_DICT else "N"
                    form, created = Form.objects.get_or_create(
                        company=company,
                        full_company=CompanyDict[company],
                        state=state,
                        form_type=form_type,
                        full_form_type=full_form_type,
                        date=date,
                        file_path=file_path
                    )
                    if created:
                        print(f"Saved {form}")
                    else:
                        print(f"Skipping {form} because it already exists")
                else:
                    print(f"Skipping {file} because it doesn't have enough parts")
                    print(len(parts))
    print(f"Total files: {total}")
    print(f"Total forms Parsed: {Form.objects.count()}")


parse_filenames('C:\\Users\\Noricum\\Desktop\\WebApps\\TestingSVG\\static\\Companies')
