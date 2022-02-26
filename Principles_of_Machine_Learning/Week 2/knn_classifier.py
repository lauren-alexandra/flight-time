"""
Title: KNN Classifier
Description: The classifier predicts the type of iris based on the sepal length and width (the parts of the calyx) and the petal length and width, in centimeters.
"""

import sys
import time
from math import sqrt
from csv import reader

def main():
    
    filename = '.\\iris.csv'
    k = 5

    def get_input():
        need_input = True

        while need_input:
            need_input = False
            print(f'Example iris with sepal length, sepal width, petal length, and petal width: 5.1, 3.5, 1.4, 0.2\n')
            received = input('Enter an iris: ')
            received = list(received.split(", "))
            received = [float(val.strip()) for val in received]

        return received

    iris = get_input()

    # load file
    def load_csv(filename):
        data = list()
        with open(filename, 'r') as file:
            csv = reader(file)
            for row in csv:
                if not row:
                    continue
                data.append(row)
        return data
 
    data = load_csv(filename)

    def prepare_data(data):
        # remove column headings - 'SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Name'
        data = data[1:]

        # convert string nums to floats 
        for col in range(len(data[0])-1): # excluding class values
            for row in data:
                row[col] = float(row[col].strip())

        # encode class values
        class_col = len(data[0])-1
        classes = [row[class_col] for row in data]
        class_vals = set(classes)
        class_dict = dict() # key: name, value: integer 

        for idx, value in enumerate(class_vals):
            class_dict[value] = idx
        for row in data:
            row[class_col] = class_dict[row[class_col]]

        return data, class_dict

    data, class_lookup = prepare_data(data) 

    # calculate the distance between test data and each row of training data
    def get_distance(instance, row):
        distance = 0.0

        for i in range(len(instance)-1): # excluding class col
            # Euclidean distance
            distance += (instance[i] - row[i])**2

        return sqrt(distance)

    def get_neighbors(train, instance, k_neighbors):
        distances = list()

        for row in train:
            distance = get_distance(instance, row)
            distances.append((row, distance))

        # sort the calculated distances in ascending order based on distance values
        distances.sort(key=lambda tup: tup[1]) # sort by distance at index 1
        neighbors = list()

        # get top k rows
        for i in range(k_neighbors):
            neighbors.append(distances[i][0]) # append the row data in distances to neighbors 

        return neighbors

    def predict_classification(train, instance, k_neighbors):
        neighbors = get_neighbors(train, instance, k_neighbors)
        class_values = [row[-1] for row in neighbors]
        # find the highest count of occurrences of each value in class_values 
        prediction = max(set(class_values), key=class_values.count)
        return prediction
    
    # KNN
    def k_nearest_neighbors(train, instance, k_neighbors):
        classification = predict_classification(train, instance, k_neighbors)

        # get class name
        idx = list(class_lookup.values()).index(classification)
        class_names = list(class_lookup.keys())
        class_name = class_names[idx]

        return class_name 

    train_set = data[1:]
    predicted_class = k_nearest_neighbors(train_set, iris, k)

    print("\nPrediction: ", predicted_class)

    time.sleep(3)
    sys.exit()

if __name__ == "__main__":
    main()