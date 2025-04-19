
import random
import pandas as pd

data = pd.read_csv('list.csv', encoding = 'UTF-8')

team_list=[]

team = int(input("How much team? : "))
max_person = int(input("How many person per team? : "))

grade1 = []
grade2 = []
for i in range (len(data)):
    if data['grade'][i] == 1:
        grade1.append(data['name'][i])
    else:
        grade2.append(data['name'][i])

random.shuffle(grade1)
random.shuffle(grade2)

for i in range (0,team):
    team_list.append([])

for i in range (len(grade1)):
    team_list[i] = [grade1[i]]

for i in range (len(grade2)):
    if i >= team:
        team_list[i-team].append(grade2[i])
    else:
        team_list[i].append(grade2[i])

for i in range (len(team_list)):
    print('team', i+1, ' : ', team_list[i])
