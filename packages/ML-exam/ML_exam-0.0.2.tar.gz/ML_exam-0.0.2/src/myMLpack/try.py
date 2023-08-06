import numpy as np
np.random.seed(2)

X = np.random.randn(2,3)
y = np.random.randn(1,3) > 0

def sig(Z):
    s = 1/(1+np.exp(-Z)) 
    return s

def tanh(Z):
    s = (np.exp(Z) - np.exp(-Z)) / (np.exp(Z) + np.exp(-Z)) 
    return s

def relu(Z):
    s = np.maximum(0,Z) 
    return s

def leaky_relu(Z):
    s = np.maximum(0.01,Z)
    return s

def shape(X,y):
    n_x = X.shape[0]
    n_h = 4
    n_y = y.shape[0] 

    return (n_x, n_h, n_y)

n_x, n_h, n_y = shape(X,y)

def initial_params(n_x, n_h, n_y):
    np.random.seed(2)
    w1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h,1))
    # b1 = np.array([0.926262883, 0.186899756, 0.590227149, 0.940082767]).reshape(-1,1)

    w2 = np.random.randn(1, n_h) * 0.01
    b2 = np.zeros((n_y, 1))
    # b2 = np.array([1]).reshape(-1,1)

    return {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}

params = initial_params(n_x, n_h, n_y)

def fwd_prop(X,params):
    w1 = params['w1']
    b1 = params['b1']
    w2 = params['w2']
    b2 = params['b2']

    z1 = np.dot(w1,X) + b1
    a1 = tanh(z1)

    z2 = np.dot(w2,a1) + b2
    a2 = sig(z2)

    return a2, {'z1': z1, 'a1': a1, 'z2': z2, 'a2': a2}

a2, catch = fwd_prop(X,params)

def compute_cost(a2,y):
    m = y.shape[1]
    logp = np.multiply(y,np.log(a2)) + np.multiply((1-y), np.log(1-a2))
    cost = -np.sum(logp)/m
    
    return cost

compute_cost(a2,y)

def bwd_prop(params, catch, X, y):
    w1 = params['w1']
    b1 = params['b1']
    w2 = params['w2']
    b2 = params['b2']

    a1 = catch['a1']
    a2 = catch['a2']

    m = y.shape[1]

    dz2 = a2 - y 
    dw2 = np.dot(dz2, a1.T)/m
    db2 = np.sum(dz2,  axis=1,  keepdims=True) / m

    dz1 = np.dot(w2.T, dz2)*(1-a1**2)
    dw1 = np.dot(dz1, X.T)/m
    db1 = np.sum(dz1,  axis=1,  keepdims=True) / m


    return {'dw1':dw1, 'db1': db1, 'dw2': dw2, 'db2': db2}

grade = bwd_prop(params, catch, X, y)

def update(params, grade, lr = 0.01):
    w1 = params['w1']
    b1 = params['b1']
    w2 = params['w2']
    b2 = params['b2']

    dw1 = grade['dw1']
    db1 = grade['db1']
    dw2 = grade['dw2']    
    db2 = grade['db2']    

    w1 = w1 - (lr * dw1)
    b1 = b1 - (lr * db1)
    w2 = w2 - (lr * dw2)
    b2 = b2 - (lr * db2)

    return {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}

def NN(X, Y, itr = 10000, print_cost = False):
    np.random.seed(3)
    n_x = shape(X,Y)[0]
    n_y = shape(X,Y)[2]
    n_h = shape(X,Y)[1]

    parameters = initial_params(n_x, n_h, n_y)

    for i in range(0, itr):
        A2, cache = fwd_prop(X, parameters)
        cost = compute_cost(A2, y)
        grades = bwd_prop(parameters, cache, X, Y)
        parameters = update(parameters, grades, lr= 0.01)

        if print_cost and i%1000 == 0:
            print(f'cost {i}:{cost}')

    return parameters

fin_parameters = NN(X,y, print_cost= True)


def predict_dec (parameters, X):

    A2, _ = fwd_prop(X, params=parameters)
    predictions = (A2>0.5)
    return predictions
