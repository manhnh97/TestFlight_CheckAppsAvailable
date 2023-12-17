from bs4 import BeautifulSoup
import requests
import re
from requests.exceptions import ConnectTimeout
from fake_useragent import UserAgent
from datetime import datetime
from time import sleep
import os

def CheckStatusCodeBetaApps():
    with open(txtTestflight_List, 'r', encoding='utf-8') as txtTestflightList_file, open(txtResult_AvailableTestflight, 'w', encoding='utf-8') as txtResult_AvailableTestflight_file, open(txtResult_ErrorLinkTestflight, 'w', encoding='utf-8') as txtResult_ErrorLinkTestflight_file:
        # List unique testflight links
        urls = list(set(txtTestflightList_file.read().splitlines()))
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36;accept-language":"en-GB,en;q=0.9'}
            while urls:
                url_testflight = urls.pop(0).strip()
                try:
                    response = requests.get(url_testflight, headers=headers)  # Set the timeout value here
                except ConnectTimeout:
                    urls.append(url_testflight)
                    headers = {'User-Agent': user_agent.random}
                    continue
                
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 3))  # Default to 5 seconds
                    sleep(retry_after)
                    urls.append(url_testflight)
                    
                if response.status_code == 200:                    
                    list_extracted_name = []
                    list_extracted_background = []
                    list_testflight_code = []
                    
                    # Find the text between "the" and "beta"
                    text_between_pattern = re.compile(r'To join the\s(.*?)\sbeta', re.IGNORECASE)
                    text_matches = text_between_pattern.findall(response.text)

                    # Find elements containing the URL (assuming it's an image)
                    url_pattern = re.compile(r'https?://\S+\.png')
                    url_match = url_pattern.findall(response.text)
                    if text_matches:
                        for extracted_name in text_matches:
                            list_extracted_name.append(extracted_name)
                            break
                        for extracted_background in url_match:
                            list_extracted_background.append(extracted_background)
                            break
                        list_testflight_code.append(f"{url_testflight.split("/")[-1]}.png")
                        
                    # Zip the lists together
                    zipped_data = list(zip(list_extracted_name, list_extracted_background, list_testflight_code))
                    # Directory containing the images
                    png_files = [file for file in os.listdir(folder_path) if file.endswith(".png")]
                    
                    for name, background, png_code in zipped_data:
                        # print(f"- Background: {background}\n- Name: {name}\n- Link: {url_testflight}\n- Code: {png_code} \n==================")
                        if png_code not in png_files:
                            url_background = requests.get(background)
                            # Assuming 'item' is a URL, you can use requests to download it
                            with open(os.path.join(folder_path, png_code), 'wb') as file:
                                file.write(url_background.content)
                                
                        name = name.replace('|', '-')
                        hashtags = re.findall(r"\b\w+\b", name)
                        hashtag = " ".join(["#" + hashtag.upper() for hashtag in hashtags])
                        # nameSearch = "https://www.google.com/search?q="+name.replace(" ", "+")+"+"+"appstore"
                        # txtResult_AvailableTestflight_file.write(
                            # f"| <img src=\"{folder_path}\\{png_code}\" align=\"center\" width=\"40\" height=\"40\" /> | **[{name}]({nameSearch})** | {hashtag}<br />{url_testflight} |\n")
                        txtResult_AvailableTestflight_file.write(
                            f"| <img src=\"{folder_path}\\{png_code}\" align=\"center\" width=\"40\" height=\"40\" /> | **[{name}]** | {hashtag}<br />{url_testflight} |\n")
                else:
                    txtResult_ErrorLinkTestflight_file.write(f"{url_testflight}\n")
        except AttributeError:
            pass

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

def ErrorLinkTestflight():
    with open(txtTestflight_List, 'r') as f1, open(txtResult_ErrorLinkTestflight, 'r') as f2:
        lines_f1 = f1.read().splitlines()
        lines_f2 = f2.read().splitlines()

    # Remove duplicate lines from Testflight_list.txt
    unique_lines_f1 = list(set(lines_f1))

    # Remove lines from Testflight_list.txt that match the content of Result_ErrorLinkTestflight.txt
    updated_lines_f1 = [line for line in unique_lines_f1 if line not in lines_f2]

    with open("Testflight_list.txt", 'w') as f1:
        f1.write('\n'.join(updated_lines_f1))

if __name__ == "__main__":
    # Create images folder if the folder is not exists
    from pathlib import Path
    Path("images").mkdir(parents=True, exist_ok=True)
    # Directory containing the images
    folder_path = "images"  # Replace this with your folder path
    
    nowTime = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    txtTestflight_List = "Testflight_List.txt"
    txtResult_AvailableTestflight = "Result_BetaAppsAvailable.md"
    txtResult_ErrorLinkTestflight = "Result_ErrorLinkTestflight.txt"
    
    user_agent = UserAgent(browsers=['edge', 'chrome'])

    CheckStatusCodeBetaApps()
    ResultBetaAppsAvailable()
    ErrorLinkTestflight()