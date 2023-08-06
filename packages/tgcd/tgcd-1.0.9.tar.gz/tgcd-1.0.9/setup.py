import setuptools

setuptools.setup(
    name="tgcd",
    version="1.0.9",
    author="reaitten",
    author_email="wsy0xf2u8@relay.firefox.com",
    description="a private fork of slam-mirrorbot.",
    include_package_data=True,
    python_requires=">=3.8.2",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp',
        'aria2p',
        'appdirs',
        'beautifulsoup4',
        'cloudscrape',
        'feedparser',
        'gitpython',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'heroku3',
        'js2py',
        'lk21',
        'lxml',
        'psutil',
        'psycopg2-binary',
        'pybase64',
        'pyrogram',
        'python-dotenv',
        'python-magic',
        'python-telegram-bot',
        'requests',
        'speedtest-cli',
        'telegraph',
        'tenacity',
        'TgCrypto',
        'youtube_dl'],
    scripts=['extract'],
    entry_points={
        "console_scripts":[
            "tgcd = bot.__main__:main"
                ],
    },
)