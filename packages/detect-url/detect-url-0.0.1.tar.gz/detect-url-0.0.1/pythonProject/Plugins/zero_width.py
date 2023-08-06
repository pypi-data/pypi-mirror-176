
class Plugin():

    def process(self, URL):
        original = len(URL)
        zero_width = ""

        if original != len(URL.replace('\u200B', '')):
            zero_width += "U+200B ZERO WIDTH SPACE, "
        if original != len(URL.replace('\u200D', '')):
            zero_width += "U+200C ZERO WIDTH NON-JOINER, "
        if original != len(URL.replace('\uFEFF', '')):
            zero_width += "U+200D ZERO WIDTH JOINER, "
        if original != len(URL.replace('\u200C', '')):
            zero_width += "U+200E LEFT-TO-RIGHT MARK, "
        if original != len(URL.replace('\u200E', '')):
            zero_width += "U+202A LEFT-TO-RIGHT EMBEDDING, "
        if original != len(URL.replace('\u202A', '')):
            zero_width += "U+202C POP DIRECTIONAL FORMATTING, "
        if original != len(URL.replace('\u202C', '')):
            zero_width += "U+202D LEFT-TO-RIGHT OVERRIDE, "
        if original != len(URL.replace('\u202D', '')):
            zero_width += "U+2062 INVISIBLE TIMES, "
        if original != len(URL.replace('\u2062', '')):
            zero_width += "U+2063 INVISIBLE SEPARATOR, "
        if original != len(URL.replace('\u2063', '')):
            zero_width += "U+FEFF ZERO WIDTH NO-BREAK SPACE, "

        if len(zero_width) == 0:
            return "Zero-width is not detected"
        else:
            return zero_width[0:len(zero_width)-2]

        # Test Case: https://en.wikipedia.org/wiki/Zero-width_space
        # ZeroWidth‌Joiner‌.com‌
        # Lorem​IpsumZeroWidth‌Joiner‌.com‌
