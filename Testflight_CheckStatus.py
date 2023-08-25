from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime

def SaveData(txtResult_AvailableTestflight, Testflight_Available, txtResult_ErrorLinkTestflight):
    nowTime = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    with open(txtResult_AvailableTestflight, 'w', encoding='utf-8') as wfile:
        wfile.write(f"# Beta Apps is available\t[{nowTime}]\n")
        wfile.write('| Sort | Image | Description |\n| --- | --- | --- | \n')
        wfile.writelines(Testflight_Available)
        wfile.write(f'''| 'ZzZ' | <img src="https://avatars.githubusercontent.com/u/42213325?v=4" alt="HaveAgreatDay" align="center" width="40" height="40" /> | **[Have a great day!!!](https://github.com/manhnh97/CheckStatusTestflight/)** |''')

    with open(txtReadme, 'w', encoding='utf-8') as wfile:
        wfile.write(f"""# CheckStatusTestflight\n## Beta Apps is available\t[{nowTime}]\n""")
        wfile.write(f"""**[Beta Apps Are Available!!!](https://github.com/manhnh97/CheckStatusTestflight/blob/master/Result_BetaAppsAvailable.md)**""")

    with open(txtResult_ErrorLinkTestflight, 'w', encoding='utf-8') as wfile:
        wfile.write('\n'.join(Testflight_Error))

if __name__ == "__main__":
    txtTestflight_List = "Testflight_List.txt"
    txtResult_AvailableTestflight = "Result_BetaAppsAvailable.md"
    txtResult_ErrorLinkTestflight = "Result_ErrorLinkTestflight.txt"
    txtReadme = 'README.md'

    Testflight_Available = []
    Testflight_Error = []

    with open(txtTestflight_List, 'r', encoding='utf-8') as rfile:
        urls = rfile.read().splitlines()
    try:
        session = requests.Session()
        for count, url_testflight in enumerate(urls, start=1):
            r = session.get(url_testflight.strip())
            print(f"Checking ({count}): ", url_testflight)
            if r.status_code == 200:
                soup = bs(r.text, 'html.parser')
                div_BetaStatus = soup.find('div', {'class': 'beta-status'})

                span_BetaStatus = div_BetaStatus.find('span').text
                isBetaAppAvaiable = re.search(r'To join the(.*) beta', span_BetaStatus)

                style = soup.find("div", {"class": "app-icon"})["style"]
                background_image_url = style.split("(")[1].split(")")[0]
                if isBetaAppAvaiable:
                    name_testfight = isBetaAppAvaiable.group(1).replace('|', '-')
                    Testflight_Available.append (
                        f'''| '{name_testfight[1].upper()}' | <img src="{background_image_url}" alt="{name_testfight}" align="center" width="40" height="40" /> | **[{name_testfight}]({url_testflight.strip()})** |\n'''
                    )
            else:
                Testflight_Error.append(url_testflight)
    except AttributeError:
        pass
    finally:
        session.close()
        Testflight_Available.sort()
        SaveData(txtResult_AvailableTestflight, Testflight_Available, txtResult_ErrorLinkTestflight)