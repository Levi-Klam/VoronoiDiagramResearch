import numpy as np

class Pareto:
    def __init__(self, weights):
        self.weights = weights

        self.schools = np.genfromtxt("distance_arrays/Schools.csv", delimiter=",")
        self.churches = np.genfromtxt("distance_arrays/Churches.csv", delimiter=",")
        self.bus_stops = np.genfromtxt("distance_arrays/Bus Stops.csv", delimiter=",")
        self.restaurants = np.genfromtxt("distance_arrays/Restaurants.csv", delimiter=",")
        self.groceries = np.genfromtxt("distance_arrays/Grocery Stores.csv", delimiter=",")
        self.social_facilities = np.genfromtxt("distance_arrays/Social Facilities.csv", delimiter=",")

        self.final = np.zeros_like(self.schools)
        self.create_weighted_arrays()

    def create_weighted_arrays(self):
        for i in range(len(self.schools)):
            self.schools[i] = self.schools[i] * self.weights[0]
            self.churches[i] = self.churches[i] * self.weights[1]
            self.bus_stops[i] = self.bus_stops[i] * self.weights[2]
            self.restaurants[i] = self.restaurants[i] * self.weights[3]
            self.groceries[i] = self.groceries[i] * self.weights[4]

        self.create_final_array()

    def create_final_array(self):
        for i in range(len(self.schools)):
            self.final[i] = int((self.schools[i] + self.churches[i] + self.bus_stops[i] + self.restaurants[i]) // 4)




# pareto = Pareto([1, 1, 1, 1])






