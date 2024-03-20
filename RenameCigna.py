import os


def rename_files(directory):
    for filename in os.listdir(directory):
        if "CIGNA_" in filename:
            new_filename = filename.replace("CIGNA_", "CIGNA-")
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")


# Call the function with the directory path
rename_files("C:\\Users\\Noricum\\Desktop\\WebApps\\TestingSVG\\static\\Companies\\Cigna")
