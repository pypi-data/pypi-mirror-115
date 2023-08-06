import sys
import io
import csv
import pprint
import pandas as pd

def excommon(arg_1 = 'a.csv', arg_2 = 'b.csv', arg_3 = 'shift-jis'):

    print('sys.argv[1]:', arg_1)
    print('sys.argv[2]:', arg_2)
    print('sys.argv[3]:', arg_3)

    df_a = pd.read_csv(arg_1, encoding=arg_3, header=None)
    list_a = []
    list_a = list(df_a.loc[0][0])

    df_b = pd.read_csv(arg_2, encoding=arg_3, header=None)
    list_b = []
    list_b = list(df_b.loc[0][0])

    after_content = ""
    after_content2 = ""
    flag_last = "0"
    def duplicate_delete_csv(content, content2, after_content, after_content2, flag_last):
        after_content = content
        after_content2 = content2
        for i in range(len(content)):
            if i > int(len(content2)-1):
                after_content = content[:i]
                flag_last = "1"
                return after_content, after_content2, flag_last
            if len(content) - 1 == i:
                flag_last = "1"
            if content[i] != content2[i]:
                for num in range(len(content) - i):
                    if content2[i] == content[i+num]:
                        after_content = content[:i] + content[(i+num):]
                        return after_content, after_content2, flag_last
                after_content2 = content2[:i] + content2[i+1:]
                return after_content, after_content2, flag_last

    while list_a != list_b:
        list_a, list_b, flag_last = duplicate_delete_csv(list_a, list_b, after_content, after_content2, flag_last) 
        if flag_last == "1":
            break
    StrA = "".join(list_a)
    print('Only common parts:', StrA)
    sys.exit
