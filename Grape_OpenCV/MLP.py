
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

class NN():
    def __init__(self, no_samples, no_features, no_classes, learning_rate, no_epochs):
        self.no_samlpes = no_samples
        self.no_features = no_features
        self.no_classes = no_classes
        self.lr = learning_rate
        self.no_epochs = no_epochs
        
    def weights_init(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.random.randn(hidden_size, 1)
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.random.randn(output_size, 1)
        
    def sofmax_func(self, z):
        eZ = np.exp(z)
        return eZ/np.sum(eZ, axis = 0)
    
    def relu_func(self, z):
        return np.maximum(z, 0)
    
    def relu_der(self, a):
        return a > 0
    
    def onehot_encoding(self, Y):
        # return sparse.coo_matrix((np.ones_like(Y), (Y, np.arange(len(Y)))), shape = (self.no_classes, len(Y))).toarray()
        onehot_encoder = OneHotEncoder(sparse = False)
        onehot_encoded = onehot_encoder.fit_transform(Y.T)
        return onehot_encoded.T
    
    def forward_pass(self, X):
        self.Z1 = np.dot(self.W1.T, X) + self.b1
        self.A1 = self.relu_func(self.Z1)
        self.Z2 = np.dot(self.W2.T, self.A1) + self.b2
        Y_hat = self.sofmax_func(self.Z2)
        return Y_hat
    
    def backward_pass(self, X, Y, Y_hat):
        dZ2 = Y_hat - Y     #   Shape (3, 300)
        dW2 = np.dot(self.A1, dZ2.T)
        db2 = np.sum(dZ2, axis = 1, keepdims = True)
        
        dZ1 = np.dot(self.W2, dZ2)*self.relu_der(self.A1)   #   Shape (50, 300)
        dW1 = np.dot(X, dZ1.T)
        db1 = np.sum(dZ1, axis = 1, keepdims = True)
        
        #   Update weights
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1      
    
    def loss_func(self, Y, Y_hat):
        return -np.sum(Y * np.log(Y_hat))/Y.shape[1]
        
    def fit(self, X, Y, input_size, hidden_size, output_size):
        loss_his = []
        #   Weights initialization
        self.weights_init(input_size, hidden_size, output_size)
        #   Train model
        for i in range(self.no_epochs):
            Y_hat = self.forward_pass(X)
            loss = self.loss_func(Y, Y_hat)
            loss_his.append(loss)
            self.backward_pass(X, Y, Y_hat)
        return (self.W1, self.b1, self.W2, self.b2), loss_his  
    
    def visualize(self, X, Y, state = None):
        if state == 'plot':
            plt.scatter(X[0, :self.no_samlpes], X[1, :self.no_samlpes], c = 'r', marker = 's', alpha = 0.7)
            plt.scatter(X[0, self.no_samlpes:2*self.no_samlpes], X[1, self.no_samlpes:2*self.no_samlpes], c = 'g', marker = '^', alpha = 0.7)
            plt.scatter(X[0, 2*self.no_samlpes:3*self.no_samlpes], X[1, 2*self.no_samlpes:3*self.no_samlpes], c = 'b', marker = 'o', alpha = 0.7)
            plt.axis('equal')
            # plt.axis([-1.5, 1.5, -1, 1])
            plt.show()
            plt.close()
    
    def predict(self, X, Y, weights):
        W1, b1, W2, b2 = weights
        Z1 = np.dot(W1.T, X) + b1
        A1 = self.relu_func(Z1)
        Z2 = np.dot(W2.T, A1) + b2
        Y_hat = self.sofmax_func(Z2)
        return Y_hat
        
        
    
if __name__ == "__main__":
    #   Create data
    no_samples = 100
    no_features = 2
    no_classes = 3
    X = np.zeros((no_features, no_samples*no_classes))
    Y = np.zeros((1, no_samples*no_classes), dtype = np.uint8)
       
    for i in range(no_classes):
        idx = range(no_samples*i, no_samples*(i+1))
        r = np.linspace(0.0, 1, no_samples)
        t = np.linspace(i*4, (i+1)*4, no_samples) + np.random.randn(no_samples)*0.2
        X[:, idx] = np.concatenate((np.array([r*np.sin(t)]), np.array([r*np.cos(t)])), axis = 0)
        Y[0, idx] = i
        
    #   Set networks architecture params
    input_size = 2
    hidden_size = 50
    output_size = 3
    
    #   Set some hyperparameters
    no_epochs = 800
    learning_rate = 0.01
        
    model = NN(no_samples, no_features, no_classes, learning_rate, no_epochs)
    
    #   Visualize dataset
    model.visualize(X, Y, state = 'plot')
    
    #   Onehot encoding
    Y = model.onehot_encoding(Y)
    
    
    weights, loss_his = model.fit(X, Y, input_size, hidden_size, output_size)
    print(np.min(loss_his))
    
    plt.plot(loss_his)
    plt.xlabel('Epoch', fontsize = 15, c = 'r')
    plt.ylabel('Loss', fontsize = 15, c = 'r')  
    plt.show()
    plt.close()
    
    #   Predict model
    Y_pred = model.predict(X, Y, weights)
    print(f'Accuracy: {np.sum(np.argmax(Y_pred, axis = 0) == np.argmax(Y, axis = 0))/Y.shape[1]*100:.2f}')
