# twi

Send tweets, change your Twitter profile description, and delete your last tweet, all from the comfort of your sweet-smelling CLI!

# Installation
```bash
> pip install twi
```
Then put these variables somewhere in your environment (get them [here](https://developer.twitter.com/en/portal/dashboard)):

- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_TOKEN_SECRET
- TWITTER_USER_ID

# Usage
```bash
> tw "hey this is my tweet"
Okay, published the tweet at https://twitter.com/yourname/status/12344556
> twd
Okay, deleted this tweet: 'hey this is my tweet'
> tw "hey this is my tweet with a screenshot" --attach=/home/me/screencap.png
Okay, published the tweet with atachment at https://twitter.com/yourname/status/12344557
> twpu "hey this is my new twitter profile description"
Okay, updated profile.
> twp
current profile: 'hey this is my current profile description'
```
