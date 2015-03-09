import os
import urllib2
from difflib import SequenceMatcher

URL = 'http://espn.com'
THRESHOLD = 1.0  # on a scale of 0 to 1
EMAIL = 'jcaine04@gmail.com'

BASEDIR = os.getcwd()
HTML_PATH = 'html'
LAST_HTML = 'last.html'
LAST_HTML_PATH = os.path.join(BASEDIR, HTML_PATH, LAST_HTML)


def main():
    html = get_html()
    if os.path.exists(LAST_HTML_PATH):
        last_html = open(LAST_HTML_PATH, 'r').read()
        score = get_score(html, last_html)

        if score < THRESHOLD:
            # notify
            notify(EMAIL, score)

        write_html(html)
    else:
        write_html(html)


def notify(email, score):
    print("Threshold of {0} has been surpassed. Current score: {1}. Emailing {2}!".format(THRESHOLD, score, email))


def get_score(html, last_html):
    sm = SequenceMatcher(None, html, last_html)
    score = sm.ratio()
    return score


def get_html():
    try:
        response = urllib2.urlopen(URL)
    except Exception as e:
        print 'Unable to open URL: ' + URL
        print e
        exit(1)
    html = response.read()
    return html

def write_html(html):
    with open(LAST_HTML_PATH, 'wb') as f:
        f.write(html)

if __name__ == '__main__':
    main()