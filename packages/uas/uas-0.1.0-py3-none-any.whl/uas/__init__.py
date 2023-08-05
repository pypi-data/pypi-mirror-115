from random import choice, randint


# https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0
BING = (
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/W.X.Y.Z Safari/537.36 Edg/W.X.Y.Z",
)
# https://developers.facebook.com/docs/sharing/webmasters/crawler
FACEBOOK = (
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "facebookexternalhit/1.1",
)
# https://developers.google.com/search/docs/advanced/crawling/overview-google-crawlers
GOOGLE = (
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36",
)
BOTS = BING + FACEBOOK + GOOGLE


def _os(macos) -> str:
    return choice((f"Macintosh; Intel Mac OS X {macos}", "Windows NT 10.0; Win64; x64"))


# https://en.wikipedia.org/wiki/Google_Chrome_version_history
def chrome() -> str:
    version = choice(
        (
            "86.0.4240",
            "87.0.4280",
            "88.0.4324",
            "89.0.4389",
            "90.0.4430",
            "91.0.4472",
            "92.0.4515"
        )
    )  # use last 7 stable
    sub = randint(7, 212)
    macos = f"10_{randint(13, 15)}_{randint(0, 6)}"
    return f"Mozilla/5.0 ({_os(macos)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.{sub} Safari/537.36"


# https://www.mozilla.org/en-US/firefox/releases/
def firefox():
    version = f"{randint(84, 90)}.{choice(['0', '0.1', '0.2', '0.3'])}"  # use last 7 major
    macos = f"10.{randint(13, 15)}"
    return f"Mozilla/5.0 ({_os(macos)}; rv:{version}) Gecko/20100101 Firefox/{version}"


def bot():
    return choice(BOTS)
