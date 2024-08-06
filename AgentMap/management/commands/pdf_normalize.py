import os

def rename_pdfs(directory):
    print(f"Renaming PDFs in directory: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.PDF'):
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, file[:-4] + '.pdf')
                print(f"Renaming: {old_file_path} to {new_file_path}")
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} to {new_file_path}")


# Replace 'your_directory_path' with the path to the directory containing the .PDF files
rename_pdfs('C:\\Users\\Noricum\\Desktop\\TestingSVG\\static\\Companies\\Manhattan-Life')