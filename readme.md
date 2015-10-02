# Twitter Media Bot

This is a Twitter bot which looks for metions - once someone tweets a mention, it will record a video (or take a picture), upload to Twitter and tweet it back to them as a reply.

Built for a project at work, where people can stand in front of the iconic Brighton graffiti and get a picture or video of them.

It uses the Twitter streaming API to get the tweets in real time.

## Hardware

This runs on a Raspberry Pi with a standard Camera Module. As it only uses Python to run, it could be run on any compatible platform. The camera code is obviously for the Raspberry Pi, so would need to be tweaked for your needs.

## Status

If you run into any problems (or suggestions) then please add a [Github Issue](https://github.com/liquidlight/graffcam/issues)

## Installation

The installation of this is a bit patchy as it's done from memory. However, it should be (fairly) self explanitory.

#### Step 1: Download the code to your RPi

Download the code and put it in somewhere like `/home/pi/tweetcam`

#### Step 2: Set up config file

Rename `_config.cfg.skel` to `_config.cfg` and update the values.

- `setup`
	- `debug_mode` - This stops the script from actually tweeting but output on the command line
	- `twitter_username` - The username of your twitter bot
- `twitter_api` - Your keys for the API app
- `tweets:last_mention_id` - This just needs to stay on 0, the script uses this to keep track of what tweets have been replied to
- `tweet_text` - a list of dictionaries containing phrases that your bot can reply, if make sure they contain `[[user]]` to include the username
	- `photo` - for when the bot takes a picture e.g. `["Looking good [[user]]!", "Very nice shoes [[user]]!"]`
	- `video` - for status with video e.g. `["Here is your #graffcam short [[user]]", "Enjoy your film [[user]]"]`
	- `preperation` - the tweet which is sent before recording starts e.g. `["[[user]] - get ready, filming will begin in 5 seconds!", "[[user]] I hope you're ready to be filmed in 5 seconds"]`

#### Step 3: Run the bot

Run the `bot.py` script manually to make sure everything is OK.

```
python bot.py
```

It will go through any mentions the bot has and reply to them with a video (hopefully)

#### Step 4: Set up the daemon

Modify line 14 of `StreamingDaemon` to the correct path of your script. Copy it to `/etc/init.d` with a slightly more sensible name.

```
sudo cp StreamingDeamon /etc/init.d/StreamingTweets
```

Ensure the script is executable

```
sudo chmod +x /etc/init.d/StreamingTweets
```

And initalise it as a service

```
sudo insserv /etc/init.d/StreamingTweets
```
