#!/usr/bin/env python3

import pandas as pd

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
    names = list(data)
    left = pd.DataFrame(columns=list(data))
    right = pd.DataFrame(columns=list(data))
    gini, ind = get_split(data)
    value = data.iloc[ind][names[0]]
    print("Splitting with gini {} at index {} value {}".format(gini, ind, value))
    # Split the node as given in the notes above
    for i in range(0, len(data)):
        if(data.iloc[i][col] < value):
            left = left.append(data.iloc[i])
            left = left.drop([col], axis=1)
        else:
            right = right.append(data.iloc[i])
            right = right.drop([col], axis=1)
    # Return the new child nodes
    return(left, right, value)

# Node for binary decision tree
class Node:
    left = right = splitting_condition = is_terminal = records = max_depth = minimum_records = value = viability = _records = None


    # records: pandas Dataframe of self records. records for a parent node is the same as
    #   the set addition of the children's nodes if self is not terminal.
    # splitting_conditions: a tuple of splitting conditions, where each item
    #   corresponds to the splitting condition for the corresponding level
    def __init__(self, records, max_depth, minimum_records):
        # Create root Node
        # Recursively split:
        #   using splitting conditions
        #   stopping using stopping rules

        self.max_depth = max_depth
        self.minimum_records = minimum_records

        self.is_terminal = self.check_if_terminal(records);

        self.records = records if self.is_terminal else None

        left_records, right_records, self.value = split_nodes(records, list(records)[0]) if not self.is_terminal else (None, None, None)
        self.left = Node(left_records, max_depth - 1, minimum_records) if not self.is_terminal else None
        self.right = Node(right_records, max_depth - 1, minimum_records) if not self.is_terminal else None
        self.viability = self.make_leaf()
        print("{}{} {}".format("\t" * max_depth, self.value, self.viability))

    def get_records(self):
        if isinstance(self._records, pd.DataFrame):
            return self._records

        print("Appending")
        ret = self.left.records.append(self.right.records)
        print("Appended")
        return ret

    def set_records(self, records):
        self._records = records

    records = property(get_records, set_records)

    def scale(data):
        return(data - data.mean() / data.std())

    # Always use the first column of the data frame for splitting each node's
    # records.
    #
    # return bool
    def predict(self, record):
        if self.is_terminal:
            return self.viability

        if record[0] < self.value:
            return self.left.predict(record)

        if (record[0] >= self.value):
            return self.right.predict(record)

    # Returns the value of a leaf node, 1.0 or 0.0
    # To be called when any one of the stopping criteria is met
    def make_leaf(self):
        return sum(self.records.iloc[:,-1]==1)/len(self.records) if len(self.records) > 0 else 0

    def get_depth(self):
        if not self.left:
            return 1

        return 1 + max(self.left.get_depth(), self.right.get_depth())


    # return bool
    def check_if_terminal(self, records):
        if self.get_depth() == self.max_depth:
            return True

        if len(records) <= self.minimum_records:
            return True

        if self.get_gini(records) == 0:
            return True

        return False

    # Compute Gini Index -- Intro to Data Mining pg. 158
    def get_gini(self, data):
        viable = list(data.iloc[:,-1]) # Get the class variable
        count_t, count_f = 0, 0        # Instantiate count variables
        nrow = len(data.iloc[:,0])                # Get the number of rows in the column
        for i in viable:               # Count the number each of 1.0 and 0.0
            if(i == 1): count_t += 1
            else: count_f += 1
        return(1 - ((count_t/nrow)**2 + (count_f/nrow)**2))
