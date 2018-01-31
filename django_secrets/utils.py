def _wrap_with(code):
    def inner(text, bold=False):
        return "\033[%sm%s\033[0m" % (code, text)
    return inner


red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')
