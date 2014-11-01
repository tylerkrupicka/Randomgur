import hashlib
import random
import sys
import webbrowser
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

class Randomgur:

    def __init__(self):
        self.chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.url = "http://i.imgur.com/"
        self.ext = ['.jpg','.jpeg','.png']
        self.size = 1024 * 20
        self.count = 0

    def generateLink(self):
        elements = []
        rand = random.choice("57")
        for i in range(0,int(rand)):
            elements.append(random.choice(self.chars))
        s = ""
        s = s.join(elements)
        link = self.url + s
        return link
        
    def testPage(self,url):
        req = Request(url)
        data = None

        try:
            data = urlopen(req)
        except HTTPError as e:
            error_print("HTTP Error: "+str(e.code)+' '+image_name)
        except URLError as e:
            error_print("URL Error: "+str(e.reason)+' '+image_name)

        if data:
            try:
                data = data.read();

                # Check if placeholder image.
                if 'd835884373f4d6c8f24742ceabe74946' == hashlib.md5(data).hexdigest():
                    error_print("Received placeholder image: "+image_name)
                # Check if image is above minimum size.
                elif self.size > sys.getsizeof(data):
                    error_print("Received image is below minimum size threshold: "+image_name)
                else:
                    return True
            except:
                return False
                        
    def saveImage(self):
        pass
    def main(self):
        while True:
            link = self.generateLink()
            for end in self.ext:
                if(self.testPage(link + end)):
                    print(link+end)
                    self.count += 1
                    wait = input("Next ->")
                    webbrowser.open(link+end)
                    break
                    
            
if __name__ == '__main__':
    Randomgur().main()

    
