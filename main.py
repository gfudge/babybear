#!/usr/bin/python

import urllib2
import sys
from bs4 import BeautifulSoup
from urlparse import urljoin

spotifile = "spotifile.txt"

baseUrl = "http://ws.spotify.com/lookup/1/?uri="
trackID = "spotify:track:5aZCwTIsfqv22p5bewcrgf"

def trackLookup(trackID):
	try:
		url = baseUrl + trackID
		openpage=urllib2.urlopen(url)
		soup = BeautifulSoup(openpage.read( ))
		print soup.track.artist.name.string
		return soup;
	except: 
		print "Could not open page"	
		return 1;
	

def parseXML(soup):
	print soup.track.artist.nameTag

def readList(spotifile):
	return [line.strip() for line in open(spotifile)];

#print trackLookup(trackID)
trackList = readList(spotifile)
print "Number of tracks: " + str(len(trackList))

for track in trackList:
	trackLookup(track)
	#parseXML(track)
