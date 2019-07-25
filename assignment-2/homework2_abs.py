from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import random
import math

data = load_boston()
X,y = data['data'],data['target']

X_rm = X[:, 5]

def draw_room_price(num):
    plt.scatter(X[:,num],y)


def price_hat(rm,k,b):
    return k*rm+b

def loss_abs(y,y_hat):
    return sum(abs(y_i - y_hat_i) for y_i,y_hat_i in zip(list(y),list(y_hat))) / len(list(y))

def partial_k_abs(x,y, y_hat):
    n = len(y)
    gradient = 0
    for x_i,y_i, y_hat_i in zip( list(x),list(y), list(y_hat)):

        if y_i - y_hat_i > 0:#如果y_i > y_hat_i，|y-y_hat| = y-xk-b  ,导数等于-x
            gradient+=(-1*x_i)

        elif y_i - y_hat_i < 0:#如果y_i > y_hat_i，|y-y_hat| = -y+xk+b  ,导数等于x
            gradient += (1* x_i)

        else:                  #如果y_i == y_hat_i，|y-y_hat| = 0  ,导数等于0
            gradient+=0

    return 1 / n * gradient


def partial_b_abs(y, y_hat):
    n = len(y)
    gradient = 0
    for y_i, y_hat_i in zip(list(y), list(y_hat)):

        if y_i - y_hat_i > 0:#如果y_i > y_hat_i，|y-y_hat| = y-xk-b  ,导数等于-1
            gradient += (-1 )

        elif y_i - y_hat_i < 0:#如果y_i > y_hat_i，|y-y_hat| = -y+xk+b  ,导数等于1
            gradient += 1

        else:                   #如果y_i == y_hat_i，|y-y_hat| = 0  ,导数等于0
            gradient += 0

    return 1 / n * gradient


trying_times = 20000
min_loss = float('inf')

current_k = random.random() * 200 - 100
current_b = random.random() * 200 - 100

learning_rate = 1e-03

update_time = 0

for i in range(trying_times):

    price_by_k_and_b = [price_hat(r, current_k, current_b) for r in X_rm]

    current_loss = loss_abs(y, price_by_k_and_b)

    if current_loss < min_loss:  # performance became better
        min_loss = current_loss
        best_k , best_b = current_k ,current_b
        if i % 50 == 0:
            print(
                'When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))

    k_gradient = partial_k_abs(X_rm, y, price_by_k_and_b)
    b_gradient = partial_b_abs( y, price_by_k_and_b)

    current_k = current_k + (-1 * k_gradient) * learning_rate
    current_b = current_b + (-1 * b_gradient) * learning_rate


X_rm = X[:, 5]
k = 5.3
b = -10.98
price_by_random_k_and_b = [price_hat(r, k, b) for r in X_rm]

draw_room_price(5)
plt.scatter(X_rm, price_by_random_k_and_b)
plt.show()