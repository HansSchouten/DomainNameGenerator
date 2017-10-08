import pythonwhois
import json
from pprint import pprint
from numpy.random import choice

syllable_count = 2

def main():
    with open('syllable_stats.json') as file:
        stats = json.load(file)
    
    while True:
        domain, score = generate_domain(stats)
        if is_available(domain):
            print("> " + domain + ".com [available] " + str(round(score, 5)))
        else:
            print(domain + ".com [taken] " + str(round(score, 5)))


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


if __name__ == "__main__":
    main()