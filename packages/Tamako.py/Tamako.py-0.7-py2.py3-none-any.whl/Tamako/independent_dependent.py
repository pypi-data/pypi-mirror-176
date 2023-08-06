import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
data=pd.read_csv("data.csv")  #Reading the csv file...
print("Data is: ")
data.columns=['Num_of_Symptoms','Amount_of_Activity', 'Amount_of_sleep','Amount_of_food_consumed', 'Apetite', 'Skin_Reaction', 'Other_Factors']
data.Num_of_Symptoms = data.Num_of_Symptoms.astype(str)
print(data)  #Printing the data..

x=data.loc[:,"Amount_of_Activity":]    #Independent variable
y=data.Num_of_Symptoms                 #Depenedent variable
print("Ind: ",x)
print("Dep: ",y)

pd.plotting.scatter_matrix(data.loc[:,"Amount_of_Activity":"Other_Factors"],diagonal="kde") #Function to plot
plt.tight_layout()
plt.show() #Display the graph..

df=pd.read_csv("data.csv")
sns.lmplot(x="x2",y="x1",data=df) #x: x-axis content
sns.lmplot(x="x3",y="x1",data=df) #y: y-axis conteny
sns.lmplot(x="x4",y="x1",data=df)
sns.lmplot(x="x5",y="x1",data=df)
sns.lmplot(x="x6",y="x1",data=df)
sns.lmplot(x="x7",y="x1",data=df)

ax=data[['Num_of_Symptoms','Amount_of_Activity', 'Amount_of_sleep','Amount_of_food_consumed', 'Apetite', 'Skin_Reaction', 'Other_Factors']].plot()
ax.legend(loc='best') #set the legend
print(x.apply(np.std)) #Deviation in independent variables
plt.show()