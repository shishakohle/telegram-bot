import urllib.request

# <div class="H4 Question-title u-big u-mbm ">Kann mir jemand helfen?</div>\n'
indicator_pre  = "<div class=\"H4 Question-title u-big u-mbm \">"
indicator_post = "</div>"


def latest_question() -> str:
    with urllib.request.urlopen("https://www.gutefrage.net/fragen/neue/1") as response:
        for line in response.readlines():
            candidate = line.decode('utf-8')
            if indicator_pre in candidate:
                question = candidate.partition(indicator_pre)[2].partition(indicator_post)[0]
                return question
