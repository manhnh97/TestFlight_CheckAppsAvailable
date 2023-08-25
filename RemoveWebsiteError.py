with open("Testflight_list.txt", 'r') as f1, open('Result_ErrorLinkTestflight.txt', 'r') as f2:
    lines_f1 = f1.readlines()
    lines_f2 = f2.readlines()

    updated_lines_f1 = [line for line in lines_f1 if line not in lines_f2]

with open("Testflight_list.txt", 'w') as f1:
    f1.writelines(updated_lines_f1)