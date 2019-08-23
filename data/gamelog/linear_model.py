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
def linear(x_train, x_test, y_train, y_test, target):
    reg = LinearRegression().fit(x_train, y_train)
    yard_pred = reg.predict(x_test)
    
    # The coefficients
    print('Coefficients: \n', reg.coef_)

    print('Score: ', reg.score(x_test, y_test))

    # The mean squared error
    print("Mean squared error: %.2f"
        % mean_squared_error(y_test, yard_pred))

    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(y_test, yard_pred))

    # Plot outputs
    plt.figure()
    plt.xlabel(target, fontsize=18)
    plt.ylabel('yards', fontsize=16)
    plt.scatter(x_test, y_test,  color='black')
    plt.plot(x_test, yard_pred, color='blue', linewidth=3)

def adjustedScore(sack, inter, tackle):
    result = sack*1.2 + inter*1.5 + tackle
    print result
    return result

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
        #x_sub.append(adjustedScore(row[2], row[3], row[4]))
        x_sub.append(row[2])
        x.append(x_sub)
        y.append(row[1])
    return (x, y)

# return accuracy
def correlation(target):
    #print getData(target)
    (x, y) = getData(target)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, shuffle=False)
    linear(x_train, x_test, y_train, y_test, target)

def main():
    correlation("sacks")
    correlation("intercep")
    correlation("tackles")
    correlation("avg_sack")
    correlation("avg_int")
    correlation("avg_tackle")
    #correlation("avg_sack, avg_int, avg_tackle")
    plt.show()

main()