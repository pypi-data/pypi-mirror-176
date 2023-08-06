import numpy as np
from scipy.stats import mode
 
class KNN:
   
   #Minkowski Distance , When Power  = 1 it Will calculate Manhattan Distance 
   #and For Power = 2 it will calculate Euclidean Distance 

 def Minkowski(self,Trained_features,Query_Point,power):

     return (1/power)**(np.sum((Trained_features-Query_Point)**power))

 #Predicting the Query Points Based on the Shortest Distance and Hyperparameter k
 #Required Arguments are Traning_Data, Traning_Class_Label , Testing_Data, k ,power

 def predict(self,Traning_Data, Traning_Class_Label , Testing_Data, k ,power):

    Predicted_Class_Labels = []  # Intially Empty < We will Add Outcome when Calculated > 
     
    #Calculating query distance while traversing through each training data one by one 

    for query_point in Testing_Data: 
         
        #List to store shorted distances
        Shorted_Distance = []  # Intially Empty < We will Add Shorted distance when Calculated >
         
        #Calculating shortest distance from every traning features
        for train_feature_index in range(len(Traning_Data)): 
            
            distances = self.Minkowski(np.array(Traning_Data[train_feature_index,:]) ,query_point,power) 
            
            #Calculating the  distance between qurey points and traning features
            Shorted_Distance.append(distances) 
        Shorted_Distance = np.array(Shorted_Distance) 
         
        #Sorting the array while preserving the index
        #Keeping the first K datapoints
        dist = np.argsort(Shorted_Distance)[:k] 
         
        #Labels of the K datapoints from above
        labels = Traning_Class_Label[dist]
         
        #Majority voting from the shortes distance metric
        lab = mode(labels) 
        lab = lab.mode[0]
        Predicted_Class_Labels.append(lab)
 
    return Predicted_Class_Labels
