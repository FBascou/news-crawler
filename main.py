import inspect
import os 
import sys
import urllib.request
from dotenv import load_dotenv
from simple_salesforce import Salesforce
import requests
import time
from datetime import datetime


# SALESFORCE FUNCTIONS
# sf_account_list(SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_SECURITY_TOKEN)
# sf_chatter_post(final_account_news_list)

# NEWS FUNCTIONS
# get_naver_news(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, sf_filtered_account_list)
# get_google_news(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, sf_filtered_account_list)

# APP GUI
# Simple GUI with a "Start" button
# Make it an .exe file

# POTENTIAL PROBLEMS
# Duplicate news - Naver in KR, Google in EN
# Limited API queries, will have to pay eventually
# Denied access if crawling search engines very fast - Fixed NAVER with Sleep()


# Load all the ids, passwords, and tokens
load_dotenv()

# Get Id, EN Name, and KR Name from SF
SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
SALESFORCE_SECURITY_TOKEN = os.getenv("SALESFORCE_SECURITY_TOKEN")

sf = Salesforce(username=SALESFORCE_USERNAME, password=SALESFORCE_PASSWORD, security_token=SALESFORCE_SECURITY_TOKEN)
print("Login successful")
data = sf.query_all("SELECT...") # Query to get Id of startups 
data_iter = sf.query_all_iter("SELECT...") # Query to get startup names

# Pass SF Id, EN Name, and KR Name into new list
sf_unfiltered_account_list = []
for index in data_iter:
    for row in index.values():
        sf_unfiltered_account_list.append(row)

# Clean and filter new_list by removing unnecessary data (None, OrderedDict, and Account Id)
sf_filtered_account_list = [row for row in sf_unfiltered_account_list if type(row) == str and not row.startswith('0015g')]

print(f"# of Accounts: {len(sf_filtered_account_list)}")


# Get News from Naver
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# Iterate over "encText" with company list and search news
for query in sf_filtered_account_list:
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/news?query="+ encText

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()

        # Append news to .txt file. Maybe add to a list as it will have the news article as a list with dictionaries inside. 
        date = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        with open(f"{date}startup_news.txt", "a+", -1, 'utf-8') as f:
            # return 
            f.write(response_body.decode("utf-8"))
            time.sleep(1.5)
        print(query + " completed")
    else: 
        print("Error code:" + rescode)





