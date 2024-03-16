from time import sleep
import requests
import re
from fake_useragent import UserAgent
from requests.exceptions import ConnectTimeout
from requests.adapters import HTTPAdapter
from random import choice
from lxml import html


# Constants
URL_PROXIES = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=json"
TXT_RESULT_NEWTESTERS_BETA_APPS = "Result_Testflight_NewTesters_BetaApps.md"
TXT_RESULT_ERROR_BETA_APPS =        "Result_Testflight_Error_BetaApps.md"

TOKEN_REMINDSLOW_ID = ''
BASE_URL_REMINDSLOW = f""
GROUP_TESTFLIGHT_CAMPINGAPPS_ID = '-'

XPATH_STATUS = '//*[@class="beta-status"]/span/text()'
XPATH_TITLE = '/html/head/title/text()'
TITLE_REGEX = r'Join the (.+) beta - TestFlight - Apple'
FULL_TEXTS = ['This beta is full.',
              "This beta isn't accepting any new testers right now."]
MAX_RETRIES = 3

def ListProxies():
    list_proxies = []
    response = requests.get(URL_PROXIES)
    proxy_data = response.json().get('proxies', [])  # Use get() with a default value of an empty list
    if response.status_code == 200:
        listCountry = ['VN']
        for proxies in proxy_data:
            ip_data = proxies.get('ip_data', {})  # Use get() to handle missing 'ip_data' key
            countryCode = ip_data.get('countryCode')
            if countryCode in listCountry:
                list_proxies.append((proxies['protocol'], proxies['proxy']))
    return list_proxies

def fetch_beta_apps_info(data_proxy):
    with open(TXT_RESULT_NEWTESTERS_BETA_APPS, 'r', encoding='utf-8') as txt_result_newtesters_testflight_file, \
        open(TXT_RESULT_ERROR_BETA_APPS, 'w', encoding='utf-8') as txt_result_error_link_testflight_file:
        urls = list(set(txt_result_newtesters_testflight_file.read().split()))
        user_agent = UserAgent()
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=MAX_RETRIES)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers = {'User-Agent': user_agent.random}
        protocol, proxy = choice(data_proxy)
        
        try:
            while urls:
                url_testflight = urls.pop(0).strip()
                try:
                    r = session.get(url_testflight, headers=headers, proxies={protocol: proxy})
                except (ConnectTimeout, ConnectionError) as e:
                    urls.append(url_testflight)
                    headers = {'User-Agent': user_agent.random}
                    protocol, proxy = choice(data_proxy)
                    continue
                if r.status_code == 429:
                    urls.append(url_testflight)
                    headers = {'User-Agent': user_agent.random}
                    protocol, proxy = choice(data_proxy)
                    retry_after = int(r.headers.get('Retry-After', MAX_RETRIES))
                    sleep(retry_after)
                    continue
                
                if r.status_code == 200:
                    page = html.fromstring(r.text)
                    free_slots = page.xpath(XPATH_STATUS)[0] not in FULL_TEXTS
                    
                    if free_slots:
                        title = re.findall(
                                TITLE_REGEX,
                                page.xpath(XPATH_TITLE)[0])[0]
                        textname_between_tothe_and_beta = title.strip()
                        hashtags = re.findall(r"\b\w+\b", textname_between_tothe_and_beta)
                        hashtag = " ".join(["#" + hashtag.upper() for hashtag in hashtags])
                        parameter = {
                                        "chat_id": GROUP_TESTFLIGHT_CAMPINGAPPS_ID,
                                        "text": f"{hashtag}\n\n{url_testflight}\nOpening for New Testers"
                                    }
                        requests.post(BASE_URL_REMINDSLOW, data=parameter)
                        txt_result_error_link_testflight_file.write(f"{url_testflight}\n")
                else:
                    txt_result_error_link_testflight_file.write(f"{url_testflight}\n")
        except (ConnectTimeout, TimeoutError, OSError) as e:
            print(f"Connection error: {e}")
            headers = {'User-Agent': user_agent.random}
            protocol, proxy = choice(data_proxy)
            urls.append(url_testflight)
            pass
        finally:
            session.close()

def update_testflight_list():
    with open(TXT_RESULT_NEWTESTERS_BETA_APPS, 'r', encoding='utf-8') as f1, open(TXT_RESULT_ERROR_BETA_APPS, 'r', encoding='utf-8') as f2:
        lines_f1 = f1.read().splitlines()
        lines_f2 = f2.read().splitlines()
    unique_lines_f1 = list(set(lines_f1))
    updated_lines_f1 = [line for line in unique_lines_f1 if line not in lines_f2]
    
    with open(TXT_RESULT_NEWTESTERS_BETA_APPS, 'w', encoding='utf-8') as f1:
        f1.write('\n'.join(updated_lines_f1))

if __name__ == "__main__":
    data_proxy = ListProxies()
    fetch_beta_apps_info(data_proxy)
    update_testflight_list()