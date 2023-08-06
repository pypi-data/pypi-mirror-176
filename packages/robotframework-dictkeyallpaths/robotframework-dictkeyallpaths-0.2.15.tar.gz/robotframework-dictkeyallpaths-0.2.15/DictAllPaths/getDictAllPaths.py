class GetDictAllPaths:

    def __init__(self):
        pass

    def __chkDupPath(self,subKey,allKeys):
        chk=False
        keyPath=","
        keyPath=keyPath.join(subKey)
        jsonPath=self.__setFormatRobotPath(keyPath)

        if len(allKeys)>1:
            for path_key in allKeys:
                if path_key.find(jsonPath) != -1:
                    chk=True
                    break

        return chk

    def __chkPath(self,subKey,dataDict,allKeys):
        chkDictPath=[subKey,True]
        for y in subKey:
            
            if (y.find('[') != -1): # To split subkey dct[k[0]] >> dct[k][0]
                start=y.find('[')
                end=y.find(']')
                index=int(y[start+1:end])
                tmpKey=y[:start]
                try:
                    if start == 0:
                        dataDict = dataDict[index]
                    else:
                        dataDict = dataDict[tmpKey][index]
                except:
                    subKey.pop()
                    subKey.pop()
                    chkDictPath[0]=subKey
                    chkDictPath[1]=False
                    break
            else:
                try:
                    dataDict = dataDict[y]
                except:
                    subKey.pop()
                    subKey.pop()
                    chkDictPath[0]=subKey
                    chkDictPath[1]=False 
                    break

        if chkDictPath[1] and self.__chkDupPath(subKey,allKeys):
            subKey.pop()
            subKey.pop()
            chkDictPath[0]=subKey
            chkDictPath[1]=False 

        return chkDictPath


    def __NextPath(self,subKey,key,dataDict,allKeys):  # Check Next Path is correct?
        if len(subKey)>0:
            subKey.pop()  # delete previous  key

        subKey.append(key) # ad new key

        for i in range(len(subKey)):
            chkJsonPath=self.__chkPath(subKey,dataDict,allKeys)
            if chkJsonPath[1] == True:
                break
            subKey=chkJsonPath[0]
            subKey.append(key)
        return subKey


    def __recursive_dict(self,dataDict):
        for key, value in dataDict.items():
            if type(value) is dict:
                yield (key, value)
                yield from self.__recursive_dict(value)
            elif type(value) is list:
                yield from self.__recursive_list(key,value)
            else:
                yield (key, value)

    def __recursive_list(self,key,dataList):          
        index=0
        for item in dataList:
            tmpKey=key + "[" + str(index) + "]"
            yield (tmpKey,item)
            if type(item) is dict:
                yield from self.__recursive_dict(item)
            elif type(item) is list:
                yield from self.__recursive_list('',item)
            index+=1


    def __setFormatRobotPath(self,keyPath):
        keyPath=keyPath.replace("[",",[")
        pathList=keyPath.split(",")
        robotDictPath=""
        for item in pathList:
            if (item.find("[") == -1):  # If it not List
                robotDictPath=robotDictPath + "['" + item + "']"
            else:
                robotDictPath=robotDictPath + item
        robotDictPath=robotDictPath.replace("['']","")
        return robotDictPath

    def Get_Dict_Paths(self,dataDict):
        '''
		This is function that get keys from dictionary type.
		Return all paths of the given dictionary as a list.
		'''
        allKeys=[]
        subKey=[]

        preValue="<class 'dict'>"
        for key, value in self.__recursive_dict(dataDict):
            # print(f'key >> {key}')
            if type(value) in [dict]:
                if preValue == "<class 'dict'>":
                    subKey.append(key)
                subKey=self.__NextPath(subKey,key,dataDict,allKeys)
            elif type(value) in [list]:
                subKey=self.__NextPath(subKey,key,dataDict,allKeys)
            else:
                subKey.append(key)

                for i in range(len(subKey)):
                    chkJsonPath=self.__chkPath(subKey,dataDict,allKeys)
                    if chkJsonPath[1] == True:
                        break
                    subKey=chkJsonPath[0]
                    subKey.append(key)

                mySeparator=","
                keyPath=mySeparator.join(subKey)
                jsonPath=self.__setFormatRobotPath(keyPath)
                allKeys.append(jsonPath)


            preValue=str(type(value))

        return allKeys

    def __str__(self):
        return "This is a function that gets the keys of all values ​​in the dictionary."


if __name__ == '__main__':

	json_string='''
	{
	  	"SuperMarket": {
		    "Fruit": [
		      {
		        "Name": "Apple",
		        "Manufactured":"USA",
		        "price": 7.99
		      },
		      {
		        "Name": "Banana",
		        "Manufactured":"Japan",
		        "price": 3.99
		      }
		    ],
		    "Drink": {
				"SoftDrink":{
					"Cola": [
				      	{
				      		"Color":"Red",
				      		"Price":15.00
				      	},
				      	{
				      		"Color":"Green",
				      		"Price":17.99
				      	}
				      ],      
				      "Coffee": {
				      	"Hot":[
					      	{
					      		"Type":"Espresso",
					      		"Price":15.90
					      	},
					      	{
					      		"Type":"Cappuccino",
					      		"Price":10.90
					      	}
					    ],
					    "Ice":[
					      	{
					      		"Type":"Espresso",
					      		"Price":20.90
					      	},
					      	{
					      		"Type":"Cappuccino",
					      		"Price":15.90
					      	}
					    ]
				    }
				}     
		    }
	  	}
	}
	'''

	dictData=json.loads(json_string)
	print(dictData)
	dictKeys=GetDictAllPaths()
	keyList=dictKeys.getDictPaths(dictData)
	for item in keyList:
		print("key:" + item + " >> value:")