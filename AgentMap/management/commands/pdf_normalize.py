import os
import shutil

# Eventually need to expand the parameters to include the carrier name and the form_type
def rename_pdfs(directory):
    print(f"Renaming PDFs in directory: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"File: {file}")
            if file.endswith('.PDF'):
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, file[:-4] + '.pdf')
                print(f"Renaming: {old_file_path} to {new_file_path}")
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} to {new_file_path}")
                # Copy the renamed file to the static/Companies/Manhattan-Life dir
                shutil.copy(new_file_path, 'C:\\Users\\Noricum\\Desktop\\TestingSVG\\static\\Companies\\Manhattan-Life')
                print(f"Copied {new_file_path} to static/Companies/Manhattan-Life")
            elif file.endswith('.pdf'):
                # Copy the file to the static/Companies/Manhattan-Life dir
                file_path = os.path.join(root, file)
                shutil.copy(file_path, 'C:\\Users\\Noricum\\Desktop\\TestingSVG\\static\\Companies\\Manhattan-Life')
    print("Finished renaming PDFs")


# Replace 'your_directory_path' with the path to the directory containing the .PDF files
rename_pdfs('C:\\Users\\Noricum\\Desktop\\Cancer\\Manhatten-Life')