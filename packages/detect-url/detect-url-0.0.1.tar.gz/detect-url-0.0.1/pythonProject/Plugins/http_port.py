
class Plugin():

    def process(self, URL):
        if "https://" in URL:
            return "HTTPS: Port 443"
        elif "http://" in URL:
            return "HTTP: Port 80"
        else:
            return "No port indicated"
