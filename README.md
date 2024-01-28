# Data Literacy Project 23-24: Impact of media-relevant conflicts on German federal elections surveys

This project investigates the correlation between media presence of international conflicts and federal election predictions in Germany. The aim is to demonstrate how the number of articles on international conflicts influences parties in the federal parliament. For this purpose, we conduct a correlation analysis and a linear regression.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)


## Installation
1. Clone the repository:
```bash
 git clone https://github.com/schokoblume/Data-Literacy.git
```

2. Install dependencies:
We used the newest Pythonversion 3.10.11
In addition to the standard Python library, you need the dependencies:

Data
```bash
pip install requests
pip install beautifulsoup4
 ```

Data Analysis
```bash
pip install scikit-learn
pip install statsmodels
pip install pandas
pip install numpy 
pip install math
pip install scipy
pip install matplotlib
pip install tueplots
```

#### Usage

In the data order is the joined_survey_article_standardized_median.csv, which is required for all analyses.
To collect and prepare the data yourself, the code is in the data order.

#### Features
To provide the Datasets for Analysis by yourself: 
Data 
1. Data collection: getArcticles.py downloads all Spiegel headlines from 2000 to 2023
2. Data preprocessed:
Final Dataset


Data Analysis
- To better understand the dataset, you can run the OverviewPlots.ipynb, which provides an overview of the entire timeframe and of the most media-relevant times.
- In CorrelationAndPermutationTest.ipynb, a correlation analysis between the survey values and the article number is implemented. Furthermore, a permutation test is used to check if the correlation is significant.
- A linear regression is implemented in RegressionPrediction.ipynb.

Exploration
- Get intuition about the most media relevant time based on article number: ArticleNumber.ipynb, ArticleNumberElectionPredictions.ipynb
- Check keywords for data collection process: CheckKeywords.ipynb
- Polynomial Regression: PolynomialRegressionPrediction.ipynb, PolynomialRegressionPredictionAllParties.ipynb
- Explore correlation and permutation tests: PermutationTest.ipynb, CorrelationAllParties.ipynb
- PCA: PCA.ipynb



