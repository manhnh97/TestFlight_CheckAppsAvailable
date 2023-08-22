import csv
from bs4 import BeautifulSoup as bs
import requests
import re

txtTestflight_List = "Testflight_List.txt"
txtResult_AvailableTestflight = "Result_Testflight.txt"
txtResult_ErrorLinkTestflight = "Result_ErrorLinkTestflight.txt"

with open(txtTestflight_List, 'r', encoding='utf-8') as rfile:
    lines = [line for line in rfile]
    Testflight_Available = []
    Testflight_Error = []
    count = 1
    try:
        for url_testflight in lines:
            r = requests.get(url_testflight)
            if r.status_code == 200:
                soup = bs(r.text, 'html.parser')
                # titles = soup.find_all('span', attrs={'class', 'beta-status'})
                div_BetaStatus = soup.find('div' , {'class':'beta-status'})
                span_BetaStatus = div_BetaStatus.find('span').text
                match_JoinBeta = re.search(r'To join the(.*) beta', span_BetaStatus)
                print(f"Checking ({count}): ", url_testflight, end='')
                if match_JoinBeta:
                    name_testfight = match_JoinBeta.group(1)
                    matches = re.findall(r'\b[A-Z][A-Za-z]*\b', name_testfight)
                    hashtag_testflight = '#' + ' #'.join(matches)
                    # Testflight_Available.append(f"[{hashtag_testflight.upper()}]{name_testfight} => {url_testflight}")
                    Testflight_Available.append(f'''<li><strong><a href="{url_testflight}" title="{name_testfight}">{name_testfight}</a></strong></li>''')
                count += 1
            else:
                Testflight_Error.append(url_testflight)
    except AttributeError:
        pass

with open(txtResult_AvailableTestflight, 'w', encoding='utf-8') as wfile:
    wfile.write('<ol>\n')
    wfile.write('\n'.join(Testflight_Available))
    wfile.write('\n</ol>')

with open(txtResult_ErrorLinkTestflight, 'w', encoding='utf-8') as wfile:
    wfile.write('\n'.join(Testflight_Error))
#<a href="https://testflight.apple.com/join/zxlMasyx" title="Test">Test</a></p>

