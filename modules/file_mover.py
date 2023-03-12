import os
import glob
import shutil

def format_copy_file()->None:
    # Read directories from txt file and clean them
    lines = open("download_and_end_folders.txt",'r').readlines()
    modified = []
    for line in lines:
        if line[-1] == "\n":
            modified.append(line[:-1])
        else:
            modified.append(line)

    #assign source and destination folder
    download_folder = modified[1]
    destination_folder = modified[4]

    #access download folder and retain only the financial files
    os.chdir(download_folder)
    financial_tables = []
    for file in os.listdir():
        if "financials" in file: 
            financial_tables.append(file)

    #sort financial files and create mapped pair 
    financial_tables = sorted(financial_tables)
    mapped_title = ["balance_sheet", "cash_flow", "metrics", "growth", "income"]

    #rename downloaded files
    count = 0
    for file in financial_tables:
        try:
            os.rename(file, mapped_title[count]+".xlsx")
        except FileExistsError:
            os.remove(mapped_title[count]+".xlsx")
            os.rename(file, mapped_title[count]+".xlsx")
        count += 1

    #copy all files over to destination folder
    for file in os.listdir():
        shutil.copy(file, destination_folder)

if __name__ =="__main__":
    format_copy_file()
