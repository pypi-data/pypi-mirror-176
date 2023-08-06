import os
import pathlib as pl
import sys

from dotenv import load_dotenv
import tweepy

load_dotenv()

USER_ID = os.getenv("TWITTER_USER_ID")
        
auth = tweepy.OAuthHandler(
    os.getenv('TWITTER_CONSUMER_KEY'),
    os.getenv('TWITTER_CONSUMER_SECRET'),
)
auth.set_access_token(
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
)
api = tweepy.API(auth)


class IdenticalProfile(Exception):
    ...


class AttachmentDoesntExist(Exception):
    ...



def send_tweet(tweet: str, attachment_path: pl.Path | None = None) -> int:
    if attachment_path is None:
        return api.update_status(status=tweet).id
    if not attachment_path.exists():
        raise AttachmentDoesntExist
    return api.update_status_with_media(status=tweet, filename=str(attachment_path)).id # type: ignore


def cli_send_tweet():
    if len(sys.argv) < 2:
        print("please provide a tweet")
        sys.exit()

    text = sys.argv[1]
    if not text.strip():
        print("tweet can't be blank!")
        sys.exit()

    fp = None
    if len(sys.argv) == 3:
        arg3 = sys.argv[2]
        if not arg3.startswith("--attach="):
            print("the only additional argument supported is '--attach=...'")
            sys.exit()
        fp = pl.Path(sys.argv[2].split("--attach=")[1].strip())
    id_ = send_tweet(text, fp)
    if fp is None:
        print(f"Okay, published the tweet at https://twitter.com/{USER_ID}/status/{id_}")
    else:
        print(f"Okay, published the tweet with attachment at https://twitter.com/{USER_ID}/status/{id_}")


def update_profile_description(description: str):
    if get_current_profile_description() == description:
        return api.update_profile(description=description)


def cli_update_profile():
    if len(sys.argv) != 2:
        print("please provide a profile description")
        sys.exit()
    try:
        update_profile_description(sys.argv[1])
    except IdenticalProfile:
        print("that's your description already!")
        sys.exit()
    print("Okay, updated profile.")


def get_current_profile_description() -> str:
    return api.get_user(screen_name=USER_ID).description


def cli_show_profile() -> None:
    print(f"current profile: '{get_current_profile_description()}'")
    sys.exit()


def get_last_tweet():
    return api.user_timeline(user_id=USER_ID)[0]


def delete_last_tweet() -> str:
    last_tweet = get_last_tweet()
    api.destroy_status(last_tweet.id)
    return last_tweet.text


def cli_delete_last_tweet() -> None:
    text = delete_last_tweet()
    print(f"deleted this tweet: '{text}'")
    sys.exit()
