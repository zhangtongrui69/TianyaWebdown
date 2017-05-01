from html.parser import HTMLParser
import codecs
from bs4 import BeautifulSoup

class MyHTMLParser(HTMLParser):
    divtag=0
    level=0
    def handle_starttag(self, tag, attrs):
        if tag=='div':
            if len(attrs)>=1:
                if attrs[0]==('class', 'atl-item') or attrs[0]==('class', 'atl-item host-item'):
#                    print("Encountered a bbs content:", tag)
                    self.divtag = 1

    def handle_endtag(self, tag):
        if tag=='div':
            self.level -= 1
        if self.divtag == 1:
#            print("Encountered an end tag :", tag)
            if self.divtag==1:
                self.divtag=0

    def handle_data(self, data):
        if self.divtag==1:
            print(" bbs content:", data)

    def handle_startendtag(self, tag, attrs):
        pass
 #       print("Encountered a start-end tag", tag)

fobj= codecs.open('tianya\\post-free-3077648-1.shtml', 'r', encoding='utf-8')
s1=fobj.read()
fobj.close()

#print(s1)
#parser = MyHTMLParser()
#parser.feed(s1)

soup = BeautifulSoup(s1, 'lxml')
a = soup('div')
for a1 in a:
    try:
        if a1['class'] == ['atl-item']:
            print(a1.contents)
        else:
            print(a1['class'])
    except Exception as ex:
        print('An exception ({0}) occurred.'.format(type(ex).__name__))
