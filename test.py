
import file
import pandas as pd
import numpy as numpy

user_feat = pd.read_csv('user_feat.csv')
spice_feat = pd.read_csv('spice_feat.csv')

next_day = 1;


while next_day :
	entry = input('type 1 if you want users recommendation or type 0 if it is next_day')

	if entry==1:
		user_id = input('enter the user_id')
		recommendation = file.recommed(user_id)
		print recommendation
	elif entry == 0:
		file.change_recommendation(user_feat,spice_feat)
	else:
		print 'wrong entry try again'

     again = input('want to try again,press 1 else quit')
     if again == 1:
         next_day = 1;

     else:
         next_day = 0 

















