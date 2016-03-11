#!/usr/bin/env python

# SETUP: Import global modules
import TweetStreetCam

g = TweetStreetCam.RaspPiTweetCam()
mentions = g.GetMentions()

if mentions:
	for tweet in mentions:
		g.ActionTweet(tweet)

for tweet in g.GetStream():
	if 'text' in tweet:
		g.ActionTweet(tweet)
