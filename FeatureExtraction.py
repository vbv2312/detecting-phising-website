
from urllib.parse import urlparse  # Used in 1,5
import re  # Used in 2

#1
def getDomain(url):
    result= urlparse(url)
    
    domain = result.netloc
    
    if "www." in domain:
        domain.replace("www.","")
    
    return domain

#2
def havingIp(url):
    if re.match(r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/.*" , url ):
        return 1
    return 0   

#3
def havingAtSign(url):
    return '@' in url    # False if @ not not present else True 

#4
def urlLengthFactor(url):
    url_length = len(url)
    if url_length<54:
        return 0
    
    elif 54<=url_length<=75:
        return 1
    
    return 2     # 0 -> legitimate 1->suspicious  2->Phishing


#5
def getDepth(url):
    url_path=urlparse(url).path
    print(url_path)
    url_parts=url_path.split('/')
    url_depth=0
    
    for i in url_parts:
        if i!="" :
            url_depth+=1
    
    return url_depth            # Return the depth of url using no. of subdirectory in url path


#6
def reDirection(url):
    pos = url.rfind("//")    #Finds last occurence of // in url
    
    if pos<7:
        return 0
    
    if url[:5].upper()=="HTTPS" and pos==7:
        return 0
    
    return 1    # only 1 // must be present and that only at index less than 7




def extractFeatures(url,label):
    return [i for i in range(18)]
