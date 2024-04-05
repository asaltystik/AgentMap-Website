import os
import django
from AgentMap.models import Form


# replace 'myproject.settings' with your project's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestingSVG.settings')
django.setup()


# Dictionary to map the form type abbreviation to the full form type
FORM_TYPE_DICT = {
    "DVH+_APP": "Dental, Vision, Hearing Plus Application",
    "DVH+_OC": "Dental, Vision, Hearing Plus Outline ",
    "DVH+_BR": "Dental, Vision, Hearing Plus Brochure",
    "DVH_APP": "Dental, Vision, Hearing Plus Application",
    "MS_COMBO": "Medicare Supplement Combo App",
    "MS_APP": "Medicare Supplement Application",
    "MS_BR": "Medicare Supplement Brochure",
    "OC": "Medicare Supplement Coverage Outline",
    "BR": "Medicare Supplement Brochure",
    "HHD": "Medi Supp HouseHold Discount",
    "HANDBOOK": "Underwriting  Guidelines Handbook",
    "RP": "Medi Supp Replacement Form",
    "COMBO": "Medicare Supplement & DVH+ App",
    "MS": "Medicare Supplement",
}

# Dictionary to map the company abbreviation to the full company name
CompanyDict = {
    "AARP": "AARP",
    "AARP-UHICA": "AARP United HealthCare Insurance",
    "ABL": "American Benefit Life",
    "ACE": "Ace Chubb",
    "AETNA": "Aetna",
    "AFLAC": "Aflac",
    "AFS": "American Financial Security",
    "AMHL": "American Home Life",
    "BFAM": "Bankers Fidelity Atlantic American",
    "CIGNA-CHLIC": "Cigna Health and Life Insurance",
    "CIGNA-CNHIC": "Cigna National Health Insurance",
    "CIGNA-LOYAL": "Cigna Loyal American Life Insurance",
    "LUMICO": "Lumico",
    "ELIPS": "Elips Life Insurance",
    "LIFES": "LifeShield National Insurance",
    "NEWERA": "New Era",
    "MAN": "Manhattan Life",
    "MEDICO": "Medico",
    "MOO": "Mutual of Omaha",
    "PHILAM": "Philadelphia American Life Insurance",
    "WPS": "WPS Health Insurance"
}


# Function to parse the filenames in the given directory
def parse_filenames(directory):
    total = 0
    # Walk through the directory and get the filenames
    for root, dirs, files in os.walk(directory):
        total = total + len(files)  # Get the total number of files
        for file in files:  # iterate over the files
            print(file)
            if file.endswith('.pdf'):  # Check if the file is a pdf file
                parts = file.split('_', 2)  # Split the filename at the first underscore
                print("Parts: ", parts)  # Print the parts of the filename
                if len(parts) == 3:  # if we have 3 parts we smovin
                    company, state, form_type = parts  # Get the company, state, and form type
                    form_type = form_type.replace('.pdf', '')  # Remove the file extension from the form type
                    # If the form_type has an - in it, split it at the - and take the first part for the form_type and
                    # the second part for the date
                    if '-' in form_type:  # Edge case for form types that include a date
                        form_type, date = form_type.split('-')
                        print(f"Form Type: {form_type}, Date: {date}")
                    else:
                        date = "None"

                    # get the file path of the pdf file
                    file_path = os.path.join(root, file)
                    # print(f"Company: {company}, State: {state}, Form Type: {form_type}, File Path: {file_path}")

                    # Get the relative path of the file
                    file_path = os.path.relpath(file_path, 'C:\\Users\\Noricum\\Desktop\\WebApps\\TestingSVG\\static\\Companies')
                    file_path = file_path.replace('\\', '/')  # replace backslashes with forward slashes
                    # print("relative path: ", file_path)

                    # Get the full form type from the FORM_TYPE_DICT
                    full_form_type = FORM_TYPE_DICT[form_type] if form_type in FORM_TYPE_DICT else "N"

                    # Create a form object with the parsed data
                    form, created = Form.objects.get_or_create(
                        company=company,  # Get the company name
                        full_company=CompanyDict[company],  # Get the full company name
                        state=state,  # Get the state abbreviation
                        form_type=form_type,  # get the form type abbreviation
                        full_form_type=full_form_type,  # get the full form type
                        date=date,  # Get the date
                        file_path=file_path  # Get the file path
                    )

                    # Check if the form was created or not
                    if created:
                        print(f"Saved {form}")
                    else:
                        print(f"Skipping {form} because it already exists")
                else:
                    print(f"Skipping {file} because it doesn't have enough parts")
                    print(len(parts))
    print(f"Total files: {total}")
    print(f"Total forms Parsed: {Form.objects.count()}")


# Call the parse_filenames function with the directory path
parse_filenames('C:\\Users\\Noricum\\Desktop\\WebApps\\TestingSVG\\static\\Companies')
