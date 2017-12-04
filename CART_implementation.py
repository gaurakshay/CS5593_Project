
# Import necessary libraries
import numpy as np
import pandas as pd
# import matplotlib as plt

# Read in the file
df = pd.read_csv('coins.csv', index_col=0)
# Take a sample of the file for testing purposes
df_samp = df.sample(frac=0.01)
# Drop unused columns
df_samp = df_samp.drop(["coin", "date"], axis=1)
# Perform listwise deletion where 0 or NAN values exist
df_samp = df_samp[df_samp!=0]
df_samp = df_samp.dropna()

# 10 rows for testing purposes, at least 2 viable values will be 0
df_testing = df_samp.head(10)
df_testing.iloc[1]['viable'] = 0
df_testing.iloc[3]['viable'] = 0
df_testing.iloc[4]['viable'] = 0
df_testing.iloc[5]['viable'] = 0
df_testing.iloc[9]['viable'] = 0


# Compute Gini Index -- Intro to Data Mining pg. 158
def get_gini(data, col):
    viable = list(data.iloc[:,-1]) # Get the class variable
    count_t, count_f = 0, 0        # Instantiate count variables
    nrow = len(col)                # Get the number of rows in the column
    for i in viable:               # Count the number each of 1.0 and 0.0
        if(i == 1): count_t += 1
        else: count_f += 1
    return(1 - ((count_t/nrow)**2 + (count_f/nrow)**2))

# Return the best split point (index) for the node based on the class split
# Will need to use the index returned here to get the split value for each column
# Also returns the Gini index for the node at the best performing split
# Uses method on p. 162 of Intro to Data Mining (Tan, et.al) to select best split
def get_split(data):
    count_t, count_f = 0,0
    for i in data.iloc[:,-1]:   # Count number of each of 1.0 and 0.0 in dependent var.
        if(i == 1): count_t += 1
        else: count_f += 1
    x1, x2, x3, x4 = 0, count_t, 0, count_f
    # Create a new dataframe that will track viable (yes/no) for values below
    # and above each variable value
    d = pd.DataFrame(data=[(x1,x2),(x3,x4)], index=['yes', 'no'], columns=['lower','upper'])
    ind = 0
    gini_1 = 1 - ((d.iloc[0][0]/len(data))**2 + (d.iloc[1][0]/len(data))**2)
    gini_2 = 1 - ((d.iloc[0][1]/len(data))**2 + (d.iloc[1][1]/len(data))**2)
    gini = gini_1*((d.iloc[0][0]+d.iloc[1][0])/len(data)) + gini_2*((d.iloc[0][1]+d.iloc[1][1])/len(data))
    jeanne = gini
    # Perform the steps above for every record to get the best split index
    for i in range(1,len(data)):
        if(data.iloc[i][-1] == 1):
            d.loc['yes']['lower'] = d.loc['yes']['lower'] + 1
            d.loc['yes']['upper'] = d.loc['yes']['upper'] - 1
        if(data.iloc[i][-1] == 0):
            d.loc['no']['lower'] = d.loc['no']['lower'] + 1
            d.loc['no']['upper'] = d.loc['no']['upper'] - 1
        gini_1 = 1 - ((d.iloc[0][0]/len(data))**2 + (d.iloc[1][0]/len(data))**2)
        gini_2 = 1 - ((d.iloc[0][1]/len(data))**2 + (d.iloc[1][1]/len(data))**2)
        gini = gini_1*((d.iloc[0][0]+d.iloc[1][0])/len(data)) + gini_2*((d.iloc[0][1]+d.iloc[1][1])/len(data))
        if(gini < jeanne):  # keep the best Gini score and index, return those values
            jeanne = gini
            ind = i
    return(jeanne, ind)

# Split a node into two sub-nodes
# Records in less will have value in chosen predictor that is less
# than the split point
def split_nodes(data, col):
    # Create new nodes, left and right
    # left will hold records with values less than the chosen predictor split value
    # right will hold all other records
    left = pd.DataFrame(columns=list(data))
    right = pd.DataFrame(columns=list(data))
    gini, ind = get_split(data)
    value = data.iloc[ind][names[0]]
    # Split the node as given in the notes above
    for i in range(0, len(data)):
        if(data.iloc[i][col] < value):
            left = left.append(data.iloc[i])
            left = left.drop([col], axis=1)
        else:
            right = right.append(data.iloc[i])
            right = right.drop([col], axis=1)
    # Return the new child nodes
    return(left, right)

# Grow the tree
# proceed to split until a stopping criterion is met
def grow_tree(maximum_depth, minimum_records, data):
    depth = 0
    while True:
        if(depth <= max_depth):
            # Make leaf
            pass
        elif(len(data) <= min_records):
            # Make leaf
            pass
        elif(gini == 0):
            # Make leaf
            pass
        else:
            nd_l, nd_r = split_nodes(data, list(data)[0])
            depth += 1

# Returns the value of a leaf node, 1.0 or 0.0
# To be called when any one of the stopping criteria is met
def make_leaf(data):
    if(sum(data.iloc[:,-1]==1)/len(data) >= 0.5): return(1.0)
    else: return(0.0)


max_depth, min_records = 4, 2 # Declare the maximum dept and minimum records allowed
names = list(df_testing) # produces a list of column headers
left, right = split_nodes(df_testing, names[0]) # test the split_nodes function
print(left)
print(right)
#print(get_split(df_samp)) # test the get_split function
#print(get_gini(df_testing, df_testing['open'])) # test the get_gini function

# ## Start with algorithm on pg. 164 of Intro to Data Mining
# ## Functions




# Pruning -- see APM pg. 177-8 / this may or may not be necessary


# Predicting decision vairables
