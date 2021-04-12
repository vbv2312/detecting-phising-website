import pandas as pd

data_urls = pd.read_csv("urldata.csv")

# print(data_urls.head())
# print(data_urls.columns)
# print(data_urls.shape)
# print(data_urls.info())
# data_urls.hist(bins = 50,figsize = (15,15))
# plt.show()

# %%

dataset = data_urls.drop('Domain', 1)  # removing unwanted column

x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1:].values

import MODELS.LinearRegression as linearRegression

linearRegression.models(x, y)
