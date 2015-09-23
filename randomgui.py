import sys
import threading
import random
import queue
import hashlib

from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

import PySide.QtGui as pysidegui
import PySide.QtCore as pysidecore
import PySide.QtWebKit as pysideweb

class generateLinkThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		global imgQ
		imgQ = queue.Queue(50)
		self.imgQ = imgQ
		global imgSeen
		imgSeen = []
		self.imgSeen = imgSeen
		self.chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
		self.url = "http://i.imgur.com/"
		self.ext = ['.png']
		self.size = 1024 * 20
		
		self.stopping = False
		self.start()
		while self.imgQ.qsize() < 10:
			pass

	def run(self):
		while not self.stopping:
			while not self.imgQ.full():
				print("Reloading! ---> ",self.imgQ.qsize())
				link = self.generateLink()
				print(link)
				for end in self.ext:
					fullLink = link + end
					if self.verifyUrl(fullLink):
						print(fullLink)
						if not fullLink in self.imgSeen:
							self.imgQ.put(pysidecore.QUrl(fullLink))
				if self.stopping:
					break

	def stop(self):
		self.stopping = True

	def generateLink(self):
		elements = []
		rand = random.choice("57")
		for i in range(0,int(rand)):
			elements.append(random.choice(self.chars))
		s = ""
		s = s.join(elements)
		link = self.url + s
		return link

	def verifyUrl(self,url):
		req = Request(url)
		data = None
		try:
			data = urlopen(req)
		except HTTPError as e:
			print("HTTP Error: "+str(e.code)+' '+url)
		except URLError as e:
			print("URL Error: "+str(e.reason)+' '+url)

		if data:
			try:
				data = data.read();

				# Check if placeholder image.
				if 'd835884373f4d6c8f24742ceabe74946' == hashlib.md5(data).hexdigest():
					print("Received placeholder image: "+url)
				# Check if image is above minimum size.
				elif self.size > sys.getsizeof(data):
					print("Received image is below minimum size threshold: "+url)
				else:
					return True
			except Exception as e:
				print(str(e))
				return False

class mainWin(pysidegui.QMainWindow):

	def __init__(self,parent=None):
		pysidegui.QMainWindow.__init__(self,parent)
		global imgQ
		self.imgQ = imgQ
		global imgSeen
		self.imgSeen = imgSeen
		self.setup()

	def setup(self):
		self.currUrl = self.imgQ.get()

		self.imgurViewer = pysideweb.QWebView()
		self.imgurViewer.load(self.currUrl)

		nextButton = pysidegui.QPushButton("Next!")
		nextButton.clicked.connect(self.loadNextUrl)

		centralWidgetLayout = pysidegui.QVBoxLayout()
		centralWidgetLayout.addWidget(self.imgurViewer)
		centralWidgetLayout.addWidget(nextButton)

		centralWidget = pysidegui.QWidget()
		centralWidget.setLayout(centralWidgetLayout)
		
		self.setCentralWidget(centralWidget)

		self.show()

	def loadNextUrl(self):
		self.imgSeen.append(self.currUrl.toString())
		self.currUrl = self.imgQ.get()

		self.imgurViewer.load(self.currUrl)

if __name__ == '__main__':
	genLinksThr = generateLinkThread()

	QA = pysidegui.QApplication([])
	mainWindow = mainWin()

	QA.exec_()
	genLinksThr.stop()

	sys.exit()