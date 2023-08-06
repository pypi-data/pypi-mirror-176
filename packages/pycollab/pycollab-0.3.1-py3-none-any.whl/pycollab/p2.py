from google.colab import drive
drive.mount('/content/drive')

from keras.datasets import mnist

import numpy as np
import matplotlib.pyplot as plt

image_size =28
no_of_different_labels = 10
image_pixels = image_size * image_size

data="mnist.load_data()"
train=np.loadtxt('/content/drive/MyDrive/AML/mnist_train.csv', delimiter=",")
test=np.loadtxt('/content/drive/MyDrive/AML/mnist_test.csv', delimiter=",")

test[:10]

# normalization

test[test==255]
test.shape

# 99% accuracy

fac = 0.99 / 255
train_img = np.asfarray(train[:,1:])* fac + 0.01
test_img = np.asfarray(test[:,1:])* fac + 0.01

train_label = np.asfarray(train[:,:1])
test_label = np.asfarray(test[:,:1])

import numpy as np

# learning rate

lr = np.arange(10)

for label in range(10):
  one_hot = (lr==label).astype(np.int)
  print("label: ", label, " in one-hot representation: ", one_hot)

lr = np.arange(no_of_different_labels)

train_labels_one_hot = (lr==train_label).astype(float)
test_labels_one_hot = (lr==test_label).astype(float)

train_labels_one_hot

train_labels_one_hot[train_labels_one_hot==0] = 0.01
train_labels_one_hot[train_labels_one_hot==1] = 0.99
test_labels_one_hot[test_labels_one_hot==0] = 0.01
test_labels_one_hot[test_labels_one_hot==1] = 0.99

train_labels_one_hot

for i in range(3):
  img = train_img[i].reshape((28,28))
  plt.imshow(img, cmap="Greys")
  plt.show()

# dumping 

import pickle

with open("pickled_mnist.pkl", "bw") as fh:
  data = (train_img, test_img, train_label, test_label)
  pickle.dump(data, fh)

with open("pickled_mnist.pkl", "br") as fh:
  data = pickle.load(fh)

train_img = data[0]
test_img = data[1]
train_label = data[2]
test_label = data[3]

train_labels_one_hot = (lr==train_label).astype(float)
test_labels_one_hot = (lr==test_label).astype(float)

# data is Y values
# images is X values

image_size = 28
no_of_different_labels = 10
image_pixels = image_size * image_size

@np.vectorize
def sigmoid(x):
    return 1 / (1 + np.e ** -x)
activation_function = sigmoid

# L1 norm = lasso, distance
# L2 norm = ridge

from scipy.stats import truncnorm

# z-score 
# truncate = to abruptly stop

# like z-score
# z = lower limit - mu / sigma
# z = upper limit - mu / sigma

def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, # 0
                     (upp - mean) / sd, # 10
                     loc=mean, # 0
                     scale=sd) # intervals (_|_|_|_|_)

# In graph NN is nodes

class NeuralNetwork:
  def __init__(self, no_of_in_nodes, no_of_out_nodes, no_of_hidden_nodes, 
               learning_rate):
    self.no_of_in_nodes = no_of_in_nodes
    self.no_of_out_nodes = no_of_out_nodes
    self.no_of_hidden_nodes = no_of_hidden_nodes
    self.learning_rate = learning_rate 
    self.create_weight_matrices()

  def create_weight_matrices(self):
    rad = 1 / np.sqrt(self.no_of_in_nodes)
    X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
    self.wih = X.rvs((self.no_of_hidden_nodes, self.no_of_in_nodes))
    rad = 1 / np.sqrt(self.no_of_hidden_nodes)
    X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
    self.who = X.rvs((self.no_of_out_nodes, self.no_of_hidden_nodes))
  
  def train(self, input_vector, target_vector):
        input_vector = np.array(input_vector, ndmin=2).T
        target_vector = np.array(target_vector, ndmin=2).T
        
        output_vector1 = np.dot(self.wih, 
                                input_vector)
        output_hidden = activation_function(output_vector1)
        
        output_vector2 = np.dot(self.who, 
                                output_hidden)
        output_network = activation_function(output_vector2)
        
        output_errors = target_vector - output_network
        # update the weights:
        tmp = output_errors * output_network \
              * (1.0 - output_network)     
        tmp = self.learning_rate  * np.dot(tmp, 
                                           output_hidden.T)
        self.who += tmp

        # calculate hidden errors:
        hidden_errors = np.dot(self.who.T, 
                               output_errors)
        # update the weights:
        tmp = hidden_errors * output_hidden * \
              (1.0 - output_hidden)
        self.wih += self.learning_rate \
                          * np.dot(tmp, input_vector.T)
      
  def run(self, input_vector):
        # input_vector can be tuple, list or ndarray
        input_vector = np.array(input_vector, ndmin=2).T

        output_vector = np.dot(self.wih, 
                               input_vector)
        output_vector = activation_function(output_vector)
        
        output_vector = np.dot(self.who, 
                               output_vector)
        output_vector = activation_function(output_vector)
    
        return output_vector
            
  def confusion_matrix(self, data_array, labels):
        cm = np.zeros((10, 10), int)
        for i in range(len(data_array)):
            res = self.run(data_array[i])
            res_max = res.argmax()
            target = labels[i][0]
            cm[res_max, int(target)] += 1
        return cm    

  def precision(self, label, confusion_matrix):
        col = confusion_matrix[:, label]
        return confusion_matrix[label, label] / col.sum()
    
  def recall(self, label, confusion_matrix):
        row = confusion_matrix[label, :]
        return confusion_matrix[label, label] / row.sum()
            
  def evaluate(self, data, labels):
        corrects, wrongs = 0, 0
        for i in range(len(data)):
            res = self.run(data[i])
            res_max = res.argmax()
            if res_max == labels[i]:
                corrects += 1
            else:
                wrongs += 1
        return corrects, wrongs

ANN = NeuralNetwork(no_of_in_nodes = image_pixels, 
                    no_of_out_nodes = 10, 
                    no_of_hidden_nodes = 100,
                    learning_rate = 0.1)
    
    
for i in range(len(train_img)):
    ANN.train(train_img[i], train_labels_one_hot[i])

for i in range(20):
    res = ANN.run(test_img[i])
    print(test_label[i], np.argmax(res), np.max(res))

corrects, wrongs = ANN.evaluate(train_img, train_label)
print("accuracy train: ", corrects / ( corrects + wrongs))
corrects, wrongs = ANN.evaluate(test_img, test_label)
print("accuracy: test", corrects / ( corrects + wrongs))

cm = ANN.confusion_matrix(train_img, train_label)
print(cm)

for i in range(10):
    print("digit: ", i, "precision: ", ANN.precision(i, cm), "recall: ", 
          ANN.recall(i, cm))

epochs = 3

NN = NeuralNetwork(no_of_in_nodes = image_pixels, 
                   no_of_out_nodes = 10, 
                   no_of_hidden_nodes = 100,
                   learning_rate = 0.1)

for epoch in range(epochs):  
    print("epoch: ", epoch)
    for i in range(len(train_img)):
        NN.train(train_img[i], 
                 train_labels_one_hot[i])
  
    corrects, wrongs = NN.evaluate(train_img, train_label)
    print("accuracy train: ", corrects / ( corrects + wrongs))
    corrects, wrongs = NN.evaluate(test_img, test_label)
    print("accuracy: test", corrects / ( corrects + wrongs))