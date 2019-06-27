#-------------------------------------------------TraceMaker--------------------------------------------
# In goal-oriented process mining, this tool is used to compute satisfaction level of
# all cases in terms of different goals using KPIs.
# The input of the tool is the list of all cases beside their trace and the table of all KPIs for all cases.
# Three values for each goal (Worst, threshold and target) are also required. The out put will be a table
# whose columns are satisfaction level of all goals and the rows are cases. This table, so called EnhancedLog is
# the main input of the Goal-oriented Process Discovery method introduced in ...

#-------------------------------------------------------------------------------------------------------
# The input of this tool is a csv files structured as follows:
# Column 1: Case identifier
# Column 2: Trace
# Column 3,...: KPI og Goal#1, KPI og Goal#2,...
# First row: Column header (The titles are not restricted)
# Second row: The "target value" of each goal (in the related column)
# Thirth row: The "threshold value" of each goal (in the related column)
# Fourgh row: The "worst value" of each goal (in the related column)
#--------------------------------------------------------------------------------------------------------

import csv
import os
import time
start_time = time.time()

# opens the table of traces beside KPIs for reading
KPIsTable=csv.reader(open("KPIsTable.csv", "r"))

# creates a csv file as output
#EhhancedLog=open("EnhancedLog.csv", "w")
EhhancedLog=csv.writer(open("EnhancedLog.csv","w",newline=''))

# constructs a list from the input table
ListOfKPIs=list(KPIsTable)

def satisfactionLevel(current, target, threshold, worst):
    if worst<target: # if the goal is maximization of a KPI
        if current>=threshold:
            SL=100*(0.5+0.5*(current-threshold)/(target-threshold))
        else:
            SL=100*0.5*(current-worst)/(threshold-worst)
    else:# if the goal is minimization of a KPI
        if current < threshold:
            SL = 100 * (0.5 +0.5* (threshold-current) / (threshold-target))
        else:
            SL = 100 * 0.5*(worst-current) / (worst-threshold)
    # if the current value exceeds than the target value or the worst value, satisfaction level will be 0 or 100, respectively
    SL = 0 if SL <= 0 else 100 if SL > 100 else SL
    return SL

# keeps the number of all cases and goals
NumberOfCases=len(ListOfKPIs) # the first 4 rows are Header and 3 KPI parameters
NumberOfGoals=len(ListOfKPIs[0])-2 # the first 2 columns are Case Identifier and Trace

# iteration to convert all current value of KPIs for all cases and all goals to satisfaction level using the satisfactionLevel function
for i in list(range(4,len(ListOfKPIs))):
    for j in list(range(2,len(ListOfKPIs[0]))):
          ListOfKPIs[i][j]= satisfactionLevel(float(ListOfKPIs[i][j]), float(ListOfKPIs[1][j]), float(ListOfKPIs[2][j]), float(ListOfKPIs[3][j]))

# The header line of resulting file is the same as of input file
EhhancedLog.writerows(ListOfKPIs[0:1])

# writes the resulting file from the lines of all cases in converted ListOfKPIs
EhhancedLog.writerows(ListOfKPIs[4:])



print("\nKPIsToGoals computed the satisfaction level of all goals for all cases successfully!")
print("\nEhhancedLog.csv was made in %s\ \n Number of cases= %d \n Number of goals= %d" % (os.getcwd(), len(ListOfKPIs)-4, len(ListOfKPIs[0])-2))

# report the execution time
print("\n\n--- execution time was %s seconds ---" % (time.time() - start_time))









