import pythonwhois
import json
import operator
from pprint import pprint
from numpy.random import choice

verbose = True
syllable_count = 3

def main():
    with open('syllable_stats.json') as file:
        stats = json.load(file)
    
    domains = {}
    while True:
        domain, score = generate_domain(stats)
        if not is_available(domain):
            log(domain + ".com [taken] " + str(round(score, 5)))
            continue
        
        log("> " + domain + ".com [available] " + str(round(score, 5)))
        domains[domain] = score
        
        # store available domains every tenth iteration
        if len(domains) % 10 == 0:
            sorted_domains = sorted(domains.items(), key=operator.itemgetter(1), reverse=True)
            with open('available_domains.txt', 'w') as file:
                file.write('\n'.join('%s.com %s' % domain for domain in sorted_domains))


def generate_domain(stats):
    """ Create a new random domain, based on the given language statistics. """
    syllables = list(stats['syllables'].keys())
    weights = list(stats['syllables'].values())
    syllable = choice(syllables, p=normalize(weights))
    domain = syllable
    score = stats['syllables'][syllable] / sum(weights)

    for i in range(1, syllable_count):
        last_char = syllable[-1]
        next_chars = list(stats['combinations'][last_char].keys())
        weights = list(stats['combinations'][last_char].values())
        next_char = choice(next_chars, p=normalize(weights))

        syllables = list(stats['by_char'][next_char].keys())
        occurrences = []
        for syllable in syllables:
            occurrences.append(stats['syllables'][syllable])

        syllable = choice(syllables, p=normalize(occurrences))
        domain += syllable
        score += (stats['syllables'][syllable] / sum(occurrences))
            
    return (domain, score / float(syllable_count))


def normalize(values):
    """ Let the sum of all values be one. """
    return [float(i)/sum(values) for i in values]


def is_available(domain):
    """ Return whether the given domain is available. """
    return ('id' not in pythonwhois.get_whois(domain + '.com'))


def log(message):
    """ Print status messages to console if desired. """
    if (verbose):
        print(message)


if __name__ == "__main__":
    main()