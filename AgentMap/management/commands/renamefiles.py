import os
import time
import shutil

def copy_and_rename(directory, file_to_copy, default_formtype='DDL'):
    # Ensure file_to_copy is a string representing a file path
    if not isinstance(file_to_copy, str):
        raise ValueError("file_to_copy must be a string representing a file path")

    # Get the sorted list of files in the directory
    files = sorted(os.listdir(directory))

    # Start from the second file
    for i in range(1, len(files)):
        # Get the company and state from the current and previous file
        company_state_current = '_'.join(files[i].split('_')[:2])
        company_state_previous = '_'.join(files[i-1].split('_')[:2])
        print(company_state_current, company_state_previous)

        # If the range is 1, we should copy and rename the file so we can get the first state aswell
        if i == 1:
            new_filename = f"{company_state_previous}_{default_formtype}.pdf"
            print(f"Copying {file_to_copy} to {new_filename}")
            shutil.copy(os.path.join(directory, file_to_copy), os.path.join(directory, new_filename))

        # If the states are different, copy and rename the file
        if company_state_current != company_state_previous:
            new_filename = f"{company_state_current}_{default_formtype}.pdf"
            print(f"Copying {file_to_copy} to {new_filename}")
            shutil.copy(os.path.join(directory, file_to_copy), os.path.join(directory, new_filename))

copy_and_rename('C:\\Users\\Noricum\\Desktop\\TestingSVG\\static\\Companies\\Philadelphia-American', "F:\\Carick\\New Era_Philadelphia American Declinable Drug List.pdf")