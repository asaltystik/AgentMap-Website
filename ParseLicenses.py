import os
import tabula
import django
import pandas as pd
# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestingSVG.settings')
django.setup()

from AgentMap.models import LicensedState, Agent

file = "C:\\Users\\Noricum\\Downloads\\Licenses Sircon Platform.pdf"

df = tabula.read_pdf(file, area=[194.4, 72, 756, 414], pages=1)

# Drop LICENSE TYPE column
df[0] = df[0].drop(columns=['LICENSE TYPE'])

# Drop Rows where everything is null
df[0] = df[0].dropna(how="all")

# Remove any decimal points from the 'LICENSE NUMBER' column
df[0]['LICENSE NUMBER'] = df[0]['LICENSE NUMBER'].astype(str).str.replace('\.\d+', '', regex=True)

# Shift the 'LICENSE NUMBER' and 'EXPIRATION DATE' columns up by 1 maybe 2 if needed
df[0]['LICENSE NUMBER'] = df[0]['LICENSE NUMBER'].shift(+1)
df[0]['EXPIRATION DATE'] = df[0]['EXPIRATION DATE'].shift(+1)
df[0].loc[df[0]['STATE'].isna(), 'LICENSE NUMBER'] = df[0].loc[df[0]['STATE'].isna(), 'LICENSE NUMBER'].shift(+1)
df[0].loc[df[0]['STATE'].isna(), 'EXPIRATION DATE'] = df[0].loc[df[0]['STATE'].isna(), 'EXPIRATION DATE'].shift(+1)

# Create a mask for rows where 'STATE' is more than 2 characters long
mask = df[0]['STATE'].str.len() > 2

# Use the mask to drop these rows
df[0] = df[0].loc[~mask]

# Drop Rows where everything is null
df[0] = df[0].dropna(how="all")
df[0] = df[0].dropna(subset=['STATE'])

# Set the 'EXPIRATION DATE' column to 05/31/2999 if it is null
df[0]['EXPIRATION DATE'] = df[0]['EXPIRATION DATE'].fillna('1/1/2099')

# Reset the index
df[0] = df[0].reset_index(drop=True)

# print the first page
print(df[0])

df_following_pages = tabula.read_pdf(file, area=[36, 72, 738, 414], pages="2-5")
for i in range(len(df_following_pages)-1):
    # Drop LICENSE TYPE column
    df_following_pages[i] = df_following_pages[i].drop(columns=['LICENSE TYPE'])

    # Drop Rows where everything is null
    df_following_pages[i] = df_following_pages[i].dropna(how="all")

    # Remove any decimal points from the 'LICENSE NUMBER' column
    df_following_pages[i]['LICENSE NUMBER'] = df_following_pages[i]['LICENSE NUMBER'].astype(str).str.replace('\.\d+', '', regex=True)

    # Shift the 'LICENSE NUMBER' and 'EXPIRATION DATE' columns up by 1 maybe 2 if needed
    df_following_pages[i]['LICENSE NUMBER'] = df_following_pages[i]['LICENSE NUMBER'].shift(+1)
    df_following_pages[i]['EXPIRATION DATE'] = df_following_pages[i]['EXPIRATION DATE'].shift(+1)
    df_following_pages[i].loc[df_following_pages[i]['STATE'].isna(), 'LICENSE NUMBER'] = df_following_pages[i].loc[df_following_pages[i]['STATE'].isna(), 'LICENSE NUMBER'].shift(+1)
    df_following_pages[i].loc[df_following_pages[i]['STATE'].isna(), 'EXPIRATION DATE'] = df_following_pages[i].loc[df_following_pages[i]['STATE'].isna(), 'EXPIRATION DATE'].shift(+1)

    # Create a mask for rows where 'STATE' is more than 2 characters long
    mask = df_following_pages[i]['STATE'].str.len() > 2

    # Use the mask to drop these rows
    df_following_pages[i] = df_following_pages[i].loc[~mask]

    # Drop Rows where everything is null
    df_following_pages[i] = df_following_pages[i].dropna(how="all")
    df_following_pages[i] = df_following_pages[i].dropna(subset=['STATE'])

    # Set the 'EXPIRATION DATE' column to 05/31/2999 if it is null
    df_following_pages[i]['EXPIRATION DATE'] = df_following_pages[i]['EXPIRATION DATE'].fillna('05/31/2099')

    # Reset the index
    df_following_pages[i] = df_following_pages[i].reset_index(drop=True)

    # print the following pages
    print("Page ", i+2, ":")
    print(df_following_pages[i])

df_last_page = tabula.read_pdf(file, area=[36, 72, 252, 414], pages=5)

# Drop LICENSE TYPE column
df_last_page[0] = df_last_page[0].drop(columns=['LICENSE TYPE'])

# Drop Rows where everything is null
df_last_page[0] = df_last_page[0].dropna(how="all")

# Remove any decimal points from the 'LICENSE NUMBER' column
df_last_page[0]['LICENSE NUMBER'] = df_last_page[0]['LICENSE NUMBER'].astype(str).str.replace('\.\d+', '', regex=True)

# Shift the 'LICENSE NUMBER' and 'EXPIRATION DATE' columns up by 1 maybe 2 if needed
df_last_page[0]['LICENSE NUMBER'] = df_last_page[0]['LICENSE NUMBER'].shift(+1)
df_last_page[0]['EXPIRATION DATE'] = df_last_page[0]['EXPIRATION DATE'].shift(+1)
df_last_page[0].loc[df_last_page[0]['STATE'].isna(), 'LICENSE NUMBER'] = df_last_page[0].loc[df_last_page[0]['STATE'].isna(), 'LICENSE NUMBER'].shift(+1)
df_last_page[0].loc[df_last_page[0]['STATE'].isna(), 'EXPIRATION DATE'] = df_last_page[0].loc[df_last_page[0]['STATE'].isna(), 'EXPIRATION DATE'].shift(+1)

# Create a mask for rows where 'STATE' is more than 2 characters long
mask = df_last_page[0]['STATE'].str.len() > 2

# Use the mask to drop these rows
df_last_page[0] = df_last_page[0].loc[~mask]

# Drop Rows where everything is null
df_last_page[0] = df_last_page[0].dropna(how="all")
df_last_page[0] = df_last_page[0].dropna(subset=['STATE'])

# Set the 'EXPIRATION DATE' column to 05/31/2999 if it is null
df_last_page[0]['EXPIRATION DATE'] = df_last_page[0]['EXPIRATION DATE'].fillna('05/31/2099')

# Reset the index
df_last_page[0] = df_last_page[0].reset_index(drop=True)

# print the last page
# print("Page 5:")
# print(df_last_page[0])

# Combine all the dataframes into one
df = pd.concat([df[0], df_following_pages[0], df_following_pages[1], df_following_pages[2], df_following_pages[3], df_last_page[0]], ignore_index=True)

# Drop the License Type column
df = df.drop(columns=['LICENSE TYPE'])

# Drop License Nmber and Expiration date rows that are null
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

# Save the dataframe to a csv file in Licenses folder, Ask user for the file name
file_name = input("Enter the file name: ")
df.to_csv("static/Licenses/" + file_name + ".csv", index=False)

agent = Agent.objects.get(user__username=file_name)

# Ask the user if they want to add or delete the list
action = input("Do you want to add or delete this list from the model? (add/delete): ")

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
