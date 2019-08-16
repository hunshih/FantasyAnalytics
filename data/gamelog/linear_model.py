import os
import re
import create_db as DbConn
from sqlite3 import Error
import sys
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

#graph linear model and return the accuracy and regression
def linear(x_train, x_test, y_train, y_test):
    reg = LinearRegression().fit(x_train, y_train)
    yard_pred = reg.predict(x_test)
    
    # The coefficients
    print('Coefficients: \n', reg.coef_)

    # The mean squared error
    print("Mean squared error: %.2f"
        % mean_squared_error(y_test, yard_pred))

    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(y_test, yard_pred))

    # Plot outputs
    plt.scatter(x_test, y_test,  color='black')
    plt.plot(x_test, yard_pred, color='blue', linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()

# return (x_train data, y_train, x_test data, y_test)
def getData(target):
    sql = "SELECT year, yards, " + target + " FROM correlation WHERE name = \'Matthew Stafford\' order by year asc"
    conn = DbConn.create_connection()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    x = []
    y = []
    for row in rows:
        x_sub = []
        x_sub.append(row[2])
        x.append(x_sub)
        y.append(row[1])
    return (x, y)

# return accuracy
def correlation(target, color):
    #print getData(target)
    (x, y) = getData(target)
    print x
    print y
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    #plt.scatter(x_train, y_train)
    #plt.title(target)
    #plt.show()
    print x_train
    print x_test
    linear(x_train, x_test, y_train, y_test)

def main():
    correlation("sacks", "bo")
    '''correlation("intercep", "go")
    correlation("tackles", "ro")
    correlation("avg_sack", "bo")
    correlation("avg_int", "go")
    correlation("avg_tackle", "ro")'''

main()