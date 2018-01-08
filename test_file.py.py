import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import ast
import itertools
import main_recommend


user_feat = pd.read_csv('user_features.csv')


user_feat['Calories'] = np.random.randint(150,500, size=len(user_feat))
user_feat['meal_size_rating'] = pd.DataFrame(np.random.randint(0,3, size = (len(user_feat),1)))
user_feat['previous_meal_size'] = pd.DataFrame(np.random.randint(0,3, size = (len(user_feat),1)))


spice_feat = pd.read_excel('test4.xls')
spice_feat = spice_feat.iloc[:,:7]
#print spice_feat
#food user rating table
food_user = pd.DataFrame(np.random.randint(low=0, high=2, size=(len(spice_feat),len(user_feat))),columns=user_feat.user_guid)
food_user.index  =  spice_feat['food_id']

def nor_age(age):
    
    if(age<=10):
        return 1
    elif(age>10 and age <=18):
        return 2
    elif(age>18 and age <=25):
        return 3
    elif(age>25 and age <=35):
        return 4
    elif(age>35 and age <=40):
        return 5
    elif(age>40 and age <=50):
        return 6
    elif(age>50 and age<=60):
        return 7
    else:
        return 8
    
    

s_dict = {"M":1,"F":5 }
l_dict = {'Jammu & Kashmir':2, 'Punjab & Haryana':5, 'Rajasthan':8, 'Maharashtra':10, 'South India':15}
user_feat['Age'] = user_feat['Age'].apply(nor_age)
user_feat  = user_feat.replace({"Sex":s_dict})
user_feat  = user_feat.replace({"Location":l_dict})

new_user_feat = pd.read_csv('new_user_feat.csv')


next_day = 1;

while next_day :
    entry = input('type 1 if you want users recommendation or type 0 if it is next_day')

    if entry==1:
        user_id = input('enter the user_id')
        recommendation = main_recommend.main_recommendation(new_user_feat,user_feat,user_id)
        
    elif entry == 0:
        main_recommend.change_recommendation(user_feat,spice_feat,new_user_feat)
    else:
        print 'wrong entry try again'

    again = input('want to try again,press 1 else quit')
    if again == 1:
        next_day = 1;

    else:
        next_day = 0 


