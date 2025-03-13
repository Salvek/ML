import math

def load_file_to_structure(path):
    data = {}
    
    with open(path, 'r') as f:
        lines = f.readlines()

    if not lines:
        return data
    
    num_of_columns = len(lines[0].strip().split(','))

    for i in range(num_of_columns):
        data[f"c{i+1}"] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        elements = line.split(',')
        for i, value in enumerate(elements):
            data[f"c{i+1}"].append(value)

    return data

def count_propability(data):

    propabilities = {}

    for column, values in data.items():
        num_of_rows = len(values)
        counter = {}

        unique_values = set(values)

        for value in values:
            counter[value] = counter.get(value, 0) + 1

        prob = {value: counter.get(value, 0) / num_of_rows for value in unique_values}
    
        propabilities[column] = prob

    return propabilities

def entropy(prop):
    entropy = 0.0

    for value, p in prop.items():
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy
    
def count_entropy(data):
    
    propability = count_propability(data)
    entropy_values = {}

    for column, prob in propability.items():
        entropy_values[column] = entropy(prob)
    
    return entropy_values

    
fpath = '../data/testGielda/gielda.txt'      

print(load_file_to_structure(fpath))
print('\n\n')
print(count_propability(load_file_to_structure(fpath)))
print('\n\n')
print(count_entropy(load_file_to_structure(fpath)))


