
class Plugin():

    def process(self, URL):
        # The best way to check if a URL is punycode is to see if it can be encoded
        # https://stackoverflow.com/questions/37209239/how-to-check-if-a-domain-is-punycode-or-not

        URL = URL.replace("www.", "")
        URL = URL.replace("http://", '')
        URL = URL.replace("https://", '')

        try:
            encode = URL.encode('utf-8')
            decode = encode.decode('idna')
        except:
            return "Punycode not detected"

        if URL == decode:
            return "Punycode not detected"
        else:
            return "The URL translates to " + decode

            # Test Case: 'http://xn--addas-o4a.de/'  [adidas.de]
