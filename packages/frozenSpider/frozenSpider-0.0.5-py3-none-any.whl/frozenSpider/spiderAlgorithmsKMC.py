"""


This file implements K-means cluster algorithm. This is a simple but powerful algorithm.

This file has class that  can also visualise it .

This is a preliminary file that performs K-means cluster. This is one of the first versions. So a lot
will be improved in the future.


Classes:
K_means_cluster- It carries out model
plot model- It carries out data visualisation.




Attributes:
............................
____________________________
x                  -> input x parameters (list of list or np array)
y                  -> input y for training data
showGrid           -> Boolean which indicates weather grid should be shown or not
sizeX              -> Horizontal size of graph in inches
sizeY              -> Vertical size of graph in inches
labelx_count       -> number of labels on x axis
labely_count       -> number of labels on y axis
title_color        -> color of title of plot
label_default      -> Boolean which tells if the label is default or changed by user
xlabel_color       -> color of x label
ylabel_color       -> color of y label
title              -> title text
x_label            -> List x label text for all parameters/dimentions
y_label            -> y label text
xlabel_size        -> x_label font size of text
ylabel_size        -> y_label font size of text
title_size         -> title font size of text
model              -> this is the model object i.e. logistic regression object in case we need any parent class variables
x_calculated       -> The calculated part of model's x parameters or the test data's x coordinates
y_calculated       -> Calculated classification using model or the test data
learning_rate      -> The rate at with we want to train our model (usually in order of 0.001)
n_iters            -> Number of iterations which we we want our model to pass through the training process
weights            -> List of weights used in our model
bias               -> single float/double containing our bias value
parameters         -> count of x parameters, dimentions
coordinates_size   -> size of training data
calculated_point_class0_label -> train data class 0 color
calculated_point_class1_label -> train data class 1 point color
calculated_point_class0_color -> test data class 0 point color
calculated_point_class1_color -> test data class 1 point color
calculated_point_alpha        -> alpha/transparency of the point


#####.....IMP.......####
display_graph -> Specify weather graph needs to be displayed before saving in plot_graph method
color_dict -> Dictionary that contains wide range of colors in the form of dictionary. The keys are the names of colors
              , values are the hex codes of that color. You can get this dict using get_color_dict function()
You can print this dict i.e. print(object.get_color_dict()) to know which colors are available.






You are most welcomed to improve this code:
You can pull request for this code at

github.com/mrfrozen97/                      (In spiderAlgorithms repo)
or
Email - mrfrozenpeak@gmail.com




"""

import matplotlib.pyplot as plt
import numpy as np
import random
#from sklearn import datasets
#from sklearn.model_selection import train_test_split
from matplotlib.animation import FuncAnimation
#from sklearn.manifold import TSNE



class K_means_cluster():

    def __init__(self):

        self.x =[]
        self.y = []
        self.centeroids = []
        self.k = 2
        self.n_iters = 300
        self.clusters = {}
        self.unknown = []
        self.cluster_population = []
        self.graph_centeroids = []
        self.graph_centeroids2D = []
        self.plot_x = []
        self.plot_y = []



    def fit(self, x, y, k, n_iters=300):
        self.x = x
        self.y = y
        self.k = k
        self.centeroids = []
        self.n_iters = n_iters

        """
        i = 0
        while i<k:
            rand_centeroid = random.choice(self.x)
            if rand_centeroid in self.centeroids:
                pass
            else:
                i+=1
                self.centeroids.append(rand_centeroid)
                
        """
        for _ in range(k):
            self.centeroids.append(self.x[random.randint(0,len(self.x)-1)])
            self.cluster_population.append({})

        #print(self.centeroids)



        for i in range(self.n_iters):

            for j in range(k):
                self.clusters[j] = []
                self.cluster_population[j] = {}


            for index,coord in enumerate(self.x):
                dist_list = []
                for centeroid in self.centeroids:
                    dist_list.append(np.sum(np.square(np.subtract(coord, centeroid))))

                temp_index=dist_list.index(min(dist_list))
                self.clusters[temp_index].append(coord)
                if self.y[index] in self.cluster_population[temp_index]:
                    self.cluster_population[temp_index][self.y[index]] +=1
                else:
                    self.cluster_population[temp_index][self.y[index]] = 1



            #print(self.clusters)

            prev_centereoids = self.centeroids
            new_centeroids = []

            for cluster in self.clusters:

                temp_centeroid = np.average(self.clusters[cluster], axis=0)
                #print(temp_centeroid)
                new_centeroids.append(list(temp_centeroid))

                #print(temp_centeroid[0], temp_centeroid[1])

            self.centeroids = new_centeroids
            self.graph_centeroids.append(prev_centereoids)

            if np.sum(np.abs(np.subtract(new_centeroids, prev_centereoids))) < 0.0001:

                print("Optimised: " + str(i))
                break

        #print(self.cluster_population)
        #print(list(self.graph_centeroids))


    def get_centeroid_transition(self):

        return self.graph_centeroids

    def get_clusters(self):

        return self.cluster_population



    def predict(self, unknown):

        self.unknown = unknown
        calculated_unknown = []
        for coord in self.unknown:
            dist_list = []
            for centeroid in self.centeroids:
                dist_list.append(np.sum(np.square(np.subtract(coord, centeroid))))

            temp_index = dist_list.index(min(dist_list))
            temp_index_class = max(self.cluster_population[temp_index], key=self.cluster_population[temp_index].get)
            calculated_unknown.append(temp_index_class)
        return calculated_unknown







    def animate(self, i):
        self.plot_x.append(self.graph_centeroids[i][0])
        self.plot_y.append(self.graph_centeroids[i][1])


    def graph_animations(self):
        print(self.graph_centeroids)



        self.plot_x.append(self.graph_centeroids[0][0])
        self.plot_y.append(self.graph_centeroids[0][1])

        plt.scatter(self.plot_x, self.plot_y)
        ani = FuncAnimation(plt.gcf(), self.animate, interval=2000, frames=2)
        plt.show()















#Example
"""

coords = [
         [2, 3],
         [7, 11],
         [-1, 0],
         [5, 6],
         [7, 10],
         [2, 2.5],
         [9, 10.4],
         [4, 5],
         [5.5, 3.8],
         [4.7, 3.2],
         [7.5, 6.2]
          ]
y = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]



#datasetb = datasets.load_breast_cancer()
#x, y = datasetb.data, datasetb.target

#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1234)


model = K_means_cluster()
model.fit(coords, y, 2, n_iters=100)

#res = model.predict(x_test)



count = 0

#for i in range(len(res)):
 #   if res[i]==y_test[i]:
 #       count+=1


print(model.get_clusters())


#print("Accuracy = " + str(count/len(res)*100))

"""