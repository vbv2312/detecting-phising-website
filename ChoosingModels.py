import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_urls = pd.read_csv("datasets/phishcoop.csv")

import pandas as pd


def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

data_urls=clean_dataset(data_urls)
# print(data_urls.head())
# print(data_urls.columns)
# print(data_urls.shape)
# print(data_urls.info())

data_urls.hist(bins = 50,figsize = (15,15))
plt.show()

# %%
data_urls = data_urls.drop('id', 1) #removing unwanted column

x = data_urls.iloc[:, :-1].values
y = data_urls.iloc[:, -1].values

#print(x[:1],y[:1])

import MODELS.LinearRegression as linearRegression
import MODELS.SimpleVectorMachine as svm
import MODELS.DecisionTree as decisionTree
linearRegression.models(x, y)
svm.models(x, y)
decisionTree.model(x,y)
