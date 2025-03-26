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

def count_probability(data):

    probabilities = {}

    for column, values in data.items():
        num_of_rows = len(values)
        counter = {}

        for value in values:
            counter[value] = counter.get(value, 0) + 1

        prob = {value: count / num_of_rows for value, count in counter.items()}
        probabilities[column] = prob

    return probabilities

def entropy(probabilities):
    entropy_value = 0.0

    for p in probabilities.values():
        if p > 0:
            entropy_value -= p * math.log2(p)

    return entropy_value

def count_entropy(data):

    probabilities = count_probability(data)
    entropy_values = {column: entropy(prob) for column, prob in probabilities.items()}
    
    return entropy_values

def count_info_x_t(data, decision_column):

    info_values = {}
    total_rows = len(data[decision_column])
    
    for column in data:
        if column == decision_column:
            continue
        
        column_values = set(data[column])
        info_x_t = 0.0
        
        for value in column_values:
            subset_indices = [i for i, v in enumerate(data[column]) if v == value]
            subset_size = len(subset_indices)
            
            decision_values = [data[decision_column][i] for i in subset_indices]
            decision_counts = {v: decision_values.count(v) for v in set(decision_values)}
            decision_probs = {k: v / subset_size for k, v in decision_counts.items()}
            
            entropy_subset = entropy(decision_probs)
            info_x_t += (subset_size / total_rows) * entropy_subset
        
        info_values[column] = info_x_t
    
    return info_values

def count_gain(data, decision_column):

    total_entropy = entropy(count_probability({decision_column: data[decision_column]})[decision_column])
    info_x_t_values = count_info_x_t(data, decision_column)
    
    gain_values = {column: total_entropy - info for column, info in info_x_t_values.items()}
    
    return gain_values

fpath = '../data/testGielda/gielda.txt'

data = load_file_to_structure(fpath)

decision_column = "c4"

print("Dane wczytane ze struktury:")
print(data)
print("\nPrawdopodobieństwa:")
print(count_probability(data))
print("\nEntropia:")
print(count_entropy(data))
print("\nInfo(X, T):")
print(count_info_x_t(data, decision_column))
print("\nGain(X, T):")
print(count_gain(data, decision_column))
