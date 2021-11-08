import shutil
import os

def getInfo(listOfElems):
    ''' Get duplicate element in a list along with their indices in list
     and frequency count'''
    dictOfElems = dict()
    index = 0
    # Iterate over each element in list and keep track of index
    for elem in listOfElems:
        # If element exists in dict then keep its index in lisr & increment its frequency
        if elem in dictOfElems:
            dictOfElems[elem][0] += 1
            dictOfElems[elem][1].append(index)
        else:
            # Add a new entry in dictionary
            dictOfElems[elem] = [1, [index]]
        index += 1

    dictOfElems = { key:value for key, value in dictOfElems.items() if value[0] > 1}
    return dictOfElems

def correct_duplicates(dictOfElems, files_names, bin):
    try:
        for key, value in dictOfElems.items():
            res_list = [files_names[i] for i in value[1]]
            print('Element = ', key , ' :: Repeated Count = ', value[0] , ' :: Index Positions =  ', value[1], ' :: FilePaths = ', res_list)
            print("What file do you want to keep?")
            iter = 1
            for pos in res_list:
                print(iter,":", pos)
                iter += 1
            value = int(input("Enter corresponding number\n"))
            value = value - 1
            print(res_list[value]," will be kept")
            iter = 0
            for rep in res_list:
                if rep == res_list[value]:
                    pass
                else:
                    ext = os.path.splitext(rep)[1]
                    os.rename(rep,os.path.join(bin,key[0:5]+str(iter)+ext))
                    iter += 1
        return 0
    except Exception as e: 
        print(e)
        return 1


'''WARNING!!!'''
'''The following is legacy code. It had some problems, but I am keeping it here to ensure backword compatibility'''

def correct_duplicates_old(dictOfElems, files_names, bin):
    try:
        for key, value in dictOfElems.items():
            res_list = [files_names[i] for i in value[1]]
            print('Element = ', key , ' :: Repeated Count = ', value[0] , ' :: Index Positions =  ', value[1], ' :: FilePaths = ', res_list)
            smallest = min(len(entry) for entry in res_list)
            iter = 1
            redo = False
            for rep in res_list:
                if redo == False:
                    if len(rep) == smallest:
                        ext = os.path.splitext(rep)[1]
                        shutil.copy(rep,os.path.join(bin,key[0:5]+"0"+ext))
                        redo = True
                    else:
                        ext = os.path.splitext(rep)[1]
                        os.rename(rep,os.path.join(bin,key[0:5]+str(iter)+ext))
                        iter += 1
                else:
                    ext = os.path.splitext(rep)[1]
                    os.rename(rep,os.path.join(bin,key[0:5]+str(iter)+ext))
                    iter += 1
        return 0
    except Exception as e: 
        print(e)
        return 1
