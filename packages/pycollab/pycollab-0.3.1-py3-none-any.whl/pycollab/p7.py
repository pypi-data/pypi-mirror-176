import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

import time

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("/content/drive/MyDrive/AML/SampleData.csv")

data.describe()

data

def MCModelv1(data, alpha, e, epsilon, budget, reward):
    # Define the States
    Ingredients = list(set(data['Ingredient']))
    # Initialise V_0
    V0 = data['V_0']
    data['V'] = V0
    output = []
    output1 = []
    output2 = []
    actioninfull = []
    #Interate over the number of episodes specified
    for e in range(0,e):
        
        episode_run = []
#Introduce epsilon-greedy selection, we randomly select the first episode as 
#V_0(a) = 0 for all actions
        epsilon = epsilon
        if e == 0:
            for i in range(0,len(Ingredients)):
                episode_run = np.append(episode_run,np.random.random_integers
                          (low = 1, high = sum(1 for p in data.iloc[:, 0] 
                                               if p == i+1 ), size = None))
            episode_run = episode_run.astype(int)
        
        else:
            for i in range(0,len(Ingredients)):
                greedyselection = np.random.random_integers(low = 1, high =10)
                if greedyselection <= (epsilon)*10:
                    episode_run = np.append(episode_run,np.random.random_integers
                              (low = 1, high = sum(1 for p in data.iloc[:, 0] 
                                                   if p == i+1 ), size = None))
                else:
                    data_I = data[data['Ingredient'] == (i+1)] 
                    MaxofVforI = data_I[data_I['V'] == data_I['V'].max() ]['Product']
                    #If multiple max values, take first
                    MaxofVforI = MaxofVforI.values[0]
                    episode_run = np.append(episode_run, MaxofVforI)
                    
                episode_run = episode_run.astype(int)
                                          
        episode = pd.DataFrame({'Ingredient' : Ingredients, 
                                'Product': episode_run})    
        episode['Merged_label'] =  (episode['Ingredient']*10 + 
                                    episode['Product']).astype(float)
        data['QMerged_label'] = (data['QMerged_label']).astype(float)
        data['Reward'] = reward
        episode2 =  episode.merge(data[['QMerged_label','Real_Cost','Reward']], 
                left_on='Merged_label',right_on='QMerged_label', how = 'inner')
        data = data.drop('Reward',1)
        
        # Calculate our terminal reward
        if(budget >= episode2['Real_Cost'].sum()):
            Return = 1  
        else:
            Return = -1 
        episode2 = episode2.drop('Reward',1)
        episode2['Return'] = Return
        
        # Apply update rule to actions that were involved in obtaining terminal reward 
        data = data.merge(episode2[['Merged_label','Return']], 
                          left_on='QMerged_label',right_on='Merged_label', 
                          how = 'outer')
        data['Return'] = data['Return'].fillna(0)
        for v in range(0,len(data)):
            if data.iloc[v,7] == 0:
                data.iloc[v,5] = data.iloc[v,5] 
            else:
                data.iloc[v,5]  = data.iloc[v,5]  + alpha*((data.iloc[v,7]/len(Ingredients)) - data.iloc[v,5] )
                
        # Output table    
        data = data.drop('Merged_label',1)
        data = data.drop('Return',1)
        
        # Output is the Sum of V(a) for all episodes
        output  = np.append(output, data.iloc[:,-1].sum())
        
# Output 1 and 2 are the Sum of V(a) for for the cheapest actions and rest respectively
# I did this so we can copare how they converge whilst applying to such a small sample problem
        output1 = np.append(output1, data.iloc[[1,2,4,8],-1].sum())
        output2 = np.append(output2, data.iloc[[0,3,5,6,7],-1].sum())
        
# Ouput to optimal action from the model based on highest V(a)
        action = pd.DataFrame(data.groupby('Ingredient')['V'].max())
        action2 = action.merge(data, left_on = 'V',right_on = 'V', how = 'inner')
        action3 = action2[['Ingredient','Product']]
        action3 = action3.groupby('Ingredient')['Product'].apply(lambda x :x.iloc[np.random.randint(0, len(x))])
        
# Output the optimal action at each episode so we can see how this changes over time
        actioninfull = np.append(actioninfull, action3)
        actioninfull = actioninfull.astype(int)
        
        # Rename for clarity
        SumofV = output
        SumofVForCheapest = output1
        SumofVForExpensive = output2
        OptimalActions = action3
        ActionsSelectedinTime = actioninfull
        
    return(SumofV, SumofVForCheapest, SumofVForExpensive, OptimalActions, 
           data, ActionsSelectedinTime)

#Run Model on sample variables

alpha = 0.1
num_episodes = 100
epsilon = 0.5
budget = 30

# Currently not using a reward
reward = [0,0,0,0,0,0,0,0,0]

start_time = time.time()

Mdl = MCModelv1(data=data, alpha = alpha, e = num_episodes,epsilon = epsilon, 
                budget = budget, reward = reward)

print("--- %s seconds ---" % (time.time() - start_time))

print(Mdl[3])

Mdl[4]

plt.plot(range(0,num_episodes), Mdl[0])
plt.title('Sum of V for all Actions at each Episode')
plt.xlabel('Episode')
plt.ylabel('Sum of V')
plt.show()

plt.plot(range(0,num_episodes), Mdl[1],range(0,num_episodes), Mdl[2])
plt.title('Sum of V for the cheapest actions and others seperated at each Episode')
plt.xlabel('Episode')
plt.ylabel('Sum of V')
plt.show()

Ingredients = list(set(data['Ingredient']))
actions = pd.DataFrame()

for a in range(0, len(Ingredients)):   
    individualactions = []
    for i in range(0,num_episodes):    
        individualactions = np.append(individualactions, 
                                      Mdl[5][a+(i*(len(Ingredients)))])
    actions[a] = individualactions
    plt.plot(range(0,num_episodes), actions[a])
    plt.title('Product for Ingredient: ' + str(a+1))
    plt.xlabel('Episode')
    plt.ylabel('Product')
    plt.show()

actions2 = actions
actions2['Product1'] = actions2.iloc[:,0]+10
actions2['Product2'] = actions2.iloc[:,1]+20
actions2['Product3'] = actions2.iloc[:,2]+30
actions2['Product4'] = actions2.iloc[:,3]+40

actions3 = actions2.merge(data[['QMerged_label','Real_Cost']],
                          left_on = 'Product1',right_on = 'QMerged_label', 
                          how = 'left')
actions4 = actions3.merge(data[['QMerged_label','Real_Cost']],
                          left_on = 'Product2',right_on = 'QMerged_label', 
                          how = 'left')
actions5 = actions4.merge(data[['QMerged_label','Real_Cost']],
                          left_on = 'Product3',right_on = 'QMerged_label', 
                          how = 'left')
actions6 = actions5.merge(data[['QMerged_label','Real_Cost']],
                          left_on = 'Product4',right_on = 'QMerged_label', 
                          how = 'left')


actions6['Total_Cost'] = actions6.iloc[:,9] + actions6.iloc[:,11] + actions6.iloc[:,13] + actions6.iloc[:,15]
actions6 = actions6.iloc[:,[0,1,2,3,-1]]

actions6 = actions6.iloc[:num_episodes]

plt.plot(range(0,num_episodes), actions6['Total_Cost'])
plt.plot([0, num_episodes], [budget, budget], 'k-', lw=2)
plt.title('Total Real Cost of Best Products at each Episode')
plt.xlabel('Episode')
plt.ylabel('Total Real Cost (£)')
plt.ylim([0,budget+10])
plt.show()