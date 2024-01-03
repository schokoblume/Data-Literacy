import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt

# Before you run this script, download articles with getArticles.py
# You could do everything in one function, but we already had the intermediate results, so we added functions to work on them

# Keywords determine if an article is about war. At least one of them has to be in the headline to count the article.
# In-word is searched, i.e. for keyword "krieg", "Angriffskrieg" is counted
keywords = ["krieg", "Krieg", "konflikt", "Konflikt", "Angriff", "angriff"]

directory = os.getcwd() + "\\spiegel_articles_ausland_politik"

# create a data frame with row for each headline: date, each keyword (present: 1, not present: 0), war: at least one keyword present (yes: 1, no: 0)
# output_file: name of output file
# keywords: list of strings
# directory: directory of files to search
# overwirte: True, if file exists it will be overwritten, False, if file exists we do not change it
def create_basic_csv(output_file, keywords, directory, overwrite=False):
    if not overwrite:
        if os.path.exists(output_file):
            print("File already exists. Change file name or enable overwrite.")

    print("Searching files...")

    # make data frame
    df = pd.DataFrame(columns=["date"])

    # go through all txt files in directory
    for file in Path(directory).glob('**/*.txt'):
        filename = os.path.basename(file).split('/')[-1]
        date = filename.replace(".txt", "")
        # print progress
        #print(date)

        # go through all headlines and check if keywords are contained
        # we used two encodings to download, so try both for reading
        lines = open(file, encoding="utf-8").readlines()
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
            print("Output file already exists. Change file name or enable overwrite.")
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
        #print(date)
        date_df = df.where(df["date"] == date)
        num_articles = date_df["war"].sum()
        # add row in new df
        new_df.loc[len(new_df)] = {"date": date, "war articles": num_articles}

    # save as csv
    new_df.to_csv(output_file, sep=";")

# create a data frame with row for each date: how many articles were about war, how many articles on that day, standardized number
# input_file: csv file created with create_accumulated_csv
# output_file: name of output file
# directory: same as in create_basic_csv
# overwirte: True, if file exists it will be overwritten, False, if file exists we do not change it
def create_standardized_csv(input_file, output_file, directory, overwrite=False):
    if not overwrite:
        if os.path.exists(output_file):
            print("Output file already exists. Change file name or enable overwrite.")
    if not os.path.exists(input_file):
        print("The specified input file does not exist.")

    base_df = pd.read_csv(input_file, sep=";")
    new_df = pd.DataFrame(columns=["date", "war articles", "total articles", "standardized"])

    # take war articles from previous df
    new_df["date"] = base_df["date"]
    new_df["war articles"] = base_df["war articles"]

    # go through files to find total article number
    for file in Path(directory).glob('**/*.txt'):
        filename = os.path.basename(file).split('/')[-1]
        date = filename.replace(".txt", "")
        # show progress
        #print(date)
        lines = open(file, encoding="utf-8").readlines()

        counter = 0
        for line in lines:
            counter += 1
        new_df.loc[new_df['date'] == date, "total articles"] = counter
        # standardize
        war_num = new_df.loc[new_df['date'] == date, "war articles"]
        new_df.loc[new_df['date'] == date, "standardized"] = war_num / counter

    # save as csv
    new_df.to_csv(output_file, sep=";")


#create_basic_csv("Spiegel_articles_keywords_ausland_poliktik.csv", keywords, directory)
#create_accumulated_csv("Spiegel_articles_keywords_ausland_politik.csv", "Spiegel_articles_accumulated_ausland_politik.csv")
#create_standardized_csv("Spiegel_articles_accumulated_ausland_politik.csv", "spiegel_articles_standardized.csv", directory)

