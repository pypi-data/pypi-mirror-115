import sys
import io
import csv
import pprint
import pandas as pd

# sys.argv[1] = 'a.csv'
# sys.argv[2] = 'b.csv'
encoding_value = 'shift-jis'

if(len(sys.argv) <= 1):
    print('For example: only_common.py a.csv b.csv shift-jis')
    sys.exit()
elif(len(sys.argv) <= 2):
    print('For example: only_common.py a.csv b.csv shift-jis')
    sys.exit()
elif(len(sys.argv) <= 3):
    print('sys.argv[1]:', sys.argv[1])
    print('sys.argv[2]:', sys.argv[2])
    print('sys.argv[3]:', encoding_value)
elif(len(sys.argv) <= 4):
    print('sys.argv[1]:', sys.argv[1])
    print('sys.argv[2]:', sys.argv[2])
    print('sys.argv[3]:', sys.argv[3])
    encoding_value = sys.argv[3]

df_a = pd.read_csv(sys.argv[1], encoding=encoding_value, header=None)
list_a = []
list_a = list(df_a.loc[0][0])

df_b = pd.read_csv(sys.argv[2], encoding=encoding_value, header=None)
list_b = []
list_b = list(df_b.loc[0][0])

after_content = ""
def duplicate_delete_csv(content, content2, after_content):
    for i in range(len(content)):
        if content[i] != content2[i]:
            for num in range(len(content) - i):
                if content2[i] == content[i+num]:
                    after_content = content[:i] + content[(i+num):]
                    return after_content
    return content


while list_a != list_b:
    if(len(list_a) > len(list_b)):
        list_a_old = list_a
        list_a = duplicate_delete_csv(list_a, list_b, after_content)
        if list_a_old == list_a:
            break
    elif(len(list_a) < len(list_b)):
        list_b_old = list_b
        list_b = duplicate_delete_csv(list_b, list_a, after_content)
        if list_b_old == list_b:
            break
    else:
        list_a_old = list_a
        list_a = duplicate_delete_csv(list_a, list_b, after_content) 
        list_b_old = list_b
        list_b = duplicate_delete_csv(list_b, list_a, after_content)
        if list_b_old == list_b:
            break

StrA = "".join(list_a)
print('Only common parts:', StrA)
sys.exit
