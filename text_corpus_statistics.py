#! -*- coding: utf-8 -*-

from collections import defaultdict
import re
import sys
import dill


class TextCorpusStatisticsCalculator(object):
    def __init__(self, files):
        self.occurrneces = defaultdict(lambda: 0)
        self.files = files
        self.words = []

    def read_words(self, fle):
        with open(fle, encoding='iso-8859-2') as f:
            self.words = f.readlines()
            self.words = list(map(lambda x: x.strip(), self.words))
            return self.words

    def read_data(self, fle):
        with open(fle) as f:
            data = f.read()
            return data

    def remove_special_chars(self, text):
        text = text.lower()
        text = re.sub('\n', ' ', text)
        text = ''.join(e for e in text if e.isalnum() or e == ' ')
        return text.split(' ')

    def calculate_statistics(self):
        for f in files:
            text = self.read_data(f)
            text = self.remove_special_chars(text)
            for word in text:
                if self.occurrneces[word] > 0 or word in self.words:
                    self.occurrneces[word] += 1
                    # print(word, self.occurrneces[word])

    def dump_statistics(self, path):
        with open(path, 'wb') as f:
            dill.dump(self.occurrneces, f)


if __name__ == '__main__':
    files = sys.argv[2:]
    calc = TextCorpusStatisticsCalculator(files)
    calc.read_words(sys.argv[1])
    calc.calculate_statistics()
    calc.dump_statistics('cache/occ.data')
