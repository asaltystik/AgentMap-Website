import os
import tabula
import django
import argparse
import pandas as pd

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestingSVG.settings')
django.setup()

from AgentMap.models import LicensedState, Agent


# function to parse the tables
def process_dataframe(dataframe):
    """
        This function processes a dataframe by performing several operations such as dropping columns,
        removing null rows, shifting values, and setting default values.

        Parameters:
        dataframe (pd.DataFrame): The dataframe to be processed.

        Returns:
        dataframe (pd.DataFrame): The processed dataframe.
        """

    # Drop LICENSE TYPE column
    dataframe = dataframe.drop(columns=['LICENSE TYPE'])

    # Drop Rows where everything is null
    dataframe = dataframe.dropna(how="all")

    # Remove any decimal points from the 'LICENSE NUMBER' column
    dataframe['LICENSE NUMBER'] = dataframe['LICENSE NUMBER'].astype(str).str.replace('\.\d+', '', regex=True)

    # Shift the 'LICENSE NUMBER' and 'EXPIRATION DATE' columns up by 1 maybe 2 if needed
    dataframe['LICENSE NUMBER'] = dataframe['LICENSE NUMBER'].shift(+1)
    dataframe['EXPIRATION DATE'] = dataframe['EXPIRATION DATE'].shift(+1)
    dataframe.loc[dataframe['STATE'].isna(), 'LICENSE NUMBER'] = dataframe.loc[dataframe['STATE'].isna(), 'LICENSE NUMBER'].shift(+1)
    dataframe.loc[dataframe['STATE'].isna(), 'EXPIRATION DATE'] = dataframe.loc[dataframe['STATE'].isna(), 'EXPIRATION DATE'].shift(+1)

    # Create a mask for rows where 'STATE' is more than 2 characters long
    mask = dataframe['STATE'].str.len() > 2

    # Use the mask to drop these rows
    dataframe = dataframe.loc[~mask]

    # Drop Rows where everything is null
    dataframe = dataframe.dropna(how="all")
    dataframe = dataframe.dropna(subset=['STATE'])

    # Set the 'EXPIRATION DATE' column to 05/31/2999 if it is null
    dataframe['EXPIRATION DATE'] = dataframe['EXPIRATION DATE'].fillna('05/31/2099')

    # Reset the index
    dataframe = dataframe.reset_index(drop=True)

    return dataframe


# Create an argument parser
parser = argparse.ArgumentParser(description='Parse a PDF file and save the data to a CSV file')
parser.add_argument('file', type=str, help='The PDF file to parse')

# Parse the arguments
args = parser.parse_args()

# Ask the user for the coordinates of the table
print("Enter the coordinates of the table in inches")

# Get the coordinates of the table
x1 = 1 * 72
x2 = 5.75 * 72

# Get the y coordinates of the table
while True:
    try:
        y1 = float(input("Enter the y1 coordinate: ")) * 72
        y2 = float(input("Enter the y2 coordinate: ")) * 72
        break
    except ValueError:
        print("Needs to be an integer or float")

# Read the first page of the pdf
df = tabula.read_pdf(args.file, area=[y1, x1, y2, x2], pages=1)

# process the first page
df[0] = process_dataframe(df[0])

# print the first page
print(df[0])

# Ask the user for the coordinates of the table on pages 2-4
print("Enter the coordinates of the table in inches for pages 2-4")

# Get the coordinates of the table
while True:
    try:
        y1 = float(input("Enter the y1 coordinate: ")) * 72
        y2 = float(input("Enter the y2 coordinate: ")) * 72
        break
    except ValueError:
        print("Needs to be an integer or float")

# Read all middle pages
df_following_pages = tabula.read_pdf(args.file, area=[y1, x1, y2, x2], pages="2-5")

# Process the middle pages one at a time
for i in range(len(df_following_pages)-1):
    df_following_pages[i] = process_dataframe(df_following_pages[i])

    # print the following pages
    print("Page ", i+2, ":")
    print(df_following_pages[i])

# Ask the user for the coordinates of the table on the last page
print("Enter the coordinates of the table in inches for the last page")

# Get the coordinates of the table on the last page
while True:
    try:
        y1 = float(input("Enter the y1 coordinate: ")) * 72
        y2 = float(input("Enter the y2 coordinate: ")) * 72
        break
    except ValueError:
        print("Needs to be an integer or float")

# Read the last page
df_last_page = tabula.read_pdf(args.file, area=[36, 72, 252, 414], pages=5)

# Process the last page
df_last_page[0] = process_dataframe(df_last_page[0])

# print the last page
print("Page 5:")
print(df_last_page[0])

# Combine all the dataframes into one
df = pd.concat([df[0], df_following_pages[0], df_following_pages[1],
                df_following_pages[2], df_following_pages[3], df_last_page[0]], ignore_index=True)

# Drop the License Type column
df = df.drop(columns=['LICENSE TYPE'])

# Drop rows that are NULL
df = df.dropna(subset=['LICENSE NUMBER', 'EXPIRATION DATE'])

# if there is a duplicate STATE then drop the second one
df = df.drop_duplicates(subset=['STATE'])

# Reset the index
df = df.reset_index(drop=True)

# Format the Expiration Date Column from mm/dd/yyyy to yyyy-mm-dd
df['EXPIRATION DATE'] = pd.to_datetime(df['EXPIRATION DATE'])

pd.set_option('display.max_rows', None)
# print the final dataframe
print(df)

# Ask the user if they want to manually edit the dataframe
edit = input("Do you want to manually edit the dataframe? (yes/no): ")

while edit.lower() == 'yes':
    # Ask the user for the row number to edit
    while True:
        try:
            row_number = int(input("Enter the row number to edit: "))
            break
        except ValueError:
            print("Invalid row number. Please enter an integer.")

    # Ask the user for the column to edit
    while True:
        try:
            column = input("Enter the column to edit(STATE, LICENSE NUMBER, or EXPIRATION DATE): ").upper()
            if column not in ['STATE', 'LICENSE NUMBER', 'EXPIRATION DATE']:
                raise ValueError
            break
        except ValueError:
            print("Invalid column. Please enter STATE, LICENSE NUMBER, or EXPIRATION DATE.")

    # Ask the user for the new value
    new_value = input("Enter the new value: ")

    # Update the dataframe
    df.at[row_number, column] = new_value

    # Print the updated row
    print(df.loc[row_number])

    # Ask the user if they want to edit another row
    edit = input("Do you want to edit another row? (yes/no): ")

# Save the dataframe to a csv file in Licenses folder, Ask user for the file name
file_name = input("Enter the agent name: ")
df.to_csv("static/Licenses/" + file_name + ".csv", index=False)

# Get the current user as the agent
agent = Agent.objects.get(user__username=file_name)

# Ask the user if they want to add or delete the list
action = input("Do you want to add or delete this list from the model? (add/delete): ")

# Iterate over the rows in the dataframe to add or delete the licenses
for index, row in df.iterrows():
    print(row['STATE'], row['LICENSE NUMBER'], row['EXPIRATION DATE'])
    existing_license = LicensedState.objects.filter(agent=agent, state=row['STATE'], licenseNumber=row['LICENSE NUMBER']).first()
    if existing_license is None:
        # Create a LicensedState object
        LicensedState.objects.create(
            agent=agent,
            state=row['STATE'],
            licenseNumber=row['LICENSE NUMBER'],
            expiration=pd.to_datetime(row['EXPIRATION DATE'])
        )
