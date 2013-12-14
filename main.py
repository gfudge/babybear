#!/usr/bin/python

import urllib2
import transmissionrpc
import sys, re, subprocess, time
from bs4 import BeautifulSoup
from urlparse import urljoin

spotifile = "spotifile.txt"


#trackID = "spotify:track:5aZCwTIsfqv22p5bewcrgf"

def trackLookup(trackID):
	baseUrl = "http://ws.spotify.com/lookup/1/?uri="
	try:
		url = baseUrl + trackID
		openpage = urllib2.urlopen(url)
		soup = BeautifulSoup(openpage.read( ))
		return soup;
	except: 
		print "Could not open page"	
		return -1;
	

def parseXML(soup):
	try:
		trackDetails = []
		trackDetails.append(soup.track.artist.nameTag.string)
		trackDetails.append(soup.track.nameTag.string)
		trackDetails.append(soup.track.album.nameTag.string)
		return trackDetails; 
	except:
		print "Error parsing file"
		return -1;

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


def pirateSearch(trackDetails):
	searchString = trackDetails[0] + "%20" + trackDetails[2]
	searchString = searchString.replace(" ", "%20")
	### PROXY URL -> LIKELY TO CHANGE ###	
	baseLink = "http://www.proxybay.eu/search/" + searchString + "/0/7/0"
	### 0/7/0 indicates highest seed first
	print "Trying: " + baseLink
	try:
		searchResult = urllib2.urlopen(baseLink).read()
	except urllib2.HTTPError, err:
		if err.code == 522:
			print "Connection timeout, waiting 10 seconds..."
			time.sleep(10)
			
		else:	
			print "Could not open TBP page"
			raise
	try:	
		results = re.findall(r'<div class="detName">.*?<\/tr>', searchResult, re.DOTALL)
	except:
		print "RegEx on page results failed"
		raise
	success = False
	#print result
	if (len(results) == 0):
		print "No links found for " + trackDetails[0]
	else:
		print "Got " + str(len(results)) + " results\n"
		### WHILE? ###
		while (success == False):
			for result in results:
				#if (success == True): return
				resultLink = re.search(r'<a href=\".*>(.*?)</a>.*<a href=\"magnet:(.*?)\".*\"detDesc\">(.*?),(.*?),(.*?)<.*<td align=\"right\">([0-9]+)<.*<td align=\"right\">([0-9]+)', result, re.DOTALL)
				magnetLink = "magnet:" + resultLink.group(2)
				#print magnetLink
				### Try to add magnet link to transmission-daemon
				try:
					tc.add_torrent(magnetLink)
					success = True
					return
				except transmissionrpc.TransmissionError, err:
					print err
					success = True
					#raise
				else:
					print "Failed to add magnet"
					success = True
					raise
				#subprocess.call(["transmission-remote", "-a", magnetLink])
		return;
	
	

#print trackLookup(trackID)
tc = transmissionrpc.Client('localhost', port=9091)
trackList = readList(spotifile)
print "Number of tracks: " + str(len(trackList))

for track in trackList:
	#trackLookup(track)
	trackDetails = parseXML(trackLookup(track))
	printTrack(trackDetails)
	pirateSearch(trackDetails)


