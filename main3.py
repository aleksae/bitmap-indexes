import math
import sys
import re

states = {
    0: "No schema loaded",
    1: "Schema and data loaded, query proccessing allowed"
}
factTable = {}
factTable['columns'] = []
dTables = {}


def printOptions():
    print("-------------------------------------------------------")
    print("Current state: " + states[state])
    if state==0:
        print("1. Load schema from file (data will be loaded automatically - files must be in same folder!)")
    print("2. Execute query")
    print("Enter -1 to exit")


def proccesInput():
    print("Welcome! \n")
    printOptions()
    for line in sys.stdin:
        if '-1' == line.rstrip():
            break
        try:
            value = int(line.rstrip())
            if value == 1 and state==0:
                dataLoad()
                pass
            elif value == 2 and state==1:
                queryExec()
                pass
            elif state==1:
                pass
            else:
                print("Invalid number, please try again.")
                pass
        except Exception as e:
            print("Invalid input, please try again. In this stage int is expected.")
            print(e)
            pass
        printOptions()
    print("Done, 30 points")

factTableData = []
def get_chars_before_first_parenthesis(s):
    index = s.find('(')
    if index != -1:
        return s[:index]
    return s

def get_chars_after_first_parenthesis(s):
    index = s.find('(')
    if index != -1:
        return s[index + 1:]
    return ''

def dataLoad():
    global state
    global factTable

    print("Enter file name for schema:")
    schema = input()
    try:
        
        schemaFile = open(schema, "r")
    except:
        print("Error: File not found.")
        return
    firstRow = True
    for line in schemaFile:
        tableName = get_chars_before_first_parenthesis(line)
        columns = get_chars_after_first_parenthesis(line[:-2]).split(',')
        if firstRow:
            for column in columns:
                cols = column.split(";")
                if(len(cols)>1):

                    #d column, foreign key
                    try:
                        file1 = open(cols[1]+".txt", "r")
                        sizes = file1.readline()[:-1].split(',')
                        dTables[cols[1]]={
                            "fileHandle": file1,
                            "sizes": [int(size) for size in sizes]
                        }
                    except:
                        print("Error: Foreign key table "+cols[1]+" not found.")
                        
                        return
                try:
                    #print("Accessing "+tableName+".txt")
                    factFile = open(tableName+".txt", "r")
                    sizes = factFile.readline()[:-1].split(',')
                    factTable["fileHandle"] = factFile
                    factTable["sizes"] = [int(size) for size in sizes]
                    factTable['columns'].append(cols[0].strip()),
                    '''for line in factFile:
                        factTableData.append(line)'''
                   
                except Exception as e:
                    print("Error: Fact table "+tableName+" not found.")
                    print(e)
                    return

            firstRow = False
            print("Schema loaded - loading data.")
            print("Fact table schema: " + ", ".join(factTable['columns']))
            
        else:
            dTables[tableName]['columns'] = columns
            '''try:
                dTables[tableName]
                #print("Access ++++ "+dTables[tableName])
            except:
                print("Access error "+dTables[tableName])
                #print(dTables)'''      
    
    print("Schema and data loaded - creating indexes.")
    createIndexes()
    print("Indexes created. Procceeding to query proccessing.")
    state = 1


indexes = {}
def createIndexes():
    global indexes
    tables = []
    try:
        for table in dTables:
            tables.append(table)
            fileToBrowse = dTables[table]['fileHandle']
            indexes[dTables[table]['columns'][0]] = {}
            for line in fileToBrowse:
                id = int(line.strip("()").split(",")[0])
                indexes[dTables[table]['columns'][0]][id] = [0 for i in range(len(factTable['sizes']))]
        factFile = factTable['fileHandle']
        factFile.seek(0)
        factFile.readline()
        columns = factTable['columns'][1::]
        lineCnt = 0
        for line in factFile:
            line = line.strip("()").split(",")[1::]
            
            try:
                for i, l in enumerate(line):
                    if(i==len(line)-1):
                        continue
                    if(chechIfDColumns(columns[i])):
                        indexes[columns[i]][int(l)][lineCnt] = 1
            except Exception as e:
                print("error1")
                print(e)
            lineCnt+=1
        #print(factTableData)
    except Exception as e:
        print("error2")
        print(e)
        return


def chechIfDColumns(s):
    s_lower = s.lower()
    return 'id' in s_lower


