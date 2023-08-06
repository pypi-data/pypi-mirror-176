from pathlib import Path
from distutils.core import setup

setup(
    name="twi",
    author="Zev Averbach",
    author_email="zev@averba.ch",
    version="0.0.5",
    description="do Twitter things via CLI",
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="http://code.averba.ch/Zev/twi",
    install_requires=[
        "tweepy",
    ],
    packages=[
        "twi",
    ],
    entry_points="""
        [console_scripts]
        tw=twi.app:cli_send_tweet
        twp=twi.app:cli_show_profile
        twpu=twi.app:cli_update_profile
        twd=twi.app:cli_delete_last_tweet
    """,
)
