
import random
import pandas as pd

data = pd.read_csv('list.csv', encoding = 'UTF-8')

team_list=[]

team = int(input("How much team? : "))

grade1 = []
grade2 = []
for i in range (len(data)):
    if data['grade'][i] == 1:
        grade1.append(data['name'][i])
    else:
        grade2.append(data['name'][i])

random.shuffle(grade1)
random.shuffle(grade2)

for i in range(team):
    team_list.append([])

# grade1과 grade2를 합쳐서 한 명씩 팀에 배정
all_students = grade1 + grade2
for idx, name in enumerate(all_students):
    team_list[idx % team].append(name)

for i in range(len(team_list)):
    print('team', i+1, ' : ', team_list[i])
