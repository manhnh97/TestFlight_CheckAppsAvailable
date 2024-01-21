from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import re
from requests.exceptions import ConnectTimeout
from fake_useragent import UserAgent
from datetime import datetime

def fetch_beta_apps_info():
    with open("Testflight_List.txt", 'r', encoding='utf-8') as txt_testflight_list_file,\
            open("Result_BetaAppsAvailable.md", 'w', encoding='utf-8') as txt_result_available_testflight_file,\
            open("Result_ErrorLinkTestflight.txt", 'w', encoding='utf-8') as txt_result_error_link_testflight_file:
        
        try:
            user_agent = UserAgent()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '}
            
            session = requests.Session()
            
            urls = list(set(txt_testflight_list_file.read().split()))
            
            while urls:
                url_testflight = urls.pop(0).strip()

                try:
                    r = session.get(url_testflight, headers=headers)
                except ConnectTimeout:
                    urls.append(url_testflight)
                    headers = {'User-Agent': user_agent.random}
                    continue
                
                if r.status_code == 429:
                    retry_after = int(r.headers.get('Retry-After', 3))
                    sleep(retry_after)
                    urls.append(url_testflight)
                    
                if r.status_code == 200:
                    soup_text = bs(r.text, 'html.parser').get_text()
                    
                    text_matches = re.search(r'To join the\s(.*?)\sbeta', soup_text, re.IGNORECASE)
                    if text_matches:
                        textname_between_tothe_and_beta = text_matches.group(1).strip()
                        name = ''.join(textname_between_tothe_and_beta).replace('|', '-')
                        hashtags = re.findall(r"\b\w+\b", name)
                        hashtag = " ".join(["#" + hashtag.upper() for hashtag in hashtags])
                        txt_result_available_testflight_file.write(f"| **{name.strip()}** | {hashtag}<br />{url_testflight} |\n")
                else:
                    txt_result_error_link_testflight_file.write(f"{url_testflight}\n")
        except AttributeError:
            pass
        finally:
            session.close()

def sort_and_update_results():
    with open("Result_BetaAppsAvailable.md", "r", encoding="utf-8") as txt_result_available_testflight_file:
        contents = txt_result_available_testflight_file.readlines()

    def extract_text_within_brackets(line):
        match = re.search(r"\*\*(.*?)\*\*", line)
        return match.group(1) if match else ""

    contents.sort(key=lambda x: extract_text_within_brackets(x))

    with open("Result_BetaAppsAvailable.md", "w", encoding="utf-8") as txt_result_available_testflight_file:
        txt_result_available_testflight_file.write(f"# Beta Apps are available\t[{datetime.now().strftime('%d/%m/%Y %I:%M %p')}]\n")
        txt_result_available_testflight_file.write('| Name | #HASHTAG |\n| --- | --- | \n')
        txt_result_available_testflight_file.writelines(contents)

def update_testflight_list():
    with open("Testflight_List.txt", 'r') as f1, open("Result_ErrorLinkTestflight.txt", 'r') as f2:
        lines_f1 = f1.read().splitlines()
        lines_f2 = f2.read().splitlines()

    unique_lines_f1 = list(set(lines_f1))
    updated_lines_f1 = [line for line in unique_lines_f1 if line not in lines_f2]

    with open("Testflight_List.txt", 'w') as f1:
        f1.write('\n'.join(updated_lines_f1))

if __name__ == "__main__":
    fetch_beta_apps_info()
    sort_and_update_results()
    update_testflight_list()
