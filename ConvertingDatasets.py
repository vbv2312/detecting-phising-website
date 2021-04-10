# %%
import pandas as pd

# %%
"""
# 1.Legitimate URLs
"""

# %%
data_valid = pd.read_csv("list_of_raw_legitimate_webites.csv")
data_valid.columns = ['URLs']
print(data_valid.shape)  # shape
data_valid.head()

# %%
legiurl = data_valid.copy()
legiurl = legiurl.reset_index(drop=True)
print(legiurl.shape)  # shape
legiurl.head()

# %%
"""
# 2.Phishing Websites
"""

# %%
data_phishing = pd.read_csv("list_of_raw_phishing_websites.csv")
print(data_phishing.shape)  # shape
data_phishing.head()

# %%
phishurl = data_phishing.copy()
phishurl = phishurl.reset_index(drop=True)
print(phishurl.shape)
phishurl.head()

# %%
"""
# Converting DataSets to proper format with features
"""

# %%
import FeatureExtraction

legi_features = []
label = 0

# from datetime import datetime


for i in range(len(legiurl)):
    # now = datetime.now().time()  # time object
    # print(i,now)
    url = legiurl['URLs'][i]
    feature = FeatureExtraction.extractFeatures(url)
    feature.append(label)
    legi_features.append(feature)

print(legi_features.head())

# %%
feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
                 'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record',
                 'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Label']

legitimate = pd.DataFrame(legi_features, columns=feature_names)

print(legitimate.head())
print(legitimate.shape)

legitimate.to_csv('legitimate.csv', index=False)  # Saving in a csv file

# %%
# Converting Phishing Websites
import FeatureExtraction

phish_features = []
label = 1
for i in range(len(phishurl)):
    url = phishurl['url'][i]
    feature = FeatureExtraction.extractFeatures(url)
    feature.append(label)
    phish_features.append(feature)

feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
                 'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record',
                 'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Label']

# Web_Traffic

phishing = pd.DataFrame(phish_features, columns=feature_names)

print(phishing.head())
print(phishing.shape)

# Storing the extracted legitimate URLs features to csv file
phishing.to_csv('phishing.csv', index=False)

# %%
urldata = pd.concat([legitimate, phishing]).reset_index(drop=True)
print(urldata.shape)
print(urldata.head())

# %%
urldata.to_csv('urldata.csv', index=False)
