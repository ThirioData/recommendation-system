import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import ast
import itertools
import main_recommend


user_feat = pd.read_csv('user_features.csv')


#user_feat['Calories'] = np.random.randint(150,500, size=len(user_feat))
#user_feat['meal_size_rating'] = pd.DataFrame(np.random.randint(0,3, size = (len(user_feat),1)))
#user_feat['previous_meal_size'] = pd.DataFrame(np.random.randint(0,3, size = (len(user_feat),1)))


spice_feat = pd.read_excel('test4.xls')
spice_feat = spice_feat.iloc[:,:7]
#print spice_feat
#food user rating table
#food_user = pd.DataFrame(np.random.randint(low=0, high=2, size=(len(spice_feat),len(user_feat))),columns=user_feat.user_guid)
#food_user.index  =  spice_feat['food_id']

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
    

def user_feat_preprocess(user_feat):
    s_dict = {"M":1,"F":5 }
    l_dict = {'Jammu & Kashmir':2, 'Punjab & Haryana':5, 'Rajasthan':8, 'Maharashtra':10, 'South India':15}
    user_feat['Age'] = user_feat['Age'].apply(nor_age)
    user_feat  = user_feat.replace({"Sex":s_dict})
    user_feat  = user_feat.replace({"Location":l_dict})
    return user_feat
#user_feat1 = pd.read_csv('user_features.csv')
#user_feat = user_feat_preprocess(user_feat)

new_user_feat = pd.read_csv('new_user_feat.csv')

def generate_id(user_guid_list):
    return max(user_guid_list)+1
    
new_user = input('press 1 to add new user, 0 to continue with existing user')
while(new_user):
    user_guid = generate_id(user_feat['user_guid'])
    user_name = raw_input('enter the name ')
    age = input('enter the age ')
    sex = raw_input('gender M or F ')
    loc = raw_input('State u belongs to(Jammu & Kashmir:2, Punjab & Haryana:5, Rajasthan:8, Maharashtra:10, South India:15) ')
    nonveg = input('type1 for veg or 0 for non-veg/veg')
    #to be change later according to the formula
    calories = 300
    size = input('press 1 if you have any preference meal size?')
    meal_size_rating=1
    if(size==1):
        meal_size_rating = input('enter the meal size,0 for small ,1 for medium,2 for large')
    previous_meal_size = meal_size_rating  
    df = pd.DataFrame([[age,calories,loc,nonveg,sex,meal_size_rating,previous_meal_size,user_guid]],columns=['Age','Calories','Location','NonVeg','Sex','meal_size_rating','previous_meal_size','user_guid'])
    
    #print user_feat
    
    df = user_feat_preprocess(df) 
    #print df
    user_feat = pd.concat([user_feat,df],ignore_index=True)
    print user_feat
    user_feat.to_csv('user_features.csv',encoding='utf-8',index=False)
    #user_feat1 = pd.read_csv('user_features.csv')
    #user_feat = user_feat_preprocess(user_feat1) 
    
    last5ayreco = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    recom = [0,0,0]
    pastorder = pd.DataFrame([[user_guid,last5ayreco,last5ayreco,recom,recom,[0,0,0,0,0,0,0]]],columns=['user_guid','last_5_days_recommend','last_5_days_bought','recommends','bought','not_recommended'])
    new_user_feat = pd.concat([new_user_feat,pastorder],ignore_index=True)
    print new_user_feat
    new_user_feat.to_csv('new_user_feat.csv',encoding='utf-8',index=False)
    
    new_user = input('press 1 to add another new user, 0 to continue with existing users')
    


next_day = 1;

    

while next_day :
    entry = input('type 1 if you want users recommendation or type 0 if it is next_day')

    if entry==1:
        user_id = input('enter the user_id ')
        indexer = np.where(new_user_feat['user_guid']==user_id)[0]
        indexer = indexer[0]
        new_meal_size = main_recommend.main_recommendation(new_user_feat,user_feat,user_id)
        print new_meal_size
        order = input('enter the dish number to order ')
        print ('your previous meal size was '+str(user_feat.loc[indexer,'previous_meal_size']))
        print ('previous meal rating was '+str(user_feat.loc[indexer,'meal_size_rating'])+' so based on that your todays meal size is '+str(new_meal_size))
        user_feat.loc[indexer,'previous_meal_size'] = new_meal_size
        #print (spice_feat.loc[order,'count'])
        ## increase count of the ordered dish
        spice_feat.loc[order,'count'] = spice_feat.loc[order,'count']+1
        print ('your dish is ordered')
        # take feedback
        taste_rate = input('please give rating on the basis of taste. 0 = bad, 1 = fine, 2 = good')
        quantity_rate = input('please give rating on the basis of quantity. 0 = was less, 1 = satisfied, 2 = leftover')
        #update feedback
        user_feat.loc[indexer,'meal_size_rating'] = quantity_rate
        
    elif entry == 0:
        main_recommend.change_recommendation(user_feat,spice_feat,new_user_feat)
    else:
        print 'wrong entry try again'

    again = input('want to try again,press 1 else quit')
    if again == 1:
        next_day = 1;

    else:
        next_day = 0 


