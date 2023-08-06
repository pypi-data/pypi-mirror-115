def print_lol(aList):
    for each in aList:
        if isinstance(each,list):
            print_lol(each)
        else:
            print(each)
