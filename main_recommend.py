import pandas as pd
import numpy as np
import re
import os
from sklearn.cluster import KMeans
import ast
import itertools
import random
from random import randint
spice_feat = pd.read_excel('test4.xls')
spice_feat = spice_feat.iloc[:,:7]
def clustering_based(user_feat):    
    kmeans = KMeans(n_clusters = 5,random_state=0).fit(user_feat)
    user_feat['label'] = kmeans.labels_
    #print user_label
   
    user_feat = user_feat.sort_values(['label','Location'],ascending=[1,0])
    user = user_feat.drop_duplicates(subset=['Location','label'])
    user = user.groupby('label')['Location'].nlargest(3)
    return user,user_feat


def filter_food_loc(user_group,user_id,non_recom_list,user_feat,spice_feat):
    index = np.where(user_feat['user_guid']==user_id)[0][0]
    print index
    #print user_feat['label']
    user_label = user_feat.loc[index,'label']
    loc = user_group[user_label].tolist()
    newspice_feat = spice_feat.set_index('food_id')
    spice = newspice_feat[newspice_feat['State'].isin(loc)]
    #print spice
    return filter_food_cal(spice,non_recom_list,user_feat,user_id),loc 
    


def filter_food_cal(sspice,non_recom_list,user_feat,user_id):
    index = np.where(user_feat['user_guid']==user_id)[0][0]
    sspice = sspice[sspice['Type']==user_feat.loc[index,'NonVeg']]
   
    #sspice = sspice[sspice['Meal Size']==next_meal_size]
    #sspice = sspice[sspice['Place in Menu']==meal_type]
    
    #print spice
    s_spice =  sspice.sort_values('count',ascending=[0])
    s_index = s_spice.index[~s_spice.index.isin(non_recom_list)]
    #print ' rec ',non_recom_list
    new_spices = s_spice[s_spice.index.isin(s_index)]
    #print new_spices
    new_spices = new_spices[new_spices['Calories']<=user_feat.loc[index,'Calories']]
    return new_spices



def recommendation(user_group,user_id,non_recom_list,user_feat,spice_feat):
    new_spices,loc = filter_food_loc(user_group,user_id,non_recom_list,user_feat,spice_feat)
    
    recommend = []
    
    index = np.where(user_feat['user_guid']==user_id)[0][0]
    new_spices2 = spice_feat[spice_feat['Type']==user_feat.loc[index,'NonVeg']]   
    new_spices2 = new_spices2[new_spices2['Calories']<=user_feat.loc[index,'Calories']]
    print new_spices2
    
    #even in random,at least 2 constraints are there, calory and veg/non-veg and maybe location(to be confirmed) too
    x = randint(0,9)
    x=5
    if(x==5):
        #print ('random')  #to test
        y = randint(0,len(new_spices2)-1)
        #y = random.choice(new_spices2.index.values)
        print y
        print len(new_spices2)
        #print new_spices2.index.values
        print new_spices2.index[y]
        index_to_append = new_spices2.index[y]
        #print random_feat.loc[index_to_append,'food_id']
        recommend.append(new_spices2.loc[index_to_append,'food_id'])
    
    
        for i in range(min(4,len(new_spices))):
            recommend.append(new_spices.index[i])
    
        if(len(recommend)<5):
            other_state_spice = spice_feat[spice_feat['State'].isin(loc)==False]
    
            other_state_spice = other_state_spice.sort_values('count',ascending= [0])
            new_other_state = other_state_spice[~other_state_spice.index.isin(non_recom_list)]

            if(len(new_other_state)>=(5-len(recommend))):
                for i in range(5-len(recommend)):
                    recommend.append(new_other_state.index[i])
                    
        if(len(recommend)<5):            
            newlymade_spice = spice_feat.sort_values('count',ascending = [0])            
            for i in range(5-len(recommend)):
                recommend.append(newlymade_spice.index[i])
            
    else:
        #print ('not random')
        for i in range(min(5,len(new_spices))):
            recommend.append(new_spices.index[i])
    
        if(len(recommend)<5):
            other_state_spice = spice_feat[spice_feat['State'].isin(loc)==False]
    
            other_state_spice = other_state_spice.sort_values('count',ascending= [0])
            new_other_state = other_state_spice[~other_state_spice.index.isin(non_recom_list)]
            if(len(new_other_state)>=(5-len(recommend))):
                for i in range(5-len(recommend)):
                    recommend.append(new_other_state.index[i])
        if(len(recommend)<5):            
            newlymade_spice = spice_feat.sort_values('count',ascending = [0])            
            for i in range(5-len(recommend)):
                recommend.append(newlymade_spice.index[i])
    
    return recommend


