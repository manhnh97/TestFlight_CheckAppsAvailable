with open("Testflight_list.txt", 'r') as f1, open('Result_ErrorLinkTestflight.txt', 'r') as f2:
    list1 = set(f1.readlines())
    list2 = set(f2.readlines())

result = list1 - list2

with open('Testflight_List.txt', 'w') as f:
    f.writelines(result)