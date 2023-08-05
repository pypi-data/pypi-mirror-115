"""


This file implements K nearest algorithm. This is a slow but powerful algorithm.

This file has class that  can also visualise it.

This is a preliminary file that performs K-Nearest neighbour. This is one of the first versions. So a lot
will be improved in the future.


Classes:
K Nearest neighbours- It carries out model
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


import numpy as np
import matplotlib.pyplot as plt
import random

from sklearn import datasets
from sklearn.model_selection import  train_test_split
from frozenSpider import Data_visualisation as dt
from frozenSpider import spiderAlgorithmResources as res


class K_nearest_neighbours():

    def __init__(self, x_data, y_data, k):
        self.x_data = np.array(x_data)
        self.y_data = np.array(y_data)
        self.k = k
        self.x_classified = []
        self.y_classified = []


    def nearest_neighbour(self, distances_y, k):
       # print(collections.OrderedDict(sorted(y.items())))
        ndistances_y = {}
        count_k = 0
        for key in sorted(distances_y):
            count_k+=1
            ndistances_y[key] = distances_y[key]
            if count_k==k:
                break
        nearest = {}
        for key in ndistances_y:
            if ndistances_y[key] in nearest:
                nearest[ndistances_y[key]] +=1
            else:
                nearest[ndistances_y[key]] = 1

       # print(nearest)
        max_points = 0
        max_key = 0
        for key in nearest:
            if nearest[key]>max_points:
                max_points = nearest[key]
                max_key = key

        return max_points, max_key


    def classify(self,coordinates):

        self.x_classified = coordinates
        near_classes = []
        confidences = []


        for coords in coordinates:

            x_arr = []
            for i in range(len(self.x_data)):
                x_arr.append(coords)

            x_arr = np.array(x_arr)

            #print(np.sum(np.square(x_arr-self.x_data), axis=1))

            distances = np.array(np.sqrt(np.sum(np.square(x_arr-self.x_data), axis=1)))
            distances_y = {}

            for i in range(len(distances)):

                 distances_y[distances[i]] = self.y_data[i]


            near_points, near_class = self.nearest_neighbour(distances_y, self.k)
           # print(near_class)
            confidence = near_points/ self.k * 100

            near_classes.append(near_class)
            confidences.append(confidence)

            #print(near_points, near_class)
            #print(distances_y)
            #print(distances)

        self.y_classified = near_classes
        return near_classes, confidences













class plot_model():

    def __init__(self, model):
        self.showGrid = True
        self.sizeX = 10
        self.sizeY = 6
        self.labelx_count = 10
        self.labely_count = 10
        self.title_color = "#FF0000"
        self.xlabel_color = "#663399"
        self.ylabel_color = "#663399"
        self.label_default = True
        self.title = ""
        self.x_label = ["Dimention " + str(x) for x in range(1, 100)]
        self.y_label = ""
        self.xlabel_size = 15
        self.ylabel_size = 15
        self.title_size = 18
        self.model = model
        self.color_dict = res.Resources.get_color_dict()
        self.calculated_point_size = 10
        self.calculated_point_alpha = 0.5
        self.train_labels = []
        self.test_labels = []
        self.train_data_color = [key for key in sorted(self.color_dict)[:15]]
        self.test_data_color = [key for key in sorted(self.color_dict)[15:]]
        random.shuffle(self.train_data_color)
        random.shuffle(self.test_data_color)
        self.legend_position = "upper right"
        self.plot_background = 'dark'








    # Function to get dictionary to access the different options avaliable for the colors.........................

    def get_color_dict(self):
        return self.color_dict








    # function to set label of each dimention of the graph................................................

    def set_dimention_labels(self, dimention_label):
        self.x_label = dimention_label







    def set_marker_properties(self,plot_background='dark', legend_position="upper right", train_labels=[], test_labels=[], label_default=True, calculated_point_class1_label = "Calculated class 1", calculated_point_class0_label="Calculated class 0", calculated_point_alpha = 0.5,  calculated_point_class1_color='Red',calculated_point_class0_color="Cyan", title_size=15, xlabel_size=10, ylabel_size=10, title="Output vs dimention", y_label="y coordinates", title_color="#FF0000", xlabel_color="#663399", ylabel_color="#663399"):
        self.title_size = title_size
        self.xlabel_size = xlabel_size
        self.ylabel_size = ylabel_size
        self.y_label = y_label
        self.title = title

        self.xlabel_color = xlabel_color
        self.ylabel_color = ylabel_color
        self.title_color = title_color
        self.label_default = label_default
        self.calculated_point_size = 10

        self.calculated_point_class0_label = calculated_point_class0_label
        self.calculated_point_class1_label = calculated_point_class1_label
        self.calculated_point_class0_color = calculated_point_class0_color
        self.calculated_point_class1_color = calculated_point_class1_color

        self.calculated_point_alpha = calculated_point_alpha
        self.train_labels = train_labels
        self.test_labels = test_labels
        self.legend_position = legend_position
        self.plot_background = plot_background







  #Sets the display size which will be equal to size of image if it is being svaed.........................

    def set_display_size(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY





# main fuction thats plots the graph and saved it if path provided.........................
    #This function iterates through all the dimentions/parameters and plot each one seperate...............




    def plot_model(self, display_graph = True,display_calculated_points = True, alpha=0.6, point_size=25,label_x=[], label_y=[],class1_color='Purple', class0_color='Orange',unknown_points_label="Unknown points",line_label='Best Fit line', point_color='DeepSkyBlue', save_fig_file='dont'):


        # These are the coordinates to plot the line which is inclusion of both known and calculated points
        if self.plot_background=='dark':
              plt.style.use('dark_background')
        multi_dimentions = np.array(self.model.x_data)
        multi_dimentions_calculated = np.array(self.model.x_classified)
       # print(len(multi_dimentions[0]))
        #print(multi_dimentions)

        for dimention in range(len(multi_dimentions[0])):

            #x_train_data = []
            y_train_data = {}
            y_test_data = {}

            for i,a in enumerate(multi_dimentions):
                #print(i)
                if self.model.y_data[i] in y_train_data:
                    y_train_data[self.model.y_data[i]].append(a[dimention])
                else:
                    y_train_data[self.model.y_data[i]] = [a[dimention]]

            for i, a in enumerate(multi_dimentions_calculated):

                if self.model.y_classified[i] in y_test_data:
                    y_test_data[self.model.y_classified[i]].append(a[dimention])
                else:
                    y_test_data[self.model.y_classified[i]] = [a[dimention]]
                #x_train_data.append(i[dimention])
            #print(y_test_data)

           # print(y_train_data)

            index_color = 0
            for group in y_train_data:
                #print(group)
                y_plot_axis = []

                if len(self.train_labels)==0:
                    actual_train_label = "train class" + str(group)
                else:
                    actual_train_label = self.train_labels[index_color]

                for i in range(len(y_train_data[group])):
                    y_plot_axis.append(group)
                plt.scatter(y_train_data[group], y_plot_axis,
                            color=self.color_dict[self.train_data_color[index_color%15]],
                            label=actual_train_label,
                            alpha=alpha,
                            zorder=3)                     #plot the best fit line
                index_color+=1


            index_color = 0

            if display_calculated_points:

                for group in y_test_data:
                    #print(group)
                    y_plot_axis = []

                    if len(self.test_labels) == 0:
                        actual_test_label = "test class" + str(group)
                    else:
                        actual_test_label = self.test_labels[index_color]


                    for i in range(len(y_test_data[group])):
                        y_plot_axis.append(group)

                    plt.scatter(y_test_data[group], y_plot_axis,
                                label=actual_test_label,
                                alpha=alpha,
                                zorder=3,
                                color=self.color_dict[self.test_data_color[index_color%15]])  # plot the best fit line

                    index_color +=1



            plt.title(self.title,
                      fontdict=res.Resources.title_dict,
                      color=self.title_color)
            plt.xlabel(self.x_label[dimention],
                       fontdict=res.Resources.label_dict,
                       color=self.xlabel_color)
            plt.ylabel(self.y_label,
                       fontdict=res.Resources.label_dict,
                       color=self.ylabel_color)





            plt.legend(loc = self.legend_position)

            if self.showGrid:
                plt.grid(color='#cfd8dc', zorder=0)

            figure = plt.gcf()
            figure.set_size_inches(self.sizeX, self.sizeY)


            if not(save_fig_file=='dont') :

                  plt.savefig("./"+save_fig_file +"/"+self.x_label[dimention])#, bbox_inches='tight')
            if display_graph:
               plt.show()
            plt.close()






#Example 1
"""

bc = datasets.load_breast_cancer()
x, y = bc.data, bc.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1234)


a = K_nearest_neighbours(x_train, y_train, 3)
group, confidence = a.classify(x_test)



#print(group, confidence)
pl = plot_model(a)
#pl.plot_model()





plot1 = dt.Knn_plot(a)
plot1.plot_3D_visuals()
plot2 = dt.Knn_plot_2D(a)
plot2.plot_3D_visuals()
"""




