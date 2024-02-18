from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import re
from requests.exceptions import ConnectTimeout
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from datetime import datetime
from random import choice

# Constants
URL_PROXIES = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=json"
TXT_TESTFLIGHT_LIST =               "Testflight_List.txt"
TXT_RESULT_AVAILABLE_BETA_APPS =    "Result_Available_BetaApps.md"
TXT_RESULT_FULL_BETA_APPS =         "Result_Full_BetaApps.md"
TXT_RESULT_ERROR_BETA_APPS =        "Result_Error_BetaApps.md"
MAX_RETRIES = 3

def ListProxies():
    list_proxies = []
    response = requests.get(URL_PROXIES)
    proxy_data = response.json().get('proxies', [])  # Use get() with a default value of an empty list
    if response.status_code == 200:
        listCountry = ['VN', 'US']
        for proxies in proxy_data:
            ip_data = proxies.get('ip_data', {})  # Use get() to handle missing 'ip_data' key
            countryCode = ip_data.get('countryCode')
            if countryCode in listCountry:
                # print(f"{countryCode}:: {proxies['protocol']}: {proxies['proxy']}")
                list_proxies.append((proxies['protocol'], proxies['proxy']))
    return list_proxies

def fetch_beta_apps_info(data_proxy):
    with open(TXT_TESTFLIGHT_LIST, 'r', encoding='utf-8') as txt_testflight_list_file,\
            open(TXT_RESULT_AVAILABLE_BETA_APPS, 'w', encoding='utf-8') as txt_result_available_testflight_file,\
            open(TXT_RESULT_FULL_BETA_APPS, 'w', encoding='utf-8') as txt_result_full_testflight_file,\
            open(TXT_RESULT_ERROR_BETA_APPS, 'w', encoding='utf-8') as txt_result_error_link_testflight_file:
        urls = list(set(txt_testflight_list_file.read().split()))
        user_agent = UserAgent()
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=MAX_RETRIES)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers = {'User-Agent': user_agent.random}
        protocol, proxy = choice(data_proxy)
    
        pattern_Available = r'To join the\s(.*?)\sbeta'
        pattern_Full = r'Join the\s(.*?)\sbeta'
        try:
            while urls:
                url_testflight = urls.pop(0).strip()
                try:
                    r = session.get(url_testflight, headers=headers, proxies={protocol: proxy})
                except ConnectTimeout:
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
                    soup_text = bs(r.text, 'html.parser')
                    beta_status_element = soup_text.find(class_='beta-status')
                    first_span = beta_status_element.find('span')
                    span_text = first_span.get_text(strip=True)
                    
                    text_matches = re.search(pattern_Available, span_text, re.IGNORECASE)
                    if text_matches:
                        textname_between_tothe_and_beta = text_matches.group(1).strip()
                        name = ''.join(textname_between_tothe_and_beta).replace('|', '-')
                        hashtags = re.findall(r"\b\w+\b", name)
                        hashtag = " ".join(["#" + hashtag.upper() for hashtag in hashtags])
                        txt_result_available_testflight_file.write(f"| **{name.strip()}** | {hashtag}<br />{url_testflight} |\n")
                    elif "This beta is full." == span_text:
                        title_text = soup_text.find('title').getText()
                        text_matches = re.search(pattern_Full, title_text, re.IGNORECASE)
                        textname_between_join_and_beta = text_matches.group(1).strip()
                        txt_result_full_testflight_file.write(f"{textname_between_join_and_beta} => {url_testflight}\n")
                    else:
                        txt_result_error_link_testflight_file.write(f"{url_testflight}\n")
                else:
                    txt_result_error_link_testflight_file.write(f"{url_testflight}\n")
        except (ConnectTimeout, TimeoutError, OSError) as e:
            print(f"Connection error: {e}")
            headers = {'User-Agent': user_agent.random}
            protocol, proxy = choice(data_proxy)
            urls.append(url_testflight)
        finally:
            r.close()
            session.close()
        
def sort_and_update_results():
    with open(TXT_RESULT_AVAILABLE_BETA_APPS, "r", encoding="utf-8") as txt_result_available_testflight_file:
        contents = txt_result_available_testflight_file.readlines()

    def extract_text_within_brackets(line):
        match = re.search(r"\*\*(.*?)\*\*", line)
        return match.group(1) if match else ""

    contents.sort(key=lambda x: extract_text_within_brackets(x))

    with open(TXT_RESULT_AVAILABLE_BETA_APPS, "w", encoding="utf-8") as txt_result_available_testflight_file:
        txt_result_available_testflight_file.write(f"# Beta Apps are available\t[{datetime.now().strftime('%d/%m/%Y %I:%M %p')}]\n")
        txt_result_available_testflight_file.write('| Name | #HASHTAG |\n| --- | --- | \n')
        txt_result_available_testflight_file.writelines(contents)

def update_testflight_list():
    with open(TXT_TESTFLIGHT_LIST, 'r', encoding='utf-8') as f1, open(TXT_RESULT_ERROR_BETA_APPS, 'r', encoding='utf-8') as f2:
        lines_f1 = f1.read().splitlines()
        lines_f2 = f2.read().splitlines()

    unique_lines_f1 = list(set(lines_f1))
    updated_lines_f1 = [line for line in unique_lines_f1 if line not in lines_f2]

    with open(TXT_TESTFLIGHT_LIST, 'w', encoding='utf-8') as f1:
        f1.write('\n'.join(updated_lines_f1))

if __name__ == "__main__":
    data_proxy = ListProxies()
    fetch_beta_apps_info(data_proxy)
    sort_and_update_results()
    update_testflight_list()