import pandas as pd
import os
from pathlib import Path

# Before you run this script, download articles with getArticles.py

# Keywords determine if an article is about war. At least one of them has to be in the headline to count the article.

# create a data frame with row for each headline: date, each keyword (present: 1, not present: 0), war: at least one keyword present (yes: 1, no: 0)
# output_file: name of output file
# keywords: list of strings
# directory: directory of files to search
# overwirte: True, if file exists it will be overwritten, False, if file exists we do not change it
def create_basic_csv(output_file, keywords, directory, overwrite=False):
    if not overwrite:
        if os.path.exists(output_file):
            print("File already exists. Change file name or enable overwrite.")

    # make data frame
    df = pd.DataFrame(columns=["date"])

    # go through all txt files in directory
    for file in Path(directory).glob('**/*.txt'):
        filename = os.path.basename(file).split('/')[-1]
        date = filename.replace(".txt", "")

        # go through all headlines and check if keywords are contained
        lines = open(file).readlines()
        for line in lines:
            # create one row per headline
            index = len(df)
            df.loc[index, "date"] = date

            # check all keywords
            df.loc[index, "war"] = 0
            for keyword in keywords:
                if keyword in line:
                    df.loc[index, keyword] = 1
                    df.loc[index, "war"] = 1
                else:
                    df.loc[index, keyword] = 0

    # save df as csv file
    df.to_csv(output_file, sep=";")

# create a data frame with row for each date: how many articles were about war
# input_file: csv file created with create_basic_csv
# output_file: name of output file
# overwirte: True, if file exists it will be overwritten, False, if file exists we do not change it
def create_accumulated_csv(input_file, output_file, overwrite=False):
    if not overwrite:
        if os.path.exists(output_file):
            print("File already exists. Change file name or enable overwrite.")
    if not os.path.exists(input_file):
        print("The specified input file does not exist.")

    df = pd.read_csv(input_file, sep=";")
    new_df = pd.DataFrame(columns=["date", "war articles"])
    # remove duplicates from dates
    dates = []
    for date in df["date"]:
        if not date in dates:
            dates.append(date)
    
    # sum articles for each date
    for date in dates:
        date_df = df.where(df["date"] == date)
        num_articles = date_df["war"].sum()
        # add row in new df
        new_df.loc[len(new_df)] = {"date": date, "war articles": num_articles}

    # save as csv
    new_df.to_csv(output_file, sep=";")


#create_basic_csv("test.csv", ["test"], os.getcwd() + "\\spiegel_articles\\2000", True)
#create_accumulated_csv("test.csv", "acc_test.csv", True)