from bs4 import BeautifulSoup as bs
import requests
import re
from requests.exceptions import ConnectTimeout
from fake_useragent import UserAgent
from datetime import datetime
from time import sleep

def CheckStatusCodeBetaApps():
    with open(txtTestflight_List, 'r', encoding='utf-8') as txtTestflightList_file, open(txtResult_AvailableTestflight, 'w', encoding='utf-8') as txtResult_AvailableTestflight_file, open(txtResult_ErrorLinkTestflight, 'w', encoding='utf-8') as txtResult_ErrorLinkTestflight_file:
        urls = list(set(txtTestflightList_file.read().splitlines()))
        
        try:
            session = requests.Session()
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            while urls:
                url_testflight = urls.pop(0).strip()
                try:
                    r = session.get(url_testflight, headers=headers)  # Set the timeout value here
                except ConnectTimeout:
                    urls.append(url_testflight)
                    headers = {'User-Agent': user_agent.random}
                    continue
                
                if r.status_code == 429:
                    retry_after = int(r.headers.get('Retry-After', 5))  # Default to 5 seconds
                    sleep(retry_after)
                    urls.append(url_testflight)
                    
                if r.status_code == 200:
                    soup = bs(r.text, 'html.parser')
                    div_BetaStatus = soup.find('div', {'class': 'beta-status'})

                    span_BetaStatus = div_BetaStatus.find('span').text
                    isBetaAppAvaiable = re.search(r'To join the(.*) beta', span_BetaStatus)

                    style = soup.find("div", {"class": "app-icon"})["style"]
                    background_image_url = style.split("(")[1].split(")")[0]
                    if isBetaAppAvaiable:
                        name_testflight = isBetaAppAvaiable.group(1).replace('|', '-')
                        hashtag_testflights = re.findall(r"\b\w+\b", name_testflight)
                        hashtag_testflights = " ".join(["#" + hashtag.upper() for hashtag in hashtag_testflights])
                        # nameSearch = "https://www.google.com/search?q="+name_testflight.replace(" ", "+")+"+"+"appstore"
                        
                        # txtResult_AvailableTestflight_file.write(
                            # f"| <img src=\"{background_image_url}\" alt=\"{name_testflight}\" align=\"center\" width=\"40\" height=\"40\" /> | **[{name_testflight}]({nameSearch})** | {hashtag_testflights}<br />{url_testflight}\n")
                        txtResult_AvailableTestflight_file.write(
                            f"| <img src=\"{background_image_url}\" align=\"center\" width=\"40\" height=\"40\" /> | {name_testflight} | {hashtag_testflights}<br />{url_testflight}\n")
                else:
                    txtResult_ErrorLinkTestflight_file.write(f"{url_testflight}\n")
        except AttributeError:
            pass
        finally:
            session.close()

def ResultBetaAppsAvailable():
    with open(txtResult_AvailableTestflight, "r", encoding="utf-8") as txtResult_AvailableTestflight_file:
        contents = txtResult_AvailableTestflight_file.readlines()

    def extract_text_within_brackets(line):
        match = re.search(r"\[([^]]+)\]", line)
        return match.group(1) if match else ""

    contents.sort(key=lambda x: extract_text_within_brackets(x))

    with open(txtResult_AvailableTestflight, "w", encoding="utf-8") as txtResult_AvailableTestflight_file:
        txtResult_AvailableTestflight_file.write(f"# Beta Apps is available\t[{nowTime}]\n")
        txtResult_AvailableTestflight_file.write('| Image | Name | #HASHTAG |\n| --- | --- | --- | \n')
        txtResult_AvailableTestflight_file.writelines(contents)

if __name__ == "__main__":
    nowTime = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    txtTestflight_List = "Testflight_List.txt"
    txtResult_AvailableTestflight = "Result_BetaAppsAvailable.md"
    txtResult_ErrorLinkTestflight = "Result_ErrorLinkTestflight.txt"

    
    user_agent = UserAgent(browsers=['edge', 'chrome'])

    CheckStatusCodeBetaApps()
    ResultBetaAppsAvailable()