def convert_list(row):
    #x = str(row['last_5_days_recommend'])
    y = str(row['last_6_days_bought'])
    #if isinstance(x,basestring):
    #    x = ast.literal_eval(x)
    if isinstance(y,basestring):
        y = ast.literal_eval(y)    
        
    #l1 =  list(itertools.chain.from_iterable(x))
    l2 =  list(itertools.chain.from_iterable(y)) 
    #print l1+l2
    return l2


def change_last_recommend(x,y):
    #print (row['last 5 days recommend'])
    new_recommend = []
    #print type(x) ,y,count 
    if isinstance(x,basestring):
        x = ast.literal_eval(x)
    if isinstance(y,basestring):
        y = ast.literal_eval(y)    
    for i in range(4):
        new_recommend.append(x[i+1])
    new_recommend.append(y)
    #print new_recommend
    return str(new_recommend)


def recommend_items(user_id,non_recom_list,user,user_feat,spice_feat):
    #print type(non_recom_list)
    l1 = recommendation(user,user_id,non_recom_list,user_feat,spice_feat)
    
    #l2 = recommendation_content(user_id,spice_feat,user_rating,non_recom_list,user_feat,output_df)
    
    return str(l1)


def change_type(x):
    if isinstance(x,basestring):
        x = ast.literal_eval(x)
    return x


def next_day_recommendation(user_feat,new_user_feat,spice_feat):        #,user_rating):
    new_user_feat['last_6_days_recommend'] = new_user_feat.apply(lambda x: change_last_recommend(x['last_6_days_recommend'], x['recommends']), axis=1)
    new_user_feat['last_6_days_bought'] = new_user_feat.apply(lambda x: change_last_recommend(x['last_6_days_bought'], x['bought']), axis=1)
    new_user_feat['not_recommended'] = new_user_feat.apply(convert_list,axis=1)
    print new_user_feat['last_6_days_recommend'][0]
    print new_user_feat['last_6_days_bought'][0] 
    print new_user_feat['not_recommended'][0]
    user_group ,user_feat = clustering_based(user_feat)
    #spice = np.array(spice_feat.iloc[: ,0:4])
    #outputdf  = content_based_reco(user_rating, spice)
    new_user_feat['not_recommended'] = new_user_feat.apply(lambda x:change_type(x['not_recommended']),axis=1)
    #new_user_feat['not_recommended'].to_csv('not_recommended.csv',encoding='utf-8',index = False)
    #print new_user_feat
    new_user_feat['recommends'] = new_user_feat.apply(lambda x:recommend_items(x['user_guid'],x['not_recommended'],user_group,user_feat,spice_feat),axis=1)
    print new_user_feat
    return new_user_feat

def main_recommendation(new_user_feat,user_feat,user_id):      #,user_rating):
   
    index = np.where(new_user_feat['user_guid']==user_id)[0]
    
    
    
    x =  new_user_feat.loc[index[0],'recommends']
        
        
    if isinstance(x,basestring):
        x = ast.literal_eval(x)   
    
    temp_list =  x#list(itertools.chain.from_iterable(x))
    
        
        
    
    dish1 = spice_feat.loc[temp_list[0],'Dish']
    dish2 = spice_feat.loc[temp_list[1],'Dish']
    dish3 = spice_feat.loc[temp_list[2],'Dish']
    print (str(temp_list[0])+' = '+dish1+','+str(temp_list[1])+'='+dish2+','+str(temp_list[2])+'='+dish3)
        
    previous_rating = user_feat.loc[index[0],'meal_size_rating']
    previous_size = user_feat.loc[index[0],'previous_meal_size']
    next_meal_size = previous_size

    if(previous_rating==0 and previous_size<2):
        next_meal_size = previous_size + 1
    elif (previous_rating==2 and previous_size>0):
        next_meal_size = previous_size - 1
        
        
    #meal_type = input('enter the meal type(0,1,2,3)')
    
    return next_meal_size

def change_recommendation(user_feat,spice_feat,new_user_feat):
    new_user_feat = next_day_recommendation(user_feat,new_user_feat,spice_feat)
    new_user_feat.to_csv('new_user_feat.csv',encoding='utf-8',index = False)       




