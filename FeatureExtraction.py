
from urllib.parse import urlparse  # Used in 1,5,7
import re  # Used in 2,8 -- Regular expression operations

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



#7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain) 

def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0


#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0
#example- tinyURL("https://bitly.com/") return 1


# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate
    print(urlparse(url).netloc)
#example- tinyURL("https://bit-ly.com/") return 1


def extractFeatures(url,label):
    return [i for i in range(18)]