def queryExec():
    print("Query input:")
    print("Choose funcion to execute (min, max, avg, sum, cnt):")
    func = input()
    print("Choose column to be applied (* for all) (separate by comma, no space):")
    columns = input()
    if columns != '*':
        columns = columns.split(',')
        #print(factTable['columns'])
        try:
            for col in columns:
                if col not in set(factTable['columns']):
                    print("Error: Column "+col+" not found in fact table.")
                    return
                if chechIfDColumns(col):
                    print("Error: Column "+col+" is a foreign key.")
                    return
        except Exception as e:
            print(e)
            return
    else:
        columns = [col for col in factTable['columns'] if not chechIfDColumns(col)]
    print("Choose if you wanna apply indexes (y/n):")
    index = input()
    index = True if index == 'y' else False
    

    print("You wanna do "+func+"("+",".join(columns)+")"+(" with indexes." if index else " without indexes."))
    print("Enter conditions (dcol OP dcol....)")
    conditions =  input()
    try:
        cond, op= parseCondition(conditions)
        if index:
            proccessWithIndex(func, columns, cond, op)
        else:  
            proccessWithoutIndex(func, columns, cond, op)
    except Exception as e:
        print(e)

import time


def proccessWithIndex(func, columns, cond, op):
    start = time.time()
    print("proccessing started")

    try:
        conditionCounter = 0
        opCounter = 0
        res = []
        ispis = []
        while conditionCounter<len(cond):
            column = cond[conditionCounter].split("=")[0]
            ispis.append(column)
            
            value =  int(cond[conditionCounter].split("=")[1])
            for table in dTables:
                if column in dTables[table]['columns']:
                    file1 = dTables[table]['fileHandle']
                    file1.seek(0)
                    file1.readline()
                    dataStart = file1.tell()
                    desiredId = value
                    file1.seek(dataStart + sum([int(size) for size in dTables[table]['sizes'][:desiredId-1]])+desiredId-1)
                    desiredRow = file1.readline().strip('()').split(',')
                    desiredRow[-1] =  desiredRow[-1][:-2]
                    for row in desiredRow:
                        ispis.append(row)
                    

            '''try:
                #print(indexes[column])
            except:
                print("Error: Column "+column+" not found in indexes.")
                return
            try:
                print(indexes[column][value])
            except:
                print("Error: Value "+value+" not found in indexes.")
                return'''
            temp = indexes[column][value]
            #print("temp with column "+column+" and value "+str(value)+" is "+str(temp))
            if conditionCounter==0:
                res = temp
            else:
                if op[opCounter] == 'AND':
                    #res = [res[i] and temp[i] for i in range(len(res))]
                    res = [a & b for a, b in zip(res, temp)]
                    #res = res & temp
                else: 
                    #res = [res[i] or temp[i] for i in range(len(res))]
                    res = [a | b for a, b in zip(res, temp)]
                    #res = res | temp
                opCounter+=1
            conditionCounter+=1
        #print(res)
        rowIndexes = [cnt for cnt,i in enumerate(res) if i==1]
        rowIds = [i+1 for i in rowIndexes]
        file1 = factTable['fileHandle']
        file1.seek(0)
        file1.readline()
        lastDataPointer = file1.tell()
        lastId = 0
        #print(file1.tell())
        #print(factTableData)
        rows = []
        for rowId in rowIds:
            try:

                desiredId = rowId
                #dataStart = dataStart + sum([int(size) for size in factTable['sizes'][:desiredId-1]])+desiredId-1
                lastDataPointer = lastDataPointer + sum([int(size) for size in factTable['sizes'][lastId:desiredId-1]])+desiredId-lastId-1
                lastId = desiredId-1
                file1.seek(lastDataPointer)
                row = file1.readline()
                row = row.strip('()').split(',')
                
                row[-1] =  row[-1][:-2]
                #print(row)
                rows.append(row)
            except Exception as e:
                print("Error: Row "+str(rowId)+" not found in fact table.")
                print(e)
        #print(rows)
        neededColumns = []
        for i,c in enumerate(factTable['columns']):
            if c in columns:
                neededColumns.append(i)
        returning = [0 for i in range(0, max(neededColumns)+1)]
        if func == "max":
            for r in rows:
                for c in neededColumns:
                    returning[c] = max(returning[c], int(r[c]))
        elif func == "min":
            returning = [math.inf for i in range(0, max(neededColumns)+1)]
            for r in rows:
                for c in neededColumns:
                    returning[c] = min(returning[c], int(r[c]))
        elif func == "avg":
            for r in rows:
                for c in neededColumns:
                    returning[c] += int(r[c])
            returning = [i/len(rows) for i in returning]
        elif func == "sum":
            for r in rows:
                for c in neededColumns:
                    returning[c] += int(r[c])
        elif func == "cnt":
            for r in rows:
                for c in neededColumns:
                    returning[c] += 1
        else:
            print("Error: Function "+func+" not found.")
            return
        [ispis.append(i) for cnt,i in enumerate(returning) if cnt in neededColumns]
        end = time.time()
        print(ispis)
        print("Time taken: ")
        print(end - start)
        

    except Exception as e:
        print("proccesWithIndex error")
        print(e)



