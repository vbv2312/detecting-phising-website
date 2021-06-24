from urllib.parse import urlparse  # Used in 1,5,7
import re  # Used in 2,8 -- Regular expression operations
import datetime
import whois
from datetime import datetime
import ipaddress


# 1
def getDomain(url):
    result = urlparse(url)

    domain = result.netloc
    if "www." in domain:
        domain = domain.replace("www.", "")

    return domain


# 2
def havingIp(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip


# 3
def havingAtSign(url):
    return 1 if '@' in url else 0  # 0 if @ not not present else 1


# 4
def urlLengthFactor(url):
    url_length = len(url)
    if url_length < 54:
        return 0

    return 1

    # 0 -> legitimate 1->Phishing


# 5
def getDepth(url):
    url_path = urlparse(url).path
    # print(url_path)
    url_parts = url_path.split('/')
    url_depth = 0

    for i in url_parts:
        if i != "":
            url_depth += 1

    return url_depth  # Return the depth of url using no. of subdirectory in url path


# 6
def reDirection(url):
    pos = url.rfind("//")  # Finds last occurence of // in url

    if pos < 7:
        return 0

    if url[:5].upper() == "HTTPS" and pos == 7:
        return 0

    return 1  # only 1 // must be present and that only at index less than 7


# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)

def httpDomain(url):
    domain = urlparse(url).netloc
    if 'https' in domain.lower():
        return 1
    else:
        return 0


# listing shortening services
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
    match = re.search(shortening_services, url)
    if match:
        return 1
    else:
        return 0


# example- tinyURL("https://bitly.com/") return 1


# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1  # phishing
    else:
        return 0  # legitimate
    # print(urlparse(url).netloc)


# example- tinyURL("https://bit-ly.com/") return 1

# 10. Whether domain is registered or not
def is_registered(domain_name):
    try:
        w = whois.whois(domain_name)
    except Exception:
        return 0

    return 1 if bool(w.domain_name) else 0

"""#### **Age of Domain**

This feature can be extracted from WHOIS database. Most phishing websites live for a short period of time. The minimum age of the legitimate domain is considered to be 12 months for this project. Age here is nothing but different between creation and expiration time.

If age of domain < 6 months, the value of this feature is 1 (phishing) else 0 (legitimate).
"""


# 12.Survival time of domain: The difference between termination time and creation time (Domain_Age)

from urllib.request import urlopen

def domainAge(URL):
    if URL == None:
        return 1
    try:
        from htmldate import find_date
        creation_date = find_date(URL)

        with urlopen(URL) as f:
            s=dict(f.getheaders())['Set-Cookie'].split(";")
            expire=""
            for i in s:
                if "Expires" in i:
                    expire = i.split("=")[-1][5:16]

            from datetime import datetime

            expire_date = datetime.strptime(expire, '%d-%b-%Y').date()
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d').date()

            delta = expire_date - creation_date

            if delta.days<180:
                return 1

            return 0

    except:
        return 1



"""#### **End Period of Domain??????????**

This feature can be extracted from WHOIS database. For this feature, the remaining domain time is calculated by finding the different between expiration time & current time. The end period considered for the legitimate domain is 6 months or less  for this project. 

If end period of domain > 3 year, the vlaue of this feature is 1 (phishing) else 0 (legitimate).
"""


# 14.End time of domain: The difference between termination time and current time (Domain_End)
def domainEnd(URL):
    if URL == None:
        return 1
    try:
        with urlopen(URL) as f:
            s=dict(f.getheaders())['Set-Cookie'].split(";")
            expire=""
            for i in s:
                if "Expires" in i:
                    expire = i.split("=")[-1][5:16]
            from datetime import datetime
            expiration_date = datetime.strptime(expire, '%d-%b-%Y').date()

            today = datetime.today().date()
            end = abs((expiration_date - today).days)
            if ((end / 30) < 36):
                end = 0
            else:
                end = 1
            return end

    except:
        print("Error")
        return 1



"""## **3.HTML and JavaScript based Features**

Many features can be extracted that come under this category. Out of them, below mentioned were considered for this project.

*   IFrame Redirection
*   Status Bar Customization
*   Disabling Right Click
*   Website Forwarding

Each of these features are explained and the coded below:
"""
# importing required packages for this section
import requests

"""### **IFrame Redirection**

IFrame is an HTML tag used to display an additional webpage into one that is currently shown. Phishers can make use of the “iframe” tag and make it invisible i.e. without frame borders. In this regard, phishers make use of the “frameBorder” attribute which causes the browser to render a visual delineation. 

If the iframe is empty or repsonse is not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""


# 15. IFrame Redirection (iFrame)
def iframe(response):
    if response == "":
        return 1
    return 0

    '''else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1'''


"""### **Status Bar Customization**

Phishers may use JavaScript to show a fake URL in the status bar to users. To extract this feature, we must dig-out the webpage source code, particularly the “onMouseOver” event, and check if it makes any changes on the status bar

If the response is empty or onmouseover is found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""


# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0


"""### **Disabling Right Click**

Phishers use JavaScript to disable the right-click function, so that users cannot view and save the webpage source code. This feature is treated exactly as “Using onMouseOver to hide the Link”. Nonetheless, for this feature, we will search for event “event.button==2” in the webpage source code and check if the right click is disabled.

If the response is empty or onmouseover is not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""


# 17.Checks the status of the right click attribute (Right_Click)
def rightClick(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1


"""### ** Website Forwarding**
The fine line that distinguishes phishing websites from legitimate ones is how many times a website has been redirected. In our dataset, we find that legitimate websites have been redirected one time max. On the other hand, phishing websites containing this feature have been redirected at least 4 times.
"""


# 18.Checks the number of forwardings (Web_Forwards)
def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1


def extractFeatures(url):
    try:
        response = requests.get(url)
    except:
        response = ""

    return [getDomain(url), havingIp(url), havingAtSign(url), urlLengthFactor(url), getDepth(url), reDirection(url),
            httpDomain(url), tinyURL(url), prefixSuffix(url), is_registered(getDomain(url)), domainAge(url),
            domainEnd(url), iframe(response), mouseOver(response), rightClick(response), forwarding(response)]
