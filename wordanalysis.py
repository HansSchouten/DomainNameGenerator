import json
from pprint import pprint
from pyphen import Pyphen

pyphen = Pyphen(lang='en')
vowels = list('aeiou')
syllable_formats = ['ccv', 'cvc', 'cv']

def main():
    stats = {
        'syllables': {},
        'combinations': {},
        'by_char': {}
    }
    
    with open('wordlists/words_EN.txt') as wordlist:
        for word in wordlist:
            analyse(stats, word.strip())
    
    with open('syllable_stats.json', 'w') as file:
        json.dump(stats, file)


def analyse(stats, word):
    """ Add statistics of the given word to stats. """
    parts = pyphen.inserted(word).split('-')
    
    allowed_parts = []
    for part in parts:
        for format in syllable_formats:
            if is_format(part, format):
                # this part has an allowed format
                allowed_parts.append(part)
                # increase the occurrence of this syllable
                if part in stats['syllables']:
                    stats['syllables'][part] += 1
                else:
                    stats['syllables'][part] = 1
                # add syllable to list of syllables starting with this character
                char = part[0]
                if char in stats['by_char']:
                    stats['by_char'][char][part] = 1
                else:
                    stats['by_char'][char] = { part:1 }
    
    count_combinations(stats, allowed_parts)


def is_format(part, format):
    """ Return whether the given part is in the given format. """
    types = ''
    for char in part:
        types += get_type(char)
    return (types == format)


def count_combinations(stats, parts):
    """ Add the character string transitions between the given parts to stats. """
    previous = '';
    for current in parts:
        if (previous != ''):
            last_char = previous[-1]
            current_char = current[0]
            if last_char in stats['combinations']:
                if current_char in stats['combinations'][last_char]:
                    stats['combinations'][last_char][current_char] += 1
                else:
                    stats['combinations'][last_char][current_char] = 1
            else:
                stats['combinations'][last_char] = {current_char: 1}
        previous = current


def get_type(char):
    """ Return whether the given char is a vowel (v) or consonant (c). """
    if char in vowels:
        return 'v'
    return 'c'


if __name__ == "__main__":
    main()