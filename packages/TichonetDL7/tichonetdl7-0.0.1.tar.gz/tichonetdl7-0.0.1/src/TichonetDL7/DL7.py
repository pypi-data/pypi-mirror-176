import numpy as np
import matplotlib.pyplot as plt
import math

from   sklearn.metrics import classification_report, confusion_matrix
import os
import h5py

# =============================================================
# =============================================================
#              DLModel
# =============================================================
# =============================================================
# This class implements a deep nuarl network (ANN).
# Input / Internal parameters:
# name - A string for the ANN (model)
# layers -  a list of layers that construct the ANN. Starting from the firs Hidden layer, upto the output layer
# is_compile - a boolean to indicate if setting of the ANN is completed
# is_train - a boolean value to indicate if we are using the object to train the internal parameters of the ANN
#      or we are using the ANN, that already hav a trained set of parameters (e.g. W's and b's), to 
#      predict the value of a new sample (e.g. picture)
# Algorithm:
#    -The model is instantiated with 'name' and default values for the other internal parameters
#    -It must be activated by calling to 'compile' - setting the internal parameters of 'loss' function
#    -A sequence of 'add' activation will add nuoron layers to the model. Calling to the add must be done in the right order of course
#    -Support activation of regularization mechanism in the different layers
#    * Train the model 
#    * Predict
#    * Supports minibatches and softmax
#
# Predefined loss functions, already implemented, to choose from:
# - "squared_means"
# - "cross_entropy"
# - "categorical_cross_entropy"
# - else - raise "Unimplemented loss function" exception
class DLModel:
    def __init__(self, name="Model"): 
        self.name = name
        self.layers = [None]
        self._is_compiled = False
        self.inject_str_func = None
        self.is_train = False

    # Printout of the model parameters
    def __str__(self):
        s = self.name + " description:\n\tnum_layers: " + str(len(self.layers)-1) +"\n"
        if self._is_compiled:
            s += "\tCompilation parameters:\n"
            s += "\t\tprediction threshold: " + str(self.threshold) +"\n"
            s += "\t\tloss function: " + self.loss + "\n\n"

        for i in range(1,len(self.layers)):
            s += "\tLayer " + str(i) + ":" + str(self.layers[i]) + "\n"
        return s

    # Service routine - set the 'is_train' flag for the model and all layers
    def set_train(self, set_parameter_train):
        self.is_train = set_parameter_train
        L = len(self.layers)
        for i in range(1,L):
            self.layers[i].set_train(set_parameter_train)

    # Service routine - Enable save of the parameters for the whole ANN for future use
    # Parameters are save under a directory with the model name and each layer has its own file with the values of its parameters
    def save_weights(self,path):
        for i in range(1,len(self.layers)):
            self.layers[i].save_weights(path,"Layer"+str(i))
    
    def restore_parameters(self, directory_path):
        directory = directory_path+"/"+self.name
        for l in self.layers:
            l.restore_parameters(directory)

    # compile - set the loss function of choice for the model and set its parameters 
    # -------
    def compile(self, loss, threshold = 0.5):
        self.loss = loss            # save the loss function string 
        self.threshold = threshold  # save the loss function parameters 
        self._is_compiled = True    
        if loss == "squared_means":
            self.loss_forward = self._squared_means
            self.loss_backward = self._squared_means_backward
        elif loss == "cross_entropy":
            self.loss_forward = self._cross_entropy
            self.loss_backward = self._cross_entropy_backward
        elif loss == "categorical_cross_entropy":
            self.loss_forward = self._categorical_cross_entropy
            self.loss_backward = self._categorical_cross_entropy_backward
        else:
            raise NotImplementedError("Unimplemented loss function: " + loss)

    # Add layers of nuorons to the ANN
    # ----------
    def add(self, layer):
        self.layers.append(layer)

    # ------------
    # Implementation of the supported los functions - Forward and Backword 
    # ------------
    def _squared_means(self, AL, Y):
        error = (AL - Y)**2
        return error
    def _squared_means_backward(self, AL, Y):
        dAL = 2*(AL - Y)
        return dAL

    def _cross_entropy(self, AL, Y):
        eps = 1e-10
        AL = np.where(AL==0,eps,AL)       # to avoid divide by zero
        AL = np.where(AL == 1, 1-eps,AL)
        logprobs = np.where(Y == 0, -np.log(1 - AL), -np.log(AL))
        return logprobs
    def _cross_entropy_backward(self, AL, Y):
        m = AL.shape[1]
        dAL = np.where(Y == 0, 1/(1-AL), -1/AL) 
        return dAL

    def _categorical_cross_entropy(self, AL, Y):
        eps = 1e-10
        AL = np.where(AL==0,eps,AL)     # to avoid divide by zero
        AL = np.where(AL == 1, 1-eps,AL)
        errors = np.where(Y == 1, -np.log(AL), 0) 
        return errors
    def _categorical_cross_entropy_backward(self, AL, Y):
        # in case output layer's activation is 'softmax'- compute dZL directly using: dZL = Y - AL
        dZl = AL - Y
        return dZl
    
    # Support activation of regularization in the layers
    def regularization_cost(self, m):
        L = len(self.layers)
        reg_costs = 0
        for l in range(1,L):
            reg_costs += self.layers[l].regularization_cost(m)
        return reg_costs

    # Compute the cost for the whole network, using the loss function 
    # ----------------
    def compute_cost(self, AL, Y):
        m = AL.shape[1]
        errors = self.loss_forward(AL, Y) 
        J = (1/m)*np.sum(errors) + self.regularization_cost(m)
        return J

    # -----------------------------------------
    # Forward propagation of the model. Will be used in train and in predict phases
    # Activate the nuoron-layers that are part of this model' one after the other
    # -----------------------------------------
    def forward_propagation(self, X):
        L = len(self.layers)
        for l in range(1,L):
            X = self.layers[l].forward_propagation(X)            
        return X

    # -----------------------------------------
    # Backword propagation of the model. 
    # Activate the nuoron-layers backword propagation and update the ANN parameters in each layer, is it goes backword
    # -----------------------------------------
    def backward_propagation(self, Al, Y , t):
        L = len(self.layers)
        dAl_t = self.loss_backward(Al, Y)                       # Starts with backwording the los function
        for l in reversed(range(1,L)):                          # Walk the ANN from the end to the begin (backword...)
            dAl_t = self.layers[l].backward_propagation(dAl_t)  # Backword
            self.layers[l].update_parameters(t)                  # Update parameters
        return dAl_t

    # =================== Main Train Function ======================
    # Get the X , Y , num of epocs, mini_batch_size (supports also mini batch algorithm)
    # Note: use different seeds for mini batch random grouping (batches) of the total samples
    def train(self, X, Y, num_epocs , mini_batch_size, t = 1):
        self.set_train(True)
        print_ind = max(num_epocs // 100, 1)
        costs = []      # used to agregate costs during train, for later display
        #Al = np.array(X, copy=True)
        for i in range(num_epocs):  # if mini_batch_size is 1 - this is similar to num_of_iterations
           t = 1
           mini_batches = self.random_mini_batches(X , Y , mini_batch_size , 10 + i ) 
           for mini_batch in mini_batches:
                t += 1
                # forward propagation
                Al = self.forward_propagation(mini_batch[0])
                #backward propagation and update parameters
                dAl = self.backward_propagation(Al, mini_batch[1] , t)
         
           

            # record progress for later printout, and progress printing during long training
           if (num_epocs == 1 or ( i > 0 and i % print_ind == 0)):
                J = self.compute_cost(Al, mini_batch[1])
                costs.append(J)
                #user defined info
                inject_string = ""
                if self.inject_str_func != None:
                    inject_string = self.inject_str_func(self, X, Y, Y_hat)
                
                print(f"cost after {i} full updates {100*i/num_epocs}%:{J}" + inject_string)
        costs.append(self.compute_cost(Al, mini_batch[1]))

        self.set_train(False)

        return costs

    # =================== Predict Function ======================
    # This function will get a set of samples (X) and will return 
    # the trained ANN prediction for them (e.g. is it a cat or not)
    def predict(self, X, Y=None):
        # must create a mew copy of the input set because it is altered during the train of hte layers
        Al = np.array(X, copy=True)  
        # forward propagation
        Al = self.forward_propagation (Al)

        if Al.shape[0] > 1: # softmax 
            predictions = np.where(Al==Al.max(axis=0),1,0)
            return predictions
            #return predictions, confusion_matrix(predictions,Y)
        else:
            return Al > self.threshold

    # support to softmax algorithm. convert result to one-hot representation

    def to_one_hot(num_categories, Y):
        m = Y.shape[0]
        Y = Y.reshape(1, m)
        Y_new = np.eye(num_categories)[Y.astype('int32')]
        Y_new = Y_new.T.reshape(num_categories, m)
        return Y_new

    # enable printout of a confusion matrix represantation of train / test samples
    def confusion_matrix(self, X, Y):
        prediction = self.predict(X)
        prediction_index = np.argmax(prediction, axis=0)
        Y_index = np.argmax(Y, axis=0)
        right = np.sum(prediction_index == Y_index)
        print("accuracy: ",str(right/len(Y[0])))
        cf = confusion_matrix(prediction_index, Y_index)
        print(cf)
        return cf

    # service routine to suppoer minibatch algoriths. set a set of pairs (X,Y), using random permutations 
    @staticmethod
    def random_mini_batches(X, Y , mini_batch_size = 64 , seed = 0):
        m = X.shape[1]
        np.random.seed(seed)
        permutation = list(np.random.permutation(m))
        mini_batches = []
        num_complete_minibatches = math.floor(m/mini_batch_size)
        shuffled_X = X[:, permutation] 
        shuffled_Y = Y[:, permutation].reshape((-1,m)) 
        for k in range(num_complete_minibatches):
            mini_batch_X = shuffled_X[:, mini_batch_size*k : (k+1) * mini_batch_size] 
            mini_batch_Y = shuffled_Y[:, mini_batch_size*k : (k+1) * mini_batch_size] 
            mini_batch = (mini_batch_X, mini_batch_Y)
            mini_batches.append(mini_batch)
        top = num_complete_minibatches* mini_batch_size 
        if (top < m):                       # add the last batch (if not fully populated
           mini_batch_X = shuffled_X[:, top : m]
           mini_batch_Y = shuffled_Y[:, top : m]
           mini_batches.append ((mini_batch_X, mini_batch_Y))
        return mini_batches

    def print_regularization_cost(n,X, Y, Y_hat):
        return ""
        s = ""
        m = Y.shape[1]
        for l in n.layers:
            reg_cost = l.regularization_cost(m)
            if reg_cost > 0:
                s += f"\n\t{l.name}: {reg_cost}"
        return s

# =============================================================
# =============================================================
#              DLLayer
# =============================================================
# =============================================================
# This class implements a one layer of nuorons (Perceptrons).
# Input / Internal parameters:
# name - A string for the ANN (model)
# num_units - number of nuorons in the layer
# input_shape - number of inputs that get into the layer
# activation - name of the activation function (same for all the layer). implemented: 
#    - sigmoid
#    - trim_sigmoid
#    - tanh
#    - trim_tanh
#    - relu     ( default )
#    - leaky_relu
#    - softmax
#    - trim_softmax
#    - NoActivation
# W_initialization - name of the initialization funciton (same for all the layer), implemented : zeros, random, HE, Xaviar.
# learning_rate - sometimes called alpha.
# optimization - the algorithm to use for the gradient descent parameters update (e.g. adaptive)
# regularization - reularization to use (e.g. L2 ,dropout )
# ** note: Some of the above settings have spcific additional parameters that are also set in the __init function

# Algorithm:
#    * Forward and Backward propagation 
#
# Predefined regularization functions, already implemented, to choose from: L2, dropout

class DLLayer:
    def __init__(self, name, num_units, input_shape, activation="relu", 
                 W_initialization="random", learning_rate = 1.2, optimization=None, 
                 regularization = None, ConvMode = False): 
        self.name = name
        self._num_units = num_units
        self._input_shape = input_shape
        self._activation = activation
        self.alpha = learning_rate
        self._optimization = optimization        
        self.regularization = regularization
        self.is_train = False
        self._ConvMode = ConvMode

        # ----- setting specific parameters for the initialization parameters:

        # W and b initialization
        self.init_weights(W_initialization)

        # optimization parameters
        if self._optimization == 'adaptive':
            self._adaptive_alpha_b = np.full((self._num_units, 1), self.alpha, dtype=float)
            self._adaptive_alpha_W = np.full(self._get_W_shape(), self.alpha, dtype=float)
            self.adaptive_cont = 1.1
            self.adaptive_switch = 0.5
        elif self._optimization == 'sdg': #Stochastic Gradient Descent
            lll = 1
        elif self._optimization == 'momentum': #Stochastic Gradient Descent With Momentum
            lll = 1
        elif self._optimization == 'rmsprop': #Root Means Square
            lll = 1
        elif self._optimization == 'adadelta': #Basically Adaptive Gradient Descent++
            lll = 1
        elif self._optimization == 'adam': #The Adam Optimizaer takes features from both Adagrad and RMSProp algorithms
            self.adam_v_db = np.zeros((self._num_units, 1))
            self.adam_v_dW = np.zeros(self._get_W_shape())
            self.adam_s_db = np.zeros((self._num_units, 1))
            self.adam_s_dW = np.zeros(self._get_W_shape())
            self.adam_beta1 = 0.9
            self.adam_beta2 = 0.999
            self.adam_epsilon = 1.0e-8
 
        # regularization parameser
        self.L2_lambda = 0              # i.e. no L2
        self.dropout_keep_prob = 1      # i.e. no dropout
        if (regularization == "L2"):
            self.L2_lambda = 0.6
        elif (regularization == "dropout"):
            self.dropout_keep_prob = 0.6

        # activation parameters
        self.activation_trim = 1e-10  # keep score in bounded values

        # set activation methods
        if activation == "sigmoid":
            self.activation_forward = self._sigmoid
            self.activation_backward = self._sigmoid_backward
			
        elif activation == "trim_sigmoid":
            self.activation_forward = self._trim_sigmoid
            self.activation_backward = self._sigmoid_backward
			
        elif activation == "tanh": #Hyperbolic Tangent
            self.activation_forward = self._tanh
            self.activation_backward = self._tanh_backward
			
        elif activation == "trim_tanh":
            self.activation_forward = self._trim_tanh
            self.activation_backward = self._trim_tanh_backward
			
        elif activation == "relu": #Rectified Linear Unit
            self.activation_forward = self._relu
            self.activation_backward = self._relu_backward
			
        elif activation == "leaky_relu": #Leaky Rectified Linear Unit (Also Called LReLU)
            self.activation_forward = self._leaky_relu
            self.activation_backward = self._leaky_relu_backward
            self.leaky_relu_d = 0.01
			
        elif activation == "softmax":
            self.activation_forward = self._softmax
            self.activation_backward = self._softmax_backward
			
        elif activation == "trim_softmax":
            self.activation_forward = self._trim_softmax
            self.activation_backward = self._softmax_backward
			
        elif activation == "arctan":
            self.activation_forward = self._arctan
            self.activation_backward = self._arctan_backward
		
        elif activation == "elu": #Exponential Linear Unit
            self.activation_forward = self._elu
            self.activation_backward = self._elu_backward
			
        elif activation == "selu": #Scaled Exponential Linear Unit
            self.activation_forward = self._selu
            self.activation_backward = self._selu_backward
			
        elif activation == "gelu": #Gaussian Exponential Linear Unit
            self.activation_forward = self._gelu
            self.activation_backward = self._gelu_backward
			
        elif activation == "prelu": #Parametric Rectified Linear Unit
            self.activation_forward = self._prelu
            self.activation_backward = self._prelu_backward
			
        elif activation == "brelu": #Bipolar Rectified Linear Unit
            self.activation_forward = self._brelu
            self.activation_backward = self.brelu_backward
			
        elif activation == "isru": #Inverse Square Root Unit (Somewhat Better Performance Then ELU But Pretty Much The Same)
            self.activation_forward = self._isru
            self.activation_backward = self.isru_backward
		
        else:
            self.activation_forward = self._NoActivation
            self.activation_backward = self._NoActivation_backward


    # Printout of the model parameters
    def __str__(self):
        s = self.name + " Layer:\n"
        s += "\tlearning_rate (alpha): " + str(self.alpha) + "\n"
        s += "\tinput_shape: (" + str(self._input_shape) + ")\n"
        s += "\tnum_units: " + str(self._num_units) + "\n"
        # parameters
        s += "\tparameters:\n"
        s += "\t\t W shape: " + str(self.W.shape)+"\n"
        s += "\t\t b shape: " + str(self.b.shape) + "\n"
        s += "activation function: " + self._activation + "\n"
        if self._activation == "leaky_relu":
            s += "\t\tleaky relu parameters:\n"
            s += "\t\t\tleaky_relu_d: " + str(self.leaky_relu_d)+"\n"
        #optimization
        if self._optimization != None:
            s += "\toptimization: " + str(self._optimization) + "\n"
            if self._optimization == "adaptive":
                s += "\t\tadaptive parameters:\n"
                s += "\t\t\tcont: " + str(self.adaptive_cont)+"\n"
                s += "\t\t\tswitch: " + str(self.adaptive_switch)+"\n"
        s += self.regularization_str()
        return s
    def regularization_str(self) :
        s = "regularization: " + str(self.regularization) + "\n"
        if (self.regularization == "L2"):
            s += "\tL2 Parameters: \n" 
            s += "\t\tlambda: " + str(self.L2_lambda) + "\n"
        elif (self.regularization == "dropout"):
            s += "\tdropout Parameters: \n"
            s += "\t\tkeep prob: " + str(self.dropout_keep_prob) + "\n"
        return s

    # Service routinse
    def set_train(self, set_parameter_train):
        self.is_train = set_parameter_train
        
    # Service routine
    def _get_W_shape(self):
        if self._ConvMode == True:
            result = (self._num_units, *(self.get_W_init_factor()))
            return result

        else:
            result = (self._num_units, *(self._input_shape))
            return result

    
    # We use external set waits to enable re-initiat the Ws when needed.
    def init_weights(self, W_initialization):
        self.b = np.zeros((self._num_units,1), dtype=float)

        if self._ConvMode == True:
            _is = self.get_W_init_factor()

        else:
            _is = self._input_shape


        if W_initialization == "zeros":
            self.W = np.full(*self._get_W_shape(), self.alpha)
        elif W_initialization == "random":
            self.random_scale = 0.01   
            self.W = np.random.randn(*self._get_W_shape()) * self.random_scale
        elif W_initialization == "He":
            self.W = np.random.randn(*self._get_W_shape()) * np.sqrt(2.0/sum(_is))
        elif W_initialization == "Xaviar":
            self.W = np.random.randn(*self._get_W_shape()) * np.sqrt(1.0/sum(_is))
        else:   # init by loading values of the Ws and b from external file
            try:
                with h5py.File(W_initialization, 'r') as hf:
                    self.W = hf['W'][:]
                    self.b = hf['b'][:]
            except (FileNotFoundError):
                raise NotImplementedError("Unrecognized initialization:", W_initialization)

    # add the regularization values to the cost
    def regularization_cost(self, m):
        if (self.regularization != "L2"):
            return 0
        return self.L2_lambda* np.sum(np.square(self.W)) /(2*m)

    # --------------- Activation Functions -----------------
	
	#No Activation
    def _NoActivation(self, Z):
        return Z
    def _NoActivation_backward(self, dZ):
        return dZ

	#Softmax
    def _softmax(self, Z):
        eZ = np.exp(Z)
        A = eZ/np.sum(eZ, axis=0)
        return A    
    def _softmax_backward(self, dZ):
        #an empty backward functio that gets dZ and returns it
        #just to comply with the flow of the model
        return dZ

	#Trim Softmax
    def _trim_softmax(self, Z):
        with np.errstate(over='raise', divide='raise'):
            try:
                eZ = np.exp(Z)
            except FloatingPointError:
                Z = np.where(Z > 100, 100,Z)
                eZ = np.exp(Z)
        A = eZ/np.sum(eZ, axis=0)
        return A

	#Sigmoid
    def _sigmoid(self,Z):
        A = 1/(1+np.exp(-Z))
        return A
    def _sigmoid_backward(self,dA):
        A = self._sigmoid(self._Z)
        dZ = dA * A * (1-A)
        return dZ

	#Trim Sigmoid
    def _trim_sigmoid(self,Z):
        with np.errstate(over='raise', divide='raise'):
            try:
                A = 1/(1+np.exp(-Z))
            except FloatingPointError:
                Z = np.where(Z < -100, -100,Z)
                A = A = 1/(1+np.exp(-Z))
        TRIM = self.activation_trim
        if TRIM > 0:
            A = np.where(A < TRIM,TRIM,A)
            A = np.where(A > 1-TRIM,1-TRIM, A)
        return A
    def _trim_sigmoid_backward(self,dA):
        A = self._trim_sigmoid(self._Z)
        dZ = dA * A * (1-A)
        return dZ

	#ReLU
    def _relu(self,Z):
        A = np.maximum(0,Z)
        return A
    def _relu_backward(self,dA):
        print("000")
        print(self._Z.shape)
        print("000")
        dA = dA.reshape(self._Z.shape)
        dZ = np.where(self._Z <= 0, 0, dA)
        return dZ
    
	#LReLU (Leaky Rectified Linear Unit)
    def _leaky_relu(self,Z):
        A = np.where(Z > 0, Z, self.leaky_relu_d * Z)
        return A
    def _leaky_relu_backward(self,dA):
        #When Z <= 0, dZ = self.leaky_relu_d * dA
        dZ = np.where(self._Z <= 0, self.leaky_relu_d * dA, dA)
        return dZ
    
	#tanh (Hyperbolic Tangent)
    def _tanh(self,Z):
        A = np.tanh(Z)
        return A
    def _tanh_backward(self,dA):
        A = self._tanh(self._Z)
        dZ = dA * (1-A**2)
        return dZ
 
 	#Trim tanh (Trim Hyperbolic Tangent)
    def _trim_tanh(self,Z):
        A = np.tanh(Z)
        TRIM = self.activation_trim
        if TRIM > 0:
            A = np.where(A < -1+TRIM,TRIM,A)
            A = np.where(A > 1-TRIM,1-TRIM, A)
        return A
    def _trim_tanh_backward(self,dA):
        A = self._trim_tanh(self._Z)
        dZ = dA * (1-A**2)
        return dZ
	
	#Arctan	
    def _arctan(self,Z):
        A = np.arctan(Z)
        return A
    def _arctan_backward(self,dA):
        A = self._arctan(self._Z)
        dZ = dA * 1 / (1+A**2)
        return dZ

    #ELU (Exponential Linear Unit)
    def _elu(self,Z):
        A = np.where(Z > 0, Z, self.alpha*(np.exp(Z) - 1))
        return A
    def _elu_backward(self,dA):
        dZ = np.where(self._Z <= 0, dA * (self._elu(self._Z) + self.alpha), dA)
        return dZ

    #SELU (Scaled Exponential Linear Unit)
    def _selu(self,Z):
        A = np.where(Z > 0, self.selu_lambda * Z, self.selu_lambda*(self.selu_alpha*np.exp(Z) - self.selu_alpha))
        return A
    def _selu_backward(self,dA):
        dZ = np.where(self._Z > 0, dA * (self.selu_lambda * 1), dA * (self.selu_lambda * (self.selu_alpha*np.exp(self._Z))))
        return dZ
    
    #GELU (Gaussian Error Linear Unit) 
    def _gelu(self,Z):
        return 1 #1 Is placed when the function is there as placement
    def _gelu_backward(self,dA):
        return 1 #1 Is placed when the function is there as placement
    
    #PReLU (Parametric Rectified Linear Unit)
    def _prelu(self,Z):
        A = np.where(Z >= 0, Z, self.alpha * Z)
        return A
    def _prelu_backward(self,dA):
        dZ = np.where(self._Z >= 0, dA, dA * self.alpha)
        return dZ

    # -----------------------------------------
    # Forward propagation of the layer. 
    # -----------------------------------------
    # -----------------------------------------
    
    # dropout settings. If no dropout, will work only in the train phase
    def forward_dropout(self, A_prev):
        if (self.regularization == "dropout" and self.is_train):
            self._D = np.random.rand(*A_prev.shape)
            self._D = np.where(self._D > self.dropout_keep_prob, 0, 1)
            A_prev *= self._D
            A_prev /= self.dropout_keep_prob
        return np.array(A_prev, copy=True)


    # MAIN forward function of the layer. do both - the linear and the logic (activation) phases
    def forward_propagation(self, A_prev):
        if self._ConvMode == True:
            self.prev_A = np.transpose(A_prev, (3, 0, 1, 2))

            self.prev_A  = DLConv.im2col_indices(self.prev_A, self.filter_size, self.padding, self.strides)

            W_temp = self.W

            self.W = self.W.reshape(self.num_filters, -1)

            self._Z = self.W @ self.prev_A + self.b
            A = self.activation_forward(self._Z)
            A = A.reshape(self.num_filters, self.h_out, self.w_out, -1)
            self.W = W_temp

        else:
            self._A_prev = self.forward_dropout(A_prev)
            self._Z = self.W @ self._A_prev + self.b        
            A = self.activation_forward(self._Z)

        return A

    # Backward, if dropout (backward is also in the train mode)
    def backward_dropout(self, dA_prev):
        dA_prev *= self._D
        dA_prev /= self.dropout_keep_prob
        return dA_prev

    # MAIN backword function of the layer
    def backward_propagation(self, dA):
        if self._ConvMode == True:
            m = dA.shape[-1]

            self.W_temp = self.W
            self.W = self.W.reshape(self.num_filters, -1)
        
        
            dA = dA.reshape(self.num_filters, -1)
            self.db = np.sum(dA, keepdims=True, axis=1)

            dZ = self.activation_backward(dA)
            dA_prev = self.W.T @ dZ

            prev_A_shape = (m, *self._input_shape)
            dA_prev = DLConv.col2im_indices(dA_prev, prev_A_shape, self.filter_size, self.padding, self.strides)
            dA_prev = np.transpose(dA_prev, (1, 2, 3, 0))
            self.dW = (1.0/m) * (dZ @ self.prev_A.T)
            self.dW = self.dW.reshape(self.W_temp.shape)
        
            self.W = self.W_temp

            if self.regularization == 'L2':
                m1 = dA_prev.shape[-1]
                self.dW += (self.L2_lambda/m1) * self.W

            if (self.regularization == "dropout"):
                dA_prev = self.backward_dropout(dA_prev)
        
        else:
            m = self._A_prev.shape[1]
            dZ = self.activation_backward(dA) 

            db_m_values = dZ * np.full((1,self._A_prev.shape[1]),1)
            self.db = (1.0/m) * np.sum(db_m_values, keepdims=True, axis=1)
            
            self.dW = (1.0/m) * (dZ @ self._A_prev.T) 
            if self.regularization == 'L2':
                m1 = dZ.shape[-1]
                self.dW += (self.L2_lambda/m1) * self.W
            dA_prev = self.W.T @ dZ
            if (self.regularization == "dropout"):
                dA_prev = self.backward_dropout(dA_prev)
            
        return dA_prev

    # Update parameters - implement both regular and adaptive 
    def update_parameters(self, t=1):
        if self._optimization == 'adaptive':
            self._adaptive_alpha_W *= np.where(self._adaptive_alpha_W * self.dW > 0, self.adaptive_cont, -self.adaptive_switch)
            self._adaptive_alpha_b *= np.where(self._adaptive_alpha_b * self.db > 0, self.adaptive_cont, -self.adaptive_switch)
            self.W -= self._adaptive_alpha_W                               
            self.b -= self._adaptive_alpha_b 
        
        elif self._optimization == 'adam':
            self.adam_v_dW = self.adam_beta1 * self.adam_v_dW + (1-self.adam_beta1) * self.dW
            self.adam_v_dW_wave = self.adam_v_dW / (1 - (self.adam_beta1**t))

            self.adam_v_db = self.adam_beta1 * self.adam_v_db + (1 - self.adam_beta1) * self.db
            self.adam_v_db_wave = self.adam_v_db / (1 - (self.adam_beta1**t))

            self.adam_s_dW = self.adam_beta2 * self.adam_s_dW + (1 - self.adam_beta2)*(self.dW**2)
            self.adam_s_dW_wave = self.adam_s_dW / (1 - (self.adam_beta2**t))

            self.adam_s_db = self.adam_beta2 * self.adam_s_db + (1 - self.adam_beta2)*(self.db**2)
            self.adam_s_db_wave = self.adam_s_db / (1 - (self.adam_beta2**t))

            self.W -= self.alpha * (self.adam_v_dW_wave / np.sqrt(self.adam_s_dW_wave + self.adam_epsilon)) 
            self.b -= self.alpha * (self.adam_v_db_wave / np.sqrt(self.adam_s_db_wave + self.adam_epsilon))
        else:
            self.W -= self.alpha * self.dW                               
            self.b -= self.alpha * self.db

    # enable save of the parameters of the layer (After the train phase)
    def save_weights(self,path,file_name):
        if not os.path.exists(path):
            os.makedirs(path)

        with h5py.File(path+"/"+file_name+'.h5', 'w') as hf:
            hf.create_dataset("W",  data=self.W)
            hf.create_dataset("b",  data=self.b)
    
    def restore_weights(self, file_path):
        with h5py.File(file_path+"/"+self.name+'.h5', 'r') as hf:
            if self.W.shape != hf['W'][:].shape:
                raise ValueError(f"Wrong W shape: {hf['W'][:].shape} and not {self.W.shape}")
            self.W = hf['W'][:]
            if self.b.shape != hf['b'][:].shape:
                raise ValueError(f"Wrong b shape: {hf['b'][:].shape} and not {self.b.shape}")
            self.b = hf['b'][:]

    def get_W_init_factor(self):
        return (self._input_shape[0], (self.filter_size[0]), (self.filter_size[1]))




class DLConv(DLLayer):
    def __init__(self, name, num_filters, input_shape, filter_size, strides, padding, 
                activation="relu", W_initialization="He", learning_rate= 0.01, 
                optimization="adam", regularization = None):
        self.name = name
        self.num_filters = num_filters
        self._input_shape = input_shape
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self._activation = activation
        self.alpha = learning_rate
        self._optimization = optimization
        self.regularization = regularization
        _input_shape = self._input_shape
        DLLayer.__init__(self, name, num_filters, _input_shape, 
            activation, W_initialization, learning_rate, optimization, regularization, True)

        if self.padding == 'Valid':
            self.padding = (0, 0)
        elif self.padding == 'Same':
            self.padding = ((((self.filter_size[0]) - 1) / 2), (((self.filter_size[1]) - 1) / 2))
        else:
            self.padding = (self.padding[0], self.padding[1])

        self.w_out = math.floor(((self._input_shape[2] + 2*(self.padding[1]) - self.filter_size[1]) / self.strides[1]) + 1)
        self.h_out = math.floor(((self._input_shape[1] + 2*(self.padding[0]) - self.filter_size[0]) / self.strides[0]) + 1)

    def __str__(self):
        s = "Convolutional " + super(DLConv, self).__str__()
        s += "\tConvolutional parameters:\n"
        s += f"\t\tfilter size: {self.filter_size}\n"
        s += f"\t\tstrides: {self.strides}\n"
        s += f"\t\tpadding: {self.padding}\n"
        s += f"\t\toutput shape: {(self.num_filters, self.h_out, self.w_out)}\n"
        return s
    
    @staticmethod
    def im2col_indices(A, filter_size = (3,3), padding=(1,1),stride=(1,1)):
        """ An implementation of im2col based on some fancy indexing """  
        # Zero-pad the input
        A_padded = np.pad(A, ((0, 0), (0, 0), (padding[0], padding[1]), (padding[0], padding[1])), mode='constant', constant_values=(0,0))

        k, i, j = DLConv.get_im2col_indices(A.shape, filter_size, padding, stride)

        cols = A_padded[:, k, i, j]
        C = A.shape[1]
        cols = cols.transpose(1, 2, 0).reshape(filter_size[0] * filter_size[1] * C, -1)
        return cols

    @staticmethod
    def get_im2col_indices(A_shape, filter_size=(3,3), padding=(1,1),stride=(1,1)):
        # First figure out what the size of the output should be
        m, C, H, W = A_shape
        out_height = int((H + 2 * padding[0] - filter_size[0]) / stride[0]) + 1
        out_width = int((W + 2 * padding[1] - filter_size[1]) / stride[1]) + 1

        i0 = np.repeat(np.arange(filter_size[0]), filter_size[1])
        i0 = np.tile(i0, C)
        i1 = stride[0] * np.repeat(np.arange(out_height), out_width)
        j0 = np.tile(np.arange(filter_size[1]), filter_size[0] * C)
        j1 = stride[1] * np.tile(np.arange(out_width), out_height)
        i = i0.reshape(-1, 1) + i1.reshape(1, -1)
        j = j0.reshape(-1, 1) + j1.reshape(1, -1)

        k = np.repeat(np.arange(C), filter_size[0] * filter_size[1]).reshape(-1, 1)

        return (k, i, j)

    @staticmethod
    def col2im_indices(cols, A_shape, filter_size=(3,3), padding=(1,1),stride=(1,1)):
        """ An implementation of col2im based on fancy indexing and np.add.at """
        m, C, H, W = A_shape
        H_padded, W_padded = H + 2 * padding[0], W + 2 * padding[1]
        A_padded = np.zeros((m, C, H_padded, W_padded), dtype=cols.dtype)
        k, i, j = DLConv.get_im2col_indices(A_shape, filter_size, padding, stride)
        cols_reshaped = cols.reshape(C * filter_size[0] * filter_size[1], -1, m)
        cols_reshaped = cols_reshaped.transpose(2, 0, 1)
        np.add.at(A_padded, (slice(None), k, i, j), cols_reshaped)
        if padding[0] == 0 and padding[1] == 0:
            return A_padded
        if padding[0] == 0:
            return A_padded[:, :, :, padding[1]:-padding[1]]
        if padding[1] == 0:
            return A_padded[:, :, padding[0]:-padding[0], :]
        return A_padded[:, :, padding[0]:-padding[0], padding[1]:-padding[1]]

class DLMaxpooling (DLLayer):
    def __init__(self, name, input_shape, filter_size, strides):
        self.filter_size = filter_size
        self.strides = strides
        
        self.w_out = (input_shape[2] - filter_size[1]) // strides[1] + 1
        self.h_out = (input_shape[1] - filter_size[0]) // strides[0] + 1

        super().__init__(name, 1, input_shape)

    def update_parameters(self):
        pass

    def __str__(self):
        s = f"Maxpooling {self.name} Layer:\n"
        s += f"\tinput_shape: {self._input_shape}\n"
        s += "\tMaxpooling parameters:\n"
        s += f"\t\tfilter size: {self.filter_size}\n"
        s += f"\t\tstrides: {self.strides}\n"
        # number of output channels == number of input channels
        s += f"\t\toutput shape: {(self._input_shape[0], self.h_out, self.w_out)}\n"
        return s
    def forward_propagation(self, prev_A):
        # first transpose A_prev from (C,H,W,m) to (m,C,H,W)
        prev_A = prev_A.transpose(3, 0, 1, 2)
        m,C,H,W = prev_A.shape
        prev_A = prev_A.reshape(m*C,1,H,W)
        self.prev_A = DLConv.im2col_indices(prev_A, self.filter_size, padding = (0,0), stride = self.strides)   
        self.max_indexes = np.argmax(self.prev_A,axis=0)
        Z = self.prev_A[self.max_indexes,range(self.max_indexes.size)]
        Z = Z.reshape(self.h_out,self.w_out,m,C).transpose(3,0,1,2)
        return Z
    def backward_propagation(self,dZ):
        dA_prev = np.zeros_like(self.prev_A) 
        # transpose dZ from C,h,W,C to H,W,m,c and flatten it
        # Then, insert dZ values to dA_prev in the places of the max indexes
        dZ_flat = dZ.transpose(1,2,3,0).ravel()
        dA_prev[self.max_indexes,range(self.max_indexes.size)] = dZ_flat       
        # get the original prev_A structure from col2im
        m = dZ.shape[-1]
        C,H,W = self._input_shape
        shape = (m*C,1,H,W)
        dA_prev = DLConv.col2im_indices(dA_prev, shape, self.filter_size, padding=(0,0),stride=self.strides)
        dA_prev = dA_prev.reshape(m,C,H,W).transpose(1,2,3,0)
        return dA_prev

class DLFlatten(DLLayer):
   def __init__(self, name, input_shape): 
        DLLayer.__init__(self, name, 1, input_shape)
        self.input_shape = input_shape
        self.name = name
   def __str__(self):
        s = f"Flatten {self.name} Layer:\n"
        s += f"\tinput_shape: {self.input_shape}\n"
        return s
   def forward_propagation(self, prev_A):
        m = prev_A.shape[-1]
        A = np.copy(prev_A.reshape(-1,m))
        return A
   def backward_propagation(self,dA):
        m = dA.shape[-1]
        dA_prev = np.copy(dA.reshape(*(self.input_shape),m))
        return dA_prev
   def update_parameters(self):
        pass