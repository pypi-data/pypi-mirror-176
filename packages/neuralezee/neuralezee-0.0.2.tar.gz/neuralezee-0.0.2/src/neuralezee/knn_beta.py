class knn:
    def __init__(this):   # constructor to Knn 
    
        this.shortest_distances = [] #intializing variables
        
        this.calculated_shortest_distance=0

        this.result = []

        this.k = 0
    
    def Hyperparameter(this,k_value = 3):  # intializing value of Hyperparameter = k , if not assigned we can use default parameter as 3
        
        this.k = k_value    
    
    def __MINKOWSKI__DISTANCE__(this,_value_1_,_value_2_,POWER=2): # Finding the shortest Distance using Minkowski distance
        
        return sum(abs(x - y)**POWER 
        
        for x , y in 
        
        zip(_value_1_,_value_2_))**(1/POWER)
    
    def fit(this,traningInput,traningOutput): #fiting training data into model
        
        this._Training_Data_ = traningInput

        this._Traning_Output = traningOutput

    def predict(this,testingData,Euclidean_or_Manhattan=2): # By default its gona take Euclidean

        String = str(this._Traning_Output)

        for queryPoint in testingData:
            
            this._Predicted_Result = list(String.replace(",","").replace("[","").replace("]","").replace("'","").replace(" ","").strip()) # resetting the result
            
            for featureVector in this._Training_Data_:
                
                this.calculated_shortest_distance= this.__MINKOWSKI__DISTANCE__(queryPoint,featureVector,Euclidean_or_Manhattan)

                this.shortest_distances.append(round(this.calculated_shortest_distance,3)) #finding weight = 1/d 

            sorted_outcome=this.insertion_sort(this.shortest_distances,this._Predicted_Result)
            this.shortest_distances=[]
            answer = this.Finding_Mode(sorted_outcome)
            this.result.append(answer) #result is sending
            this._Predicted_Result=[]


    def insertion_sort(this,shortest_distances,_Predicted_Result): 
        for i in range(1,len(shortest_distances),1):
            slider = i
            while (shortest_distances[slider] < shortest_distances[slider-1] and slider > 0 ):
                shortest_distances[slider] , shortest_distances[slider-1] = shortest_distances[slider-1], shortest_distances[slider]
                _Predicted_Result[slider] , _Predicted_Result[slider-1] = _Predicted_Result[slider-1],_Predicted_Result[slider] 
                slider-=1
        return _Predicted_Result 
    
    def max(this,a,b):
        if a>b:
            return a
        return b       
    def Finding_Mode(this,_Predicted_Result):
        arr = _Predicted_Result[this.k]
        dictnary={}
        for i in arr:       #intializing the dict 
            dictnary[i]=0
        for i in arr:      #finding values of same occurances
            dictnary[i] +=1
        values = dictnary.values()
        compareList=list(values)
        maximum = 0
        for i in range(0,len(compareList),1):
            maximum = max(compareList[i],maximum)
        for i in arr:
            if(dictnary[i]==maximum):
                result = i 
                break
        return result
    def distance(this):
       return this.result



