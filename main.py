#!/usr/bin/python

import urllib2
import sys
from bs4 import BeautifulSoup
from urlparse import urljoin

spotifile = "spotifile.txt"

baseUrl = "http://ws.spotify.com/lookup/1/?uri="
#trackID = "spotify:track:5aZCwTIsfqv22p5bewcrgf"

def trackLookup(trackID):
	try:
		url = baseUrl + trackID
		openpage = urllib2.urlopen(url)
		soup = BeautifulSoup(openpage.read( ))
		return soup;
	except: 
		print "Could not open page"	
		return 1;
	

def parseXML(soup):
	trackDetails = []
	trackDetails.append(soup.track.artist.nameTag.string)
	trackDetails.append(soup.track.nameTag.string)
	trackDetails.append(soup.track.album.nameTag.string)
	return trackDetails; 

def readList(spotifile):
	return [line.strip() for line in open(spotifile)];

def printTrack(trackDetails):
	print "Artist: " + trackDetails[0]
	print "Track: " + trackDetails[1]
	print "Album: " + trackDetails[2] + "\n"

def YTSearch(trackDetails):
	YTBASEURL = "https://www.youtube.com/results?search_query="
	searchResult = YTBASEURL + trackDetails[0] + "+" + trackDetails[1]
	resultPage = urllib2.urlopen(searchResult)
	print searchResult

#print trackLookup(trackID)
trackList = readList(spotifile)
print "Number of tracks: " + str(len(trackList))

for track in trackList:
	#trackLookup(track)
	trackDetails = parseXML(trackLookup(track))
	printTrack(trackDetails)
	#YTSearch(trackDetails)