def proccessWithoutIndex(func, columns, cond, op):
    start = time.time()
    print("proccessing started")
    file1 = factTable['fileHandle']
    file1.seek(0)
    file1.readline()
    neededColumns = []
    colUnqiue=[]
    ispis = []
    for col in cond:
        for i,c in enumerate(factTable['columns']):
            if c == col.split("=")[0]:
                neededColumns.append(i)
    neededCondColumns = []
    helpCond = [cond.split("=")[0] for cond in cond]
    helpValue = [cond.split("=")[1] for cond in cond]
    neededValue = []
    for ii,ch in enumerate(helpCond):
        for i,c in enumerate(factTable['columns']):
            if c == ch:
                #if ch not in colUnqiue:
                if True:
                    #colUnqiue.append(ch)
                    #print("ispis appended " + ch)
                    ispis.append(ch)
                    #-----------------------
                    for tab in dTables:
                        if ch in dTables[tab]['columns']:
                            file2 = dTables[tab]['fileHandle']
                            file2.seek(0)
                            file2.readline()
                            desiredID = int(helpValue[ii])
                            for line in file2:
                                id = int(line.strip("()").split(",")[0])
                                if id == desiredID:
                                    desiredRow = line.strip("()").split(",")[1::]
                                    desiredRow[-1] =  desiredRow[-1][:-2]
                                    for row in desiredRow:
                                        #print("ispis appended " + row)
                                        ispis.append(row)
                    #------------------------
                neededCondColumns.append(i)
                neededValue.append(helpValue[ii])
    #print(neededCondColumns)
    #print(neededValue)
    #print(op)
    print(neededCondColumns)
    print(neededValue)
    result = []
    dataStart = file1.tell()
    desiredId = 1
    '''while desiredId<len(factTable['sizes']):
        #print(desiredId)
        file1.seek(dataStart + sum([int(size) for size in factTable['sizes'][:desiredId-1]])+desiredId-1)'''
        #line = file1.readline()
        #desiredId+=1
    for line in file1:
        
        l = line.strip("()").split(",")
        l[-1] = l[-1][:-2]
        data = []
        for cndNeeded in neededCondColumns:
            for cntIntern, ll in enumerate(l):
                if cndNeeded == cntIntern:
                    data.append(int(ll))
        conditionCounter = 0
        opCounter = 0
        #print(data)
        res = []
        while conditionCounter<len(cond):
            temp = data[conditionCounter]
            temp = int(temp)==int(neededValue[conditionCounter])
            #print("Data is "+str(data[conditionCounter])+" and needed value is "+str(neededValue[conditionCounter]))
            if conditionCounter==0:
                res = temp
                #print("res eq temp and res is "+str(res))
            else:
                if op[opCounter] == 'AND':
                    res = res and temp
                    #print("res and temp and res is "+str(res))
                else:  
                    res = res or temp
                    #print("res or temp and res is "+str(res))
                opCounter+=1
            conditionCounter+=1
        if res and l not in result:
            result.append(l)
    rows = result

    #print(rows)
    neededColumns = []
    for i,c in enumerate(factTable['columns']):
        if c in columns:
            neededColumns.append(i)
    returning = [0 for i in range(0, max(neededColumns)+1)]
    if func == "max":
        for r in rows:
            for c in neededColumns:
                returning[c] = max(returning[c], int(r[c]))
    elif func == "min":
        returning = [math.inf for i in range(0, max(neededColumns)+1)]
        for r in rows:
            for c in neededColumns:
                returning[c] = min(returning[c], int(r[c]))
    elif func == "avg":
        for r in rows:
            for c in neededColumns:
                returning[c] += int(r[c])
        returning = [i/len(rows) for i in returning]
    elif func == "sum":
        for r in rows:
            for c in neededColumns:
                returning[c] += int(r[c])
    elif func == "cnt":
        for r in rows:
            for c in neededColumns:
                returning[c] += 1
    else:
        print("Error: Function "+func+" not found.")
        return
    [ispis.append(i) for cnt,i in enumerate(returning) if cnt in neededColumns]
    end = time.time()
    print(ispis)
    print("Time taken: ")
    print(end - start)
    
    
    

def parseCondition(param):
    try:
        conditions = re.split(r'\sAND\s|\sOR\s', param)
        conditions = [condition.strip() for condition in conditions]
        operators = re.findall(r'\s(AND|OR)\s', param)
        return conditions, operators
    except Exception as e:
        print(e)

if __name__ == '__main__':
    global state
    state = 0
    proccesInput()