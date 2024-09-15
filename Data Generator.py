import random
import time
import datetime
from datetime import date
import os
import pandas as pd


#Generate a csv file for each manager
def create_table(manager):
    
    df = pd.DataFrame(columns=['name',
        'calls',
        'unique_calls',
        'minutes',
        'yaware',
        'team',
        'date'])


    directory = os.getcwd()
    folder_exists = os.path.isdir(rf'{directory}\Managers')

    if not folder_exists:
        os.mkdir(rf"{directory}\Managers")
    
    df.to_csv(rf'{directory}\managers_2\{manager}.csv', index = False)



#Generate data for each manager
def generate_data(manager, start_date, working_days, team):
    df = pd.read_csv(rf'managers_2\{manager}.csv')
    
    new_data = {
        'name' : [],
        'calls' : [],
        'unique_calls' : [],
        'minutes' : [],
        'yaware' : [],
        'team' : [],
        'date' : []
    }


    name = manager
    date = start_date
    
    for _ in range(working_days):

        #Generate Data
        calls = random.randint(130,280)
        unique_calls = calls - random.randint(0,15)
        minutes = random.randint(5,80)

        yaware_minutes = random.randint(390,540) #Worktime ranges from 6:30 to 9:00
        yaware_h, yaware_m = divmod(yaware_minutes,60) #Convert the minutes to h:mm pattern
        yaware = (f"{yaware_h}.{yaware_m}")

        date_ = date.strftime(f" %d/%m/%Y") #Convert it to Brazil pattern
        

        #Append data to dictionary
        new_data['name'].append(name)
        new_data['calls'].append(calls)
        new_data['unique_calls'].append(unique_calls)
        new_data['minutes'].append(minutes)
        new_data['yaware'].append(yaware)
        new_data['team'].append(team)
        new_data['date'].append(date_)


        weekday = date.weekday() #Get the weekday

        if team == "mon_fri":
            if weekday == 4: #if the weekday is friday
                date += datetime.timedelta(days=3) #the next workday will be monday
            
            else:
                date += datetime.timedelta(days=1)


        elif team == "tue_sat":
            if weekday == 5: #if the weekday is saturday
                date += datetime.timedelta(days=3) #the next workday will be monday
            
            else:
                date += datetime.timedelta(days=1)



    #Write dictionary into the CSV file and save it
    df = pd.DataFrame(new_data)
    df.to_csv(rf'managers_2\{manager}.csv',  mode='a', index=False, header = False)






#16 Account managers
managers = ["Fintan Wilcox",
"Arianna Blaese",
"Linda Hoffman",
"Aidan Riddle",
"Zayd Cross",
"Virginia Meadows",
"Milly Adkins",
"Alanna Mills",
"Lacie Howe",
"Elaine Roberson",
"Antonio Blanchard",
"Barbara Roach",
"Zayn Le",
"Lucy Peck",
"Keelan Johns",
"Josh Nichols"]


#Divide the managers into 2 groups
team_a = managers[:8] # First half works from Monday to Friday
team_b = managers[8:] # Second half works from Tuesday to Saturday


for manager in managers:
    working_days = 260

    if manager in team_a:
        start_date = date(2024, 1, 1)
        team = "mon_fri"

    if manager in team_b:
        start_date = date(2024, 1, 2)
        team = "tue_sat"

    create_table(manager)
    generate_data(manager,start_date, working_days,team)
    




#Generate 1 CSV for all managers stats
directory = os.getcwd()
csv_files = os.listdir(rf'{directory}\managers_2')


dfs = []

for file in csv_files:
    df = pd.read_csv(rf'{directory}\managers_2\{file}')
    dfs.append(df)


merged_df = pd.concat(dfs, ignore_index=True)
merged_df.to_csv(rf'{directory}\managers_2\_All Managers.csv', index=False)
