import os
import urllib2
import smtplib
from difflib import SequenceMatcher

#SMTP Configuration
smtpSender = """Sender Email Account""" 
receivers = ['FirstEmail', 'Second Email']
smtpHost = """SMTP Host Name"""
smtpPort = 587
smtpPassword = 'Sender Email Password'
smtpSubject = 'Simple-URLWatch has detected a change!'


#URLs to monitor
URLS = {
    '1':'http://espn.com', 
    '2':'http://www.reddit.com/new/',
    '3':'http://www.google.com'
}



THRESHOLD = 1.0  # on a scale of 0 to 1

BASEDIR = os.getcwd()
HTML_PATH = 'html'
notifySender = False

def main():
    # create html dir if it does not exist
    if not os.path.exists(os.path.join(BASEDIR, HTML_PATH)):
        try:
            os.makedirs(os.path.join(BASEDIR, HTML_PATH))
        except Exception as e:
            print("Unable to create html directory at {1}".format(os.path.join(BASEDIR, HTML_PATH)))
            print e

    MESSAGE = 'Subject: %s\n\nThe following URLS have changed \n' %(smtpSubject)

    for urlID, url in URLS.items():
        LAST_HTML = urlID + '.html'
        LAST_HTML_PATH = os.path.join(BASEDIR, HTML_PATH, LAST_HTML)
        
        html = get_html(url)
        if os.path.exists(LAST_HTML_PATH):
            last_html = open(LAST_HTML_PATH, 'r').read()
            score = get_score(html, last_html)

            if score < THRESHOLD:
                MESSAGE += url +'\n'
                notifySender = True
                #print MESSAGE

            write_html(html, LAST_HTML_PATH)
        else:
            write_html(html, LAST_HTML_PATH)

    if notifySender == True:
        notify(MESSAGE)


def notify(MESSAGE):
    print MESSAGE
    try:
        smtpObj = smtplib.SMTP(smtpHost, smtpPort)
        smtpObj.login(smtpSender, smtpPassword)
        smtpObj.sendmail(smtpSender, receivers, MESSAGE)         
        print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"

def get_score(html, last_html):
    sm = SequenceMatcher(None, html, last_html)
    score = sm.ratio()
    return score


def get_score(html, last_html):
    sm = SequenceMatcher(None, html, last_html)
    score = sm.ratio()
    return score


def get_html(url):
    try:
        response = urllib2.urlopen(url)
    except Exception as e:
        print 'Unable to open URL: ' + url
        print e
        exit(1)
    html = response.read()
    return html

def write_html(html, LAST_HTML_PATH):
    with open(LAST_HTML_PATH, 'wb') as f:
        f.write(html)

if __name__ == '__main__':
    main()