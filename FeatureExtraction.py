# -*- coding: utf-8 -*-

import regex
from tldextract import extract
import ssl
import socket
from bs4 import BeautifulSoup
import urllib.request
import re
from datetime import datetime
import ipaddress
from urllib.request import urlopen
import requests


def url_having_ip(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip


def url_length(url):
    length = len(url)
    if length < 54:
        return -1
    elif 54 <= length <= 75:
        return 0
    else:
        return 1

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

def url_short(url):
    match = re.search(shortening_services, url)
    if match:
        return 1
    else:
        return 0


def having_at_symbol(url):
    symbol = regex.findall(r'@', url)
    if (len(symbol) == 0):
        return -1
    else:
        return 1


def doubleSlash(url):
    pos = url.rfind("//")  # Finds last occurence of // in url

    if pos < 7:
        return 0

    if url[:5].upper() == "HTTPS" and pos == 7:
        return 0

    return 1  # only 1 // must be present and that only at index less than 7


def prefix_suffix(url):
    subDomain, domain, suffix = extract(url)
    if (domain.count('-')):
        return 1
    else:
        return -1


def sub_domain(url):
    subDomain, domain, suffix = extract(url)
    if (subDomain.count('.') == 0):
        return -1
    elif (subDomain.count('.') == 1):
        return 0
    else:
        return 1


def SSLfinal_State(url):
    try:
        # check wheather contains https
        if (regex.search('^https', url)):
            usehttps = 1
        else:
            usehttps = 0
        # getting the certificate issuer to later compare with trusted issuer
        # getting host name
        subDomain, domain, suffix = extract(url)
        host_name = domain + "." + suffix
        context = ssl.create_default_context()
        sct = context.wrap_socket(socket.socket(), server_hostname=host_name)
        sct.connect((host_name, 443))
        certificate = sct.getpeercert()
        issuer = dict(x[0] for x in certificate['issuer'])
        certificate_Auth = str(issuer['commonName'])
        certificate_Auth = certificate_Auth.split()
        if (certificate_Auth[0] == "Network" or certificate_Auth == "Deutsche"):
            certificate_Auth = certificate_Auth[0] + " " + certificate_Auth[1]
        else:
            certificate_Auth = certificate_Auth[0]
        trusted_Auth = ['Comodo', 'Symantec', 'GoDaddy', 'GlobalSign', 'DigiCert', 'StartCom', 'Entrust', 'Verizon',
                        'Trustwave', 'Unizeto', 'Buypass', 'QuoVadis', 'Deutsche Telekom', 'Network Solutions',
                        'SwissSign', 'IdenTrust', 'Secom', 'TWCA', 'GeoTrust', 'Thawte', 'Doster', 'VeriSign']
        # getting age of certificate
        startingDate = str(certificate['notBefore'])
        endingDate = str(certificate['notAfter'])
        startingYear = int(startingDate.split()[3])
        endingYear = int(endingDate.split()[3])
        Age_of_certificate = endingYear - startingYear

        # checking final conditions
        if ((usehttps == 1) and (certificate_Auth in trusted_Auth) and (Age_of_certificate >= 1)):
            return -1  # legitimate
        elif ((usehttps == 1) and (certificate_Auth not in trusted_Auth)):
            return 0  # suspicious
        else:
            return 1  # phishing

    except Exception as e:

        return 1


def domain_registration(URL):
    if not URL :
        return 1
    try:
        with urlopen(URL) as f:
            s = dict(f.getheaders())['Set-Cookie'].split(";")
            expire = ""
            for i in s:
                if "Expires" in i:
                    expire = i.split("=")[-1][5:16]

            expiration_date = datetime.strptime(expire, '%d-%b-%Y').date()

            today = datetime.today().date()
            end = abs((expiration_date - today).days)
            if ((end / 30) < 36):
                end = 0
            else:
                end = 1
            return end

    except:
        print("Domain Registration Error")
        return 1

"""
def domain_registration(url):
    try:
        w = whois.whois(url)
        updated = w.updated_date
        exp = w.expiration_date
        length = (exp[0] - updated[0]).days
        if (length <= 365):
            return 1
        else:
            return -1
    except:
        return 0"""


def favicon(url):
    # ongoing
    return 0


def port(url):
    # ongoing
    return 0


def https_token(url):
    subDomain, domain, suffix = extract(url)
    host = subDomain + '.' + domain + '.' + suffix
    if (host.count('https')):  # attacker can trick by putting https in domain part
        return 1
    else:
        return -1


def request_url(url):
    try:
        subDomain, domain, suffix = extract(url)
        websiteDomain = domain

        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        imgs = soup.findAll('img', src=True)
        total = len(imgs)

        linked_to_same = 0
        avg = 0
        for image in imgs:
            subDomain, domain, suffix = extract(image['src'])
            imageDomain = domain
            if (websiteDomain == imageDomain or imageDomain == ''):
                linked_to_same = linked_to_same + 1
        vids = soup.findAll('video', src=True)
        total = total + len(vids)

        for video in vids:
            subDomain, domain, suffix = extract(video['src'])
            vidDomain = domain
            if (websiteDomain == vidDomain or vidDomain == ''):
                linked_to_same = linked_to_same + 1
        linked_outside = total - linked_to_same
        if (total != 0):
            avg = linked_outside / total

        if (avg < 0.22):
            return -1
        elif (0.22 <= avg <= 0.61):
            return 0
        else:
            return 1
    except:
        return 0


def url_of_anchor(url):
    try:
        subDomain, domain, suffix = extract(url)
        websiteDomain = domain

        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        anchors = soup.findAll('a', href=True)
        total = len(anchors)
        linked_to_same = 0
        avg = 0
        for anchor in anchors:
            subDomain, domain, suffix = extract(anchor['href'])
            anchorDomain = domain
            if (websiteDomain == anchorDomain or anchorDomain == ''):
                linked_to_same = linked_to_same + 1
        linked_outside = total - linked_to_same
        if (total != 0):
            avg = linked_outside / total

        if (avg < 0.31):
            return -1
        elif (0.31 <= avg <= 0.67):
            return 0
        else:
            return 1
    except:
        return 0


def Links_in_tags(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')

        no_of_meta = 0
        no_of_link = 0
        no_of_script = 0
        anchors = 0
        avg = 0
        for meta in soup.find_all('meta'):
            no_of_meta = no_of_meta + 1
        for link in soup.find_all('link'):
            no_of_link = no_of_link + 1
        for script in soup.find_all('script'):
            no_of_script = no_of_script + 1
        for anchor in soup.find_all('a'):
            anchors = anchors + 1
        total = no_of_meta + no_of_link + no_of_script + anchors
        tags = no_of_meta + no_of_link + no_of_script
        if (total != 0):
            avg = tags / total

        if (avg < 0.25):
            return -1
        elif (0.25 <= avg <= 0.81):
            return 0
        else:
            return 1
    except:
        return 0


def sfh(url):
    # ongoing
    return 0


def email_submit(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        if (soup.find('mailto:')):
            return 1
        else:
            return -1
    except:
        return 0


def abnormal_url(url):
    # ongoing
    return 0


def redirect(url):
    # ongoing
    return 0


def on_mouseover(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0

def rightClick(url):
    try:
        response = requests.get(url)
    except:
        response = ""

    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1

def popup(url):
    try:
        response = requests.get(url)
    except:
        response = ""

    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1


def iframe(url):
    # ongoing
    return 0



def age_of_domain(URL):
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


"""def age_of_domain(url):
    try:
        w = whois.whois(url)
        start_date = w.creation_date
        current_date = datetime.datetime.now()
        age = (current_date - start_date[0]).days
        if (age >= 180):
            return -1
        else:
            return 1
    except Exception as e:
        print(e)
        return 0"""


def dns(url):
    # ongoing
    return 0


def web_traffic(url):
    # ongoing
    return 0


def page_rank(url):
    # ongoing
    return 0


def google_index(url):
    # ongoing
    return 0


def links_pointing(url):
    # ongoing
    return 0


def statistical(url):
    # ongoing
    return 0


def main(url):
    check = [[url_having_ip(url), url_length(url), url_short(url), having_at_symbol(url),
              doubleSlash(url), prefix_suffix(url), sub_domain(url), SSLfinal_State(url),
              domain_registration(url), favicon(url), port(url), https_token(url), request_url(url),
              url_of_anchor(url), Links_in_tags(url), sfh(url), email_submit(url), abnormal_url(url),
              redirect(url), on_mouseover(url), rightClick(url), popup(url), iframe(url),
              age_of_domain(url), dns(url), web_traffic(url), page_rank(url), google_index(url),
              links_pointing(url), statistical(url)]]

    print(check)
    return check

