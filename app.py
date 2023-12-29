import json
import requests
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent

# Setting up Chrome options
op = webdriver.ChromeOptions()
op.add_argument(f"user-agent={UserAgent.random}")
op.add_argument("user-data-dir=./")
op.add_experimental_option("detach", True)
op.add_experimental_option("excludeSwitches", ["enable-logging"])

# Initializing the Chrome driver
driver = uc.Chrome(chrome_options=op)

def platform_ai_login(MAIL, PASSWORD):
    """
    Logs into the OpenAI platform using the provided credentials.
    """
    driver.get('https://platform.openai.com/usage')
    time.sleep(5)
    inputElements = driver.find_elements(By.TAG_NAME, "button")
    inputElements[0].click()
    time.sleep(3)
    mail = driver.find_elements(By.TAG_NAME,"input")[1]
    mail.send_keys(MAIL)
    btn = driver.find_elements(By.TAG_NAME,"button")[0]
    btn.click()
    password = driver.find_elements(By.TAG_NAME,"input")[2]
    password.send_keys(PASSWORD)
    btn = driver.find_elements(By.TAG_NAME,"button")[2]
    btn.click()
    time.sleep(5)

def get_sensitive_id(access_token):
    """
    Retrieves sensitive_id using the given access token.
    """
    url = 'https://api.openai.com/dashboard/onboarding/login'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json() 
        else:
            return f'Error: {response.status_code}, Message: {response.text}'
    except Exception as e:
        return f'An error occurred: {str(e)}'
    
def get_activity_data(sensitive_id, start_date, end_date):
    """
    Retrieves activity data for the given date range using the sensitive_id.
    """
    url = f'https://api.openai.com/v1/dashboard/activity?end_date={end_date}&start_date={start_date}'
    headers = {'Authorization': f'Bearer {sensitive_id}'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Error: {response.status_code}, Message: {response.text}'
    except Exception as e:
        return f'An error occurred: {str(e)}'
    
def get_start_and_end_dates():
    """
    Returns the first day of the current month and the first day of the next month.
    """
    now = datetime.datetime.now()
    start_year, start_month = now.year, now.month
    end_year = start_year + 1 if start_month == 12 else start_year
    end_month = 1 if start_month == 12 else start_month + 1
    start_date = datetime.datetime(start_year, start_month, 1)
    end_date = datetime.datetime(end_year, end_month, 1)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

# Logging into the platform
platform_ai_login("EMAIL", "PASSWORD")

# Fetching data from localStorage
local_storage_data = driver.execute_script("return window.localStorage;")
json_data = local_storage_data['@@auth0spajs@@::DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD::https://api.openai.com/v1::openid profile email offline_access']
parsed_data = json.loads(json_data)

# Accessing the access_token
access_token = parsed_data['body']['access_token']

# Getting the sensitive_id
result = get_sensitive_id(access_token)
sensitive_id = result['user']['session']['sensitive_id']

# Getting the start and end dates
start_date, end_date = get_start_and_end_dates()

# Getting activity data
result = get_activity_data(sensitive_id, start_date, end_date)
print(result)

# Closing the driver
driver.close()