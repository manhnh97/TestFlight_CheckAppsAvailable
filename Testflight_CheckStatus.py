from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime
from requests.exceptions import ConnectTimeout

def CheckStatusCodeBetaApps():
    with open(txtTestflight_List, 'r', encoding='utf-8') as txtTestflightList_file, open(txtResult_AvailableTestflight, 'w', encoding='utf-8') as txtResult_AvailableTestflight_file, open(txtResult_ErrorLinkTestflight, 'w', encoding='utf-8') as txtResult_ErrorLinkTestflight_file:
        urls = list(set(txtTestflightList_file.read().splitlines()))
        
        try:
            session = requests.Session()
            while urls:
                url_testflight = urls.pop(0).strip()
                try:
                    r = session.get(url_testflight, timeout=5)  # Set the timeout value here
                except ConnectTimeout:
                    print(f"Timeout: {url_testflight}. Retrying...")
                    urls.append(url_testflight)
                    continue
                
                if r.status_code == 200:
                    soup = bs(r.text, 'html.parser')
                    div_BetaStatus = soup.find('div', {'class': 'beta-status'})

                    span_BetaStatus = div_BetaStatus.find('span').text
                    isBetaAppAvaiable = re.search(r'To join the(.*) beta', span_BetaStatus)

                    style = soup.find("div", {"class": "app-icon"})["style"]
                    background_image_url = style.split("(")[1].split(")")[0]
                    if isBetaAppAvaiable:
                        name_testfight = isBetaAppAvaiable.group(1).replace('|', '-')
                        hashtag_testflights = re.findall(r"\b\w+\b", name_testfight)
                        hashtag_testflights = " ".join(["#" + hashtag.upper() for hashtag in hashtag_testflights])
                        txtResult_AvailableTestflight_file.write(
                            f"| <img src=\"{background_image_url}\" alt=\"{name_testfight}\" align=\"center\" width=\"40\" height=\"40\" /> | **[{name_testfight}]({url_testflight})** | {hashtag_testflights}<br />{url_testflight}\n")
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
    txtTestflight_List = "Testflight_List.txt"
    txtResult_AvailableTestflight = "Result_BetaAppsAvailable.md"
    txtResult_ErrorLinkTestflight = "Result_ErrorLinkTestflight.txt"

    nowTime = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    CheckStatusCodeBetaApps()
    ResultBetaAppsAvailable()