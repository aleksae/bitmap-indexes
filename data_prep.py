import random
from urllib.request import urlopen
import json
import sys

'''response = urlopen('https://api.openf1.org/v1/drivers')
drivers = json.loads(response.read().decode('utf-8'))
file1 = open("drivers.txt", "w") 
cnt = 1
max_size = 79
to_write = []
sizes = []
unique = set()
for driver in drivers:
    if driver['driver_number'] not in unique:
        res = '(' + str(cnt) + ',' + driver['full_name'] + ',' + str(driver['driver_number']) + ')'
        res += '\n'
        cnt+=1
        sizes.append(str(len(res)))
        to_write.append(res)
        unique.add(driver['driver_number'])
    #file1.writelines(res)

file1.write(','.join(sizes))
file1.write('\n')
for write in to_write:
    file1.write(write)
file1.close()

#test read
file1 = open("drivers.txt", "r") 
driverPositions = file1.readline().split(',')
DataStart = file1.tell()
desiredId = 4
file1.seek(DataStart + sum([int(size) for size in sizes[:desiredId-1]])+desiredId-1)
print(file1.readline())'''



response = urlopen('https://api.openf1.org/v1/meetings?year=2023')
meetings = json.loads(response.read().decode('utf-8'))
racesFile = open("races.txt","w")
resultsFile = open("results.txt","w")
dataRaces = []
dataResults = []
lenRaces = []
lenResults = []
counter = 1
raceCounter = 1
for meeting in meetings:
    if(meeting['meeting_key'] != 1140):
        dataRace = ''
        if(meeting['meeting_key'] == 1224):
            dataRace1 = '(' + str(raceCounter) + ',Sao Paulo Grand Prix,' + str(meeting['year']) +')\n'
            raceCounter+=1
            dataRace2 = '(' + str(raceCounter) + ',Sao Paulo Grand Prix,' + str(2022) +')\n'
            raceCounter+=1
            dataRace3 = '(' + str(raceCounter) + ',Sao Paulo Grand Prix,' + str(2021) +')\n'
            raceCounter+=1
            dataRace4 = '(' + str(raceCounter) + ',Sao Paulo Grand Prix,' + str(2020) +')\n'
        else: 
            dataRace1 = '(' + str(raceCounter) + ',' + str(meeting['meeting_name']) + ',' + str(meeting['year']) +')\n'
            raceCounter+=1
            dataRace2 = '(' + str(raceCounter) + ',' + str(meeting['meeting_name']) + ',' + str(2022) +')\n'
            raceCounter += 1
            dataRace3 = '(' + str(raceCounter) + ',' + str(meeting['meeting_name']) + ',' + str(2021) +')\n'
            raceCounter += 1
            dataRace4 = '(' + str(raceCounter) + ',' + str(meeting['meeting_name']) + ',' + str(2020) +')\n'
        dataRaces.append(dataRace1)
        dataRaces.append(dataRace2)
        dataRaces.append(dataRace3)
        dataRaces.append(dataRace4)
        lenRaces.append(str(len(dataRace1)))
        lenRaces.append(str(len(dataRace2)))
        lenRaces.append(str(len(dataRace3)))
        lenRaces.append(str(len(dataRace4)))
        for cnt in range(1,21):
            
            raceCounter -= 3
            driver = random.randrange(1,48)
            dataResult1 = '('+str(counter) +','+ str(raceCounter) + ',' + str(driver) + ',' + str(cnt) + ')\n'
            counter+=1
            raceCounter += 1
            driver = random.randrange(1,48)
            dataResult2 = '('+str(counter) +','+ str(raceCounter) + ',' + str(driver) + ',' + str(cnt) + ')\n'
            counter+=1
            raceCounter += 1
            driver = random.randrange(1,48)
            dataResult3 = '('+str(counter) +','+ str(raceCounter) + ',' + str(driver) + ',' + str(cnt) + ')\n'
            counter+=1
            raceCounter += 1
            driver = random.randrange(1,48)
            dataResult4 = '('+str(counter) +','+ str(raceCounter) + ',' + str(driver) + ',' + str(cnt) + ')\n'
            counter+=1
            dataResults.append(dataResult1)
            dataResults.append(dataResult2)
            dataResults.append(dataResult3)
            dataResults.append(dataResult4)
            lenResults.append(str(len(dataResult1)))
            lenResults.append(str(len(dataResult2)))
            lenResults.append(str(len(dataResult3)))
            lenResults.append(str(len(dataResult4)))
        raceCounter+=1
racesFile.write(','.join(lenRaces))
racesFile.write('\n')
for dataRace in dataRaces:
    racesFile.write(dataRace)
racesFile.close()
resultsFile.write(','.join(lenResults))
resultsFile.write('\n')
for dataResult in dataResults:
    resultsFile.write(dataResult)
resultsFile.close()



