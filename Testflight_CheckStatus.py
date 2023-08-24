from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime

def SaveData(txtResult_AvailableTestflight, txtResult_ErrorLinkTestflight, Testflight_Available, Testflight_Error, txtReadme):
    nowTime = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    with open(txtResult_AvailableTestflight, 'w', encoding='utf-8') as wfile:
        wfile.write(f"""# Beta Apps is available\t[{nowTime}]\n""")
        wfile.write('| Sort | Image | Description |\n| --- | --- | --- | \n')
        wfile.write('\n'.join(Testflight_Available))
        wfile.write(f'''| \'ZzZ\' | <img src="https://avatars.githubusercontent.com/u/42213325?v=4" alt="HaveAgreatDay" align="center" width="40" height="40" /> | **[Have a great day!!!](https://github.com/manhnh97/CheckStatusTestflight/)** |''')

    with open(txtResult_ErrorLinkTestflight, 'w', encoding='utf-8') as wfile:
        wfile.write('\n'.join(Testflight_Error))

    with open(txtReadme, 'w', encoding='utf-8') as wfile:
        wfile.write(f"""# CheckStatusTestflight\n## Beta Apps is available\t[{nowTime}]\n""")
        wfile.write(f"""**[Beta Apps Are Available!!!](https://github.com/manhnh97/CheckStatusTestflight/blob/master/Result_BetaAppsAvailable.md)**""")

def RemoveLinkNotFound(txtTestflight_List, txtResult_ErrorLinkTestflight):
    with open(txtTestflight_List, 'r') as f1, open(txtResult_ErrorLinkTestflight, 'r') as f2:
        list1 = set(f1.readlines())
        list2 = set(f2.readlines())

    result = list1 - list2

    with open(txtTestflight_List, 'w') as f:
        f.writelines(result)

if __name__ == "__main__":
    txtTestflight_List = "Testflight_List.txt"
    txtResult_AvailableTestflight = "Result_BetaAppsAvailable.md"
    txtResult_ErrorLinkTestflight = "Result_ErrorLinkTestflight.txt"
    txtReadme = 'README.md'

    with open(txtTestflight_List, 'r', encoding='utf-8') as rfile:
        lines = [line for line in rfile]
        Testflight_Available = []
        Testflight_Error = []
        count = 1

        try:
            session = requests.Session()
            for url_testflight in lines:
                r = session.get(url_testflight)
                print(f"Checking ({count}): ", url_testflight, end='')
                if r.status_code == 200:
                    soup = bs(r.text, 'html.parser')
                    div_BetaStatus = soup.find('div' , {'class':'beta-status'})
                    
                    # Get Beta Name
                    span_BetaStatus = div_BetaStatus.find('span').text
                    match_JoinBeta = re.search(r'To join the(.*) beta', span_BetaStatus)
                    
                    # Get image
                    style = soup.find("div", {"class": "app-icon"})["style"]
                    background_image_url = style.split("(")[1].split(")")[0]
                    if match_JoinBeta:
                        name_testfight = match_JoinBeta.group(1).replace('|', '-')
                        matches = re.findall(r'\b[A-Z][A-Za-z]*\b', name_testfight)
                        Testflight_Available.append(f'''| \'{name_testfight[1].upper()}\' | <img src="{background_image_url}" alt="{name_testfight}" align="center" width="40" height="40" /> | **[{name_testfight}]({url_testflight.strip()})** |''')
                else:
                    Testflight_Error.append(url_testflight)
                count += 1
            session.close()
        except AttributeError:
            pass
        finally:
            Testflight_Available.sort()
            SaveData(txtResult_AvailableTestflight, txtResult_ErrorLinkTestflight, Testflight_Available, Testflight_Error, txtReadme)
            RemoveLinkNotFound(txtTestflight_List, txtResult_ErrorLinkTestflight)