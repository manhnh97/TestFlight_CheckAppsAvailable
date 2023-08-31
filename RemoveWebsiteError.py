with open("Testflight_list.txt", 'r') as f1, open('Result_ErrorLinkTestflight.txt', 'r') as f2:
    lines_f1 = f1.read().splitlines()
    lines_f2 = f2.read().splitlines()

# Remove duplicate lines from Testflight_list.txt
unique_lines_f1 = list(set(lines_f1))

# Remove lines from Testflight_list.txt that match the content of Result_ErrorLinkTestflight.txt
updated_lines_f1 = [line for line in unique_lines_f1 if line not in lines_f2]

with open("Testflight_list.txt", 'w') as f1:
    f1.write('\n'.join(updated_lines_f1))