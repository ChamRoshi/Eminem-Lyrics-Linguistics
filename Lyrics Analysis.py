from tswift import Artist, Song
import pprint
from nltk.corpus import cmudict
import nltk
import string
import pandas as pd
import csv
import os

d = cmudict.dict()

def nsyl(word): 
	return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 


def clean_lyrics(lyrics):
	lyrics1 = lyrics.split("\n\nmeaning\n\n")[0]
	lyrics2 = lyrics.split("\n\nSee all\n\n")[1]
	lyrics = lyrics1 + lyrics2
	return lyrics
def freqqdist(word_lst):
	dist = {}
	for item in word_lst: 
		if item in dist: 
			dist[item] += 1
		else: 
			dist[item] = 1
	return dist

def analysis(lyrics, name):
	word_lst = []
	lyrics = lyrics.translate(None, string.punctuation)

	tokens = nltk.word_tokenize(lyrics)
	for word in tokens:
		if word != "":
			try:
				word_lst.append(nsyl(word)[0])
			except Exception, e: 
				pass #... gotta make it pretty, it's only easter ;)
				# print e
	dist = freqqdist(word_lst)
	dist = pad_dist(dist)
	# print dist
	try:
		sylables = float(sum(word_lst))/float(len(word_lst))
	except: 
		sylables = 0
	temp = {"name": name, "words": len(tokens), "lines": len(lyrics.split("\n")), "sylables": sylables, "dist": dist}
	# print temp
	return temp


def analysis_rapper(title, artist):

	s = Song(artist = artist, title = title)
	lyrics = s.lyrics.encode("utf-8")


	try:
		lyrics = clean_lyrics(lyrics)
	except:
		lyrics = lyrics

	return analysis(lyrics, title)

		

def pad_dist(dist):
	for num in range(11):
		if num in dist:
			pass
		else: 
			dist[num] = 0
	return dist

def init_csv(csv_address):
	row = ["artist", "name", "words", "lines", "sylables"]
	for item in range(10):
		row.append(item)
	with open(csv_address, "wb") as csv_f:
		writer = csv.writer(csv_f)
		writer.writerow(row)

# df = pd.DataFrame(columns = ("artist", "song name", "word len", "Lines len", 
# analysis_rapper("rap god", "eminem")
# analysis_rapper("bad blood", "Taylor Swift")
csv_address = "eminem_analysis.csv"
csv_address = os.path.join(os.getcwd(), csv_address)
artist = "eminem"
tswift = Artist(artist)

init_csv(csv_address)


# for item in tswift.songs: 
# 	print item
# 	s = Song(title = item.title, artist = item.artist)
# 	print s.lyrics

for num, item in enumerate(tswift.songs): 
	# print item.title
	print num, item.title
	analysiss = analysis_rapper(item.title, item.artist)
	row = [artist, analysiss["name"], analysiss["words"], analysiss["lines"],
	 analysiss["sylables"]]

	for item in range(10):
		row.append(analysiss["dist"][item])
	with open(csv_address, "ab") as csv_f:
		writer = csv.writer(csv_f)
		writer.writerow(row)
		# writer.save()
		print "written"
	# break




