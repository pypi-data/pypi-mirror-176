def fun1(num):
    temp = "Empty"
    if(num==4):
        temp = """
        import numpy as np

        X = np.array(([2,9],[1,5],[3,6]),dtype='float') # x = (hrs of sleep, hrs of study)
        Y = np.array(([92],[86],[89]),dtype='float') # y = (score on test)

        #scale Units
        X = X/np.amax(X,axis=0)# Max of X array
        Y = Y/100 #Max test score is 100

        class NN(object):
            def __init__(self):
                self.inputsize = 2
                self.outputsize = 1
                self.hiddensize = 3
                self.W1 = np.random.randn(self.inputsize,self.hiddensize) #(3X2 weight matrix from input to hidden layer)
                self.W2 = np.random.randn(self.hiddensize,self.outputsize) #(3X1 weight matrix from hidden to output layer)
                
            
            def sigmoidal(self,s):
                return 1/(1+np.exp(-s))
            
            def sigmoidalprime(self,s):
                return s*(1-s)
            
            def forward(self,X):
                self.z = np.dot(X,self.W1) #dot product of X(input) and first set of 3X2 weights
                self.z2 = self.sigmoidal(self.z) #activation function
                self.z3 = np.dot(self.z2,self.W2) #dot product of hidden layer z2 and second set of 3X1 weights
                op = self.sigmoidal(self.z3) #final activation function
                return op
            
            def backward(self,x,y,o):
                self.o_error = y-o
                self.o_delta = self.o_error*self.sigmoidalprime(o)
                self.z2_error = self.o_delta.dot(self.W2.T)
                self.z2_delta = self.z2_error*self.sigmoidalprime(self.z2)
                self.W1 = self.W1 + x.T.dot(self.z2_delta)
                self.W2 = self.W2 + self.z2.T.dot(self.o_delta)
            
            def train(self,x,y):
                o = self.forward(x)
                self.backward(x, y, o) 
                
            
        obj = NN()

        for i in range(1000):
            print("Input\n"+str(X))
            print("Actual Output\n"+str(Y))
            print("Predicted Output\n"+str(obj.forward(X)))
            print("loss" + str(np.mean(np.square(Y-obj.forward(X)))))
            obj.train(X, Y)

        """
    elif(num==5):
            temp = """
            import numpy as np

def compute_next_state(state , weight):
    next_state = np.where(weight @ state >= 0, +1, -1)
    #next_state = np.matmul(weight,state)
    print(next_state)
    return next_state


#@' is shorthand for np.matmul()
#numpy.where() returns the indices of the elements in an input array
#where the given condt is satisfied 


def compute_final_state(initial_state, weight, max_iter=1000):
    previous_state = initial_state
    next_state = compute_next_state(previous_state, weight)
    is_stable = np.all(previous_state == next_state)
    
    n_iter = 0 
    while(not is_stable) and (n_iter <= max_iter):
        previous_state = next_state
        next_state = compute_next_state(previous_state, weight)
        is_stable = np.all(previous_state == next_state)
        n_iter += 1
    
    return previous_state, is_stable, n_iter


initial_state = np.array([1,-1,-1,-1])
weight = np.array([
                   [0,-1,-1,1],
                   [-1,0,1,-1],
                   [-1,1,0,-1],
                   [1,-1,-1,0]
                  ])


final_state , is_stable, n_iter = compute_final_state(initial_state, weight)

print("Final State: ",final_state)
print("is_stable: ",is_stable)
print("Iteration: ",n_iter)


            """

            print("""
            import numpy as np

def compute_next_state(state , weight):
    next_state = np.where(weight @ state >= 0, +1, -1)
    #next_state = np.matmul(weight,state)
    print(next_state)
    return next_state


#@' is shorthand for np.matmul()
#numpy.where() returns the indices of the elements in an input array
#where the given condt is satisfied 


def compute_final_state(initial_state, weight, max_iter=1000):
    previous_state = initial_state
    next_state = compute_next_state(previous_state, weight)
    is_stable = np.all(previous_state == next_state)
    
    n_iter = 0 
    while(not is_stable) and (n_iter <= max_iter):
        previous_state = next_state
        next_state = compute_next_state(previous_state, weight)
        is_stable = np.all(previous_state == next_state)
        n_iter += 1
    
    return previous_state, is_stable, n_iter


initial_state = np.array([1,-1,-1,-1])
weight = np.array([
                   [0,-1,-1,1],
                   [-1,0,1,-1],
                   [-1,1,0,-1],
                   [1,-1,-1,0]
                  ])


final_state , is_stable, n_iter = compute_final_state(initial_state, weight)

print("Final State: ",final_state)
print("is_stable: ",is_stable)
print("Iteration: ",n_iter)


            """)


    return ()