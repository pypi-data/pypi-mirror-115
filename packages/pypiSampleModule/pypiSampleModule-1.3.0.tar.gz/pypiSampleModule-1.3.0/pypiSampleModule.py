import sys
def print_lol(aList,fh=sys.stdout,level=0,indent=False):
    for each in aList:
        if isinstance(each,list):
            print_lol(each,fh,level,indent)
        else:
            if indent:
                for i in range(level):
                    print('\t',end='',file=fh)
            print(each,file=fh)
