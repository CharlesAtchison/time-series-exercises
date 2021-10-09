import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error
from math import sqrt

def plot_samples(target_var):
    '''
   plot each attribute 
   '''
    plt.figure(figsize = (12,4))
    sns.lineplot(data=train[target_var], label='train')
    sns.lineplot(data=validate[target_var], label='validate')
    sns.lineplot(data=test[target_var], label='test')
    plt.title(target_var.title())
    plt.legend()
    
def evaluate(target_var):
    '''
    the evaluate function will take in the actual values and the predicted values
    and compute the mean_squared_error and then take the sqrt returning a rounded rmse
    '''
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])),0)
    return rmse

def plot_and_eval(target_var):
    '''
    a function to evaluate forecasts by computing the rmse and plot train and validate along with predictions
    '''
    plot_samples(target_var)
    sns.lineplot(data=yhat_df[target_var], label='RMSE')
    plt.title(target_var)
    rmse = evaluate(target_var)
    print(target_var, f'--RMSE: {rmse:.0f}')
    plt.show()

def append_eval_df(model_type, target_var):
    '''
    this function will take in the model type as a string, target variable
    as a string, and run the evaluate function to compute rmse, 
    and append to the dataframe a row with the model type, 
    target variable and rmse. 
    '''
    rmse = evaluate(target_var)
    d= {'model_type':[model_type], 'target_var':[target_var], 'rmse':[rmse]}
    d= pd.DataFrame(d)
    return eval_df.append(d, ignore_index= True)

def time_split(df, train_size = .5, validate_size = .3):
    '''Splits time series data based on percentages and returns train, validate, test THE
    DATAFRAME MUST BE CHRONOLOGICALLY SORTED!'''
    t_size = int(len(df) * train_size)
    v_size = int(len(df) * validate_size)
    end = t_size + v_size
    return df[0:t_size], df[t_size:end], df[end:len(df)+1]