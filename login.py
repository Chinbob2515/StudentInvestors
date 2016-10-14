import cookielib, urllib, urllib2
from bs4 import BeautifulSoup

class Login(object):

    def __init__(self, login, password):
        """ Start up... """
        self.loginS = login
        self.password = password

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

    def doLog(self):
        # need this twice - once to set cookies, once to log in...
        return [self.login() for _ in range(2)]

    def request(self, url):
	return BeautifulSoup(''.join(self.opener.open(url).readlines()), "html.parser")
    
    def login(self):
	return self.submit("https://www.studentinvestor.org/secure/login.php", {
            'team-name' : self.loginS,
            'team-password' : self.password,
            'loginsubmitted': 1,
        })
    
    def submit(self, url, dict={}):
	data = urllib.urlencode(dict)
	response = self.opener.open(url, data)
	return BeautifulSoup(''.join(response.readlines()), "html.parser")

