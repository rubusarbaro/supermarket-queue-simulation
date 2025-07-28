# Text styles in ANSI format.
class Text :
    end = "\033[0m"

class Regular(Text) :
    bold = "\033[1m"
    underline = "\033[4m"

    blue = "\033[0;34m"
    cyan = "\033[0;36m"
    green = "\033[0;32m"
    red = "\033[0;31m"
    yellow = "\033[0;33m"
    dark_gray = "\033[1;30m"

class Bold(Text) :
    blue = "\033[1;34m"
    cyan = "\033[1;36m"
    green = "\033[1;32m"
    red = "\033[1;31m"
    yellow = "\033[1;33m"
    dark_gray = "\033[1;30m"

class Underline(Text) :
    blue = "\033[4;34m"
    cyan = "\033[4;36m"
    green = "\033[4;32m"
    red = "\033[4;31m"
    yellow = "\033[4;33m"
    dark_gray = "\033[1;30m"

class Background(Text) :
    classic = "\033[0;30m\033[47m"