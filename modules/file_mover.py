import os
import glob
import shutil

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def format_copy_file() -> None:
    # Read directories from txt file and clean them
    lines = open(f"{file_path}\download_and_end_folders.txt", "r").readlines()
    modified = []
    for line in lines:
        if line[-1] == "\n":
            modified.append(line[:-1])
        else:
            modified.append(line)

    # assign source and destination folder
    download_folder = modified[1]
    destination_folder = modified[4]

    # access download folder and retain only the financial files
    os.chdir(download_folder)

    financial_tables = []
    for file in os.listdir():
        if "financials_export" in file:
            financial_tables.append(file)

    # sort financial files and create mapped pair
    financial_tables = sorted(financial_tables)
    mapped_title = "full_data"

    # rename downloaded files
    for file in financial_tables:
        try:
            os.rename(file, mapped_title + ".xlsx")
        except FileExistsError:
            os.remove(mapped_title + ".xlsx")
            os.rename(file, mapped_title + ".xlsx")

    # copy all files over to destination folder
    for file in os.listdir():
        shutil.copy(file, destination_folder)


if __name__ == "__main__":
    format_copy_file()
