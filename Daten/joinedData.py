import datetime
import pandas as pd
import os
import numpy as np

# join survey values and standardized war article number in one csv
# problem: they have different times, survey only every couple weeks
# timeframe: how many days previous to survey should be used

def join_data(survey_input, article_input, output_file, timeframe, overwrite = False):
	if not overwrite:
		if os.path.exists(output_file):
			print("Output file already exists. Change file name or enable overwrite.")
	if not os.path.exists(survey_input):
		print("The specified survey input file does not exist.")
	if not os.path.exists(article_input):
		print("The specified article input file does not exist.")

	survey_df = pd.read_csv(survey_input, sep=";", encoding="latin1")
	article_df = pd.read_csv(article_input, sep=";")
	survey_df["standardized_war_articles"] = 0

	for date_str in survey_df["date"]:
		date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
		counter = timeframe
		war_num = 0
		# sum up standardized war article number for days defined by timeframe before the publish date of survey
		while(counter > 0):
			counter -= 1
			# do not include publish date of survey
			date -= datetime.timedelta(days=1)
			date_index = date.strftime('%d') + "." + date.strftime('%m') + "." + date.strftime('%Y')
			war_this_date = article_df.loc[article_df["date"] == date_index, "standardized"].item()
			war_num += war_this_date

		survey_df.loc[survey_df["date"] == date_str, "standardized_war_articles"] = war_num / timeframe

	# save as csv
	survey_df.to_csv(output_file, sep=";")

# use median lenght between surveys as timeframe
def median_lenght(survey_input):
	survey_df = pd.read_csv(survey_input, sep=";", encoding="latin1")
	diffs = []
	prev_date = None
	for date_str in survey_df["date"]:
		print(date_str)
		date_now = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
		if not prev_date == None:
			difference = prev_date - date_now
			diffs.append(difference.days)
		prev_date = date_now

	return np.median(diffs)

join_data("survey_values.csv", "spiegel_articles_standardized.csv", "joined_survey_article_standardized_median.csv", median_lenght("survey_values.csv"), True)
join_data("survey_values.csv", "spiegel_articles_standardized.csv", "joined_survey_article_standardized_oneweek.csv", 7, True)
join_data("survey_values.csv", "spiegel_articles_standardized.csv", "joined_survey_article_standardized_twoweeks.csv", 14, True)