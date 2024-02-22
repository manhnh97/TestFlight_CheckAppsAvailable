TXT_RESULT_FULL_BETA_APPS = 'Testflight_List_Full.txt'
TXT_RESULT_NEW_BETA_APPS = 'Testflight_List_Full.txt'

def update_testflight_list():
    with open(TXT_RESULT_FULL_BETA_APPS, 'r', encoding='utf-8') as f1, open(TXT_RESULT_NEW_BETA_APPS, 'r', encoding='utf-8') as f2:
        lines_f1 = f1.read().splitlines()
        lines_f2 = f2.read().splitlines()
    unique_lines_f1 = list(set(lines_f1))
    updated_lines_f1 = [line for line in unique_lines_f1 if line not in lines_f2]
    print(updated_lines_f1)