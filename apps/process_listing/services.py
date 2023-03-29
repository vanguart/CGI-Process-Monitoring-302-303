from main.models import Process,Task

#function that returns all processes in the data base acording to input parameters
def getAllProcessesInDB(InicialDate, EndDate, label, state,):
    
    allLabels = False
    allDates = False
    allStates = False
    
    if label == "noTag":
       allLabels = True
       
    if InicialDate == None and EndDate == None:
        allDates = True
        
    
    if state == "noState":
        allStates = True
    
        
    result = []
    result = Process.objects.all()
    
    if result.count() == 0:
        print("there is nothing in the database")
        return None
    
    if not allLabels:
        result = filterListByLabels(result, label)
   
    if not allStates:
        result = filterListByState(result, state)
        
    if not allDates:
        result = filterListByDate(result,InicialDate, EndDate)

    return result
      
#function that filter a list by Tags
def filterListByLabels(inputList,label):
              
     for i in inputList:
         if i.label != label:
             inputList.remove(i)
     
     return inputList
 
#function that filter a list by States
def filterListByState(inputList,state):
              
    for i in inputList:
        if i.state != state:
            inputList.remove(i)
     
    return inputList
 
 
 #function that gilter a list by Dates

def filterListByDate(inputList, InicialDate, EndDate):
     
    for i in inputList:
        if InicialDate > i.inicialDate or EndDate < i.finalDate:
            inputList.remove(i)
            
    return inputList

#function that returns all task in a specific process
def getAllTasksInAProcesses(processId):
    
    result = []
    used = set()   
    tasks = Task.objects.all()
    
    if tasks.count() == 0:
        print("there is nothing in the database")
        return None
 
    for i in tasks:
        if i.idTaskConfiguration.idProcessConfiguration != processId:
            if used.contains(i.idTaskConfiguration):
                continue
            else:
                used.add(i.idTaskConfiguration)
                result.append(i)
                