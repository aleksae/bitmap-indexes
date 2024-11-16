import random


factFile = open("facts.txt", "w")
d1File = open("d11.txt", "w")
d2File = open("d21.txt", "w")

dataArr = []
lenArr = []
dataD1 = []
lenD1 = []
for i in range(1,10):
    for j in range(1, 251):
        for k in range(1,251):
            rand1 = random.randrange(1, 100)
            rand2 = random.randrange(1, 100)
            data = '(' + str(i*j*k) + ',' + str(j) + ',' + str(k) + ',' + str(rand1) + ',' + str(rand2) + ')\n'
            dataArr.append(data)
            lenArr.append(str(len(data)))

for i in range(1,251):
    dataD1.append('(' + str(i) + ',' + "A"+str(i) + ')\n')
    lenD1.append(str(len(dataD1[-1])))

factFile.write(','.join(lenArr)+'\n')
for data in dataArr:
    factFile.write(data)
factFile.close()
d1File.write(','.join(lenD1)+'\n')
for data in dataD1:
    d1File.write(data)
d1File.close()
d2File.write(','.join(lenD1)+'\n')
for data in dataD1:
    d2File.write(data)
d2File.close()

    

