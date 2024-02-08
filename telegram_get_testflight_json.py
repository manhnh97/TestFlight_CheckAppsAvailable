import os
import re

def extract_unique_links(file_path):
    links = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            links.add(line.strip())
    return links

def find_result_json_files(root_folder):
    result_files = []
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == 'result.json':
                result_files.append(os.path.join(foldername, filename))
    return result_files

# Specify the root folder where you want to start searching
ROOT_FOLDER = r'D:\Downloads\Telegram Desktop'

OUTPUT_FILE = "telegram_output_testflight_list.txt"
EXISTING_LINKS_FILE = "Testflight_List.txt"

# Regex pattern to match TestFlight links
PATTERN = r'https?://testflight\.apple\.com/join/[a-zA-Z0-9]{8}+'

if not os.path.exists(EXISTING_LINKS_FILE):
    # File does not exist, create it
    with open(EXISTING_LINKS_FILE, 'w'):
        pass

# Call the function to find all result.json files
result_json_files = find_result_json_files(ROOT_FOLDER)

# Set to store unique links
unique_links = set()

# Print the list of result.json files found
for file in result_json_files:
    json_path = file.replace('\\', '\\\\')
    with open(json_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        # Find all TestFlight links in the JSON string
        testflight_links = re.findall(PATTERN, file_content)

        # Add the links to the set of unique links
        unique_links.update(testflight_links)

# Write unique TestFlight links to a file
with open(OUTPUT_FILE, 'a+') as output:
    for link in unique_links:
        output.write(link + '\n')

# Get existing links
new_links = extract_unique_links(OUTPUT_FILE)

# Read unique lines from file 'b' and store them in a set
unique_lines = set()
with open(OUTPUT_FILE, 'r', encoding='utf-8') as infile, open(EXISTING_LINKS_FILE, 'w', encoding='utf-8') as outfile:
    for line in infile:
        unique_lines.add(line.strip())

    for line in unique_lines:
        outfile.write(line + '\n')
