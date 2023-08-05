# uas

## Description
This fake user agent generator does not use any external data. Instead it
randomizes browser versions for Firefox, Chrome and OS versions for MacOS,
Windows. `uas` also contains some static user agents for bots from Facebook,
Google and Bing.

## Installation

`pip install uas`

## Usage

```
import requests
from uas import chrome, firefox, bot, GOOGLE


r = requests.get("https://example.com/chrome", headers={"User-Agent": chrome()})
r = requests.get("https://example.com/firefox", headers={"User-Agent": firefox()})
r = requests.get("https://example.com/bot", headers={"User-Agent": bot()})
r = requests.get("https://example.com/google", headers={"User-Agent": GOOGLE[0]})
```
