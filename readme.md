# Twitter Media Bot

This is a Twitter bot which looks for metions - once someone tweets a mention, it will record a video (or take a picture), upload to Twitter and tweet it back to them as a reply.

Built for a project at work, where people can stand in front of the iconic Brighton graffiti and get a picture or video of them.

It uses the Twitter streaming API to get the tweets in real time.

## Hardware

This runs on a Raspberry Pi with a standard Camera Module. As it only uses Python to run, it could be run on any compatible platform. The camera code is obviously for the Raspberry Pi, so would need to be tweaked for your needs.

## Status

If you run into any problems (or suggestions) then please add a [Github Issue](https://github.com/liquidlight/tweetcam/issues)

## Installation

The installation of this is a bit patchy as it's done from memory. However, it should be (fairly) self explanitory.

#### Step 1: Download the code to your RPi

Download the code and put it in somewhere like `/home/pi/tweetcam`

#### Step 2: Set up config file

Rename `_config.cfg.skel` to `_config.cfg` and update the values.

- `setup`
	- `debug_mode` - This stops the script from actually tweeting but output on the command line
	- `twitter_username` - The username of your twitter bot (without the @)
- `options`
	- `tweet_difference_limit` - Time (in minutes) for the cutoff for replying to tweets (e.g. if it is over this it won't reply)
- `twitter_api` - Your keys for the API app
- `tweet_text` - a list of dictionaries containing phrases that your bot can reply, if make sure they contain `[[user]]` to include the username
	- `photo` - for when the bot takes a picture
	- `video` - for status with video
	- `preperation` - the tweet which is sent before recording starts
	- `late` - for when the tweet is more than tweet difference limit

#### Step 3: Run the bot

Run the `bot.py` script manually to make sure everything is OK.

```
python bot.py
```

It will go through any mentions the bot has and reply to them with a video (hopefully)

#### Step 4: Set up the daemon

Modify line 14 of `StreamingDaemon` to the correct path of your script. Copy it to `/etc/init.d` with a slightly more sensible name.

```
sudo cp tweets /etc/init.d/tweets
```

Ensure the script is executable

```
sudo chmod +x /etc/init.d/tweets
```

And initalise it as a service

```
sudo insserv /etc/init.d/tweets
```

Now you can run

```
sudo service tweets start
```

#### Step 5: Set up the cron

You can set up a cron job to run every 15 minutes or so to check the service is running. If it is, do nothing. If it's stopped for whateve reason, start it again.

Edit the crontab

```
sudo crontab -e
```

And add this to the bottom

```
*/15 * * * * sudo sudo /bin/sh /home/pi/tweet/servicecheck.sh
```

This will run the service check script every 15 minutes - restarting the process if it's not running
