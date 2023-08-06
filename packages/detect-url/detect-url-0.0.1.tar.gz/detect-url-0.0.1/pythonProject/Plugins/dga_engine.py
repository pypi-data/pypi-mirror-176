import tldextract
import math
import re
import pickle
import sys

sys.path.insert(1, "../gib")
from gib import gib_detect_train
#import gib_detect_train

class Plugin:

    def entropy(string):
        # Calculates the Shannon entropy of a string get probability of chars in string
        prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]

        # Calculate the entropy
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy

    def count_consonants(string):
        # Counting consonants in a string
        consonants = re.compile('[bcdfghjklmnpqrstvwxyz]')
        count = consonants.findall(string)
        return len(count)

    def domain_check(domain):
        # skip tor domains
        if domain.endswith(".onion"):
            # Tor domains is ignored
            return "No"

        # only interested in main domain name without subdomain and tld
        domain_without_sub = tldextract.extract(domain).domain

        # skip localized domains
        if domain_without_sub.startswith("xn-"):
            # Localized domains is ignored
            return "No"

        # skip short domains
        if len(domain_without_sub) < 6:
            # Short domains is ignored
            return "No"

        domain_entropy = Plugin.entropy(domain_without_sub)
        domain_consonants = Plugin.count_consonants(domain_without_sub)
        domain_length = len(domain_without_sub)

        return domain_without_sub, domain_entropy, domain_consonants, domain_length

    def process(self, domain):
        if (len(domain)) < 6:
            return "DGA Link needs to be a minimun length of 6!"

        model_data = pickle.load(open('gib/gib_model.pki', 'rb'))
        model_mat = model_data['mat']
        threshold = model_data['thresh']

        try:
            if Plugin.domain_check(domain):
                domain_without_sub, domain_entropy, domain_consonants, domain_length = domain_check(domain)

                if domain_entropy > 3.8:
                    result = "High entropy indicated. " \
                             "This domain scored: " + str(domain_entropy) + " (Threshold is 3.8)"
                    return result
                if domain_consonants > 7:
                    result = "High consonants indicated. " \
                             "This domain scored: " + str(domain_consonants) + " (Threshold is 7)"
                    return result
                if domain_length > 12:
                    result = "Long domain name indicated. " \
                             "This domain scored: " + str(domain_length) + " (Threshold is 12)"
                    return result
                if not gib_detect_train.avg_transition_prob(domain_without_sub, model_mat) > threshold:
                    return ["Domain " + str(domain) + " is DGA!"]
                else:
                    result = "Domain " + str(domain) + " is not DGA! Entropy: " + str(domain_entropy) + " (Threshold is 3.8). " \
                              "Consonants count: " + str(domain_consonants) + " (Threshold is 7). Name length: " + \
                               str(domain_length) + " (Threshold is 12)"
                    return result
        except:
            return "DGA not detected"

        # Credit: {https://github.com/exp0se/dga_detector}
        # Test Cases: { OLKQXMAEUIWYX.XXX, BPWENCSDVRJXJI.PRO }0
