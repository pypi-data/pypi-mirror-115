def print_lol(aList,level):
    for each in aList:
        if isinstance(each,list):
            print_lol(each,level+1)
        else:
            for i in range(level):
                print('\t',end='')
            print(each)
