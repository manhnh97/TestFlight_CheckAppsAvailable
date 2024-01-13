import re
from os import path

json_folder = input("JSON folder: ")
json_path = path.join(json_folder, "result.json").replace("\\", "\\\\")

output_file = "telegram_output_testflight_list.txt"
existing_links_file = "Testflight_List.txt"

# Function to extract unique links from a file
def extract_unique_links(file_path):
    links = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            links.add(line.strip())
    return links

# Read the content of the JSON file
with open(json_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

    # Regex pattern to match TestFlight links
    pattern = r'https?://testflight\.apple\.com/join/[a-zA-Z0-9_-]+'

    # Find all TestFlight links in the JSON string
    testflight_links = re.findall(pattern, file_content)

    # Use a set to store unique links
    unique_links = set(testflight_links)

    # Write unique TestFlight links to a file
    with open(output_file, 'a+') as output:
        for link in unique_links:
            output.write(link + '\n')

    # Get existing links
    existing_links = extract_unique_links(existing_links_file)
    new_links = extract_unique_links(output_file)

    # Get the unique links that are not in the existing set
    unique_new_links = new_links - existing_links

    # Append unique new links to the Testflight_List.txt file
    with open(existing_links_file, 'a') as append_file:
        for link in unique_new_links:
            append_file.write(link + '\n')
        append_file.write('\n')
