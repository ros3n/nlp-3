from collections import defaultdict
import sys
import dill
import numpy as np


class ErrorProbabilityCalculator(object):
    def __init__(self, error_probability=None):
        if error_probability:
            self.error_probability = error_probability
        else:
            self.error_probability = defaultdict(lambda: 0)
        self.raw_data = []

    def levenshtein_distance(self, word_a, word_b):
        indicator = lambda x, y: 0 if x == y else 1
        len_a = len(word_a)
        len_b = len(word_b)
        if min(len_a, len_b) == 0:
            return max(len_a, len_b)
        distance = np.empty([len_a + 1, len_b + 1])
        for i in range(0, len_a + 1):
            distance[i][0] = i
        for j in range(0, len_b + 1):
            distance[0][j] = j
        for i, a in enumerate(word_a, start=1):
            for j, b in enumerate(word_b, start=1):
                distance[i][j] = min(
                    distance[i - 1][j] + 1,
                    distance[i][j - 1] + 1,
                    distance[i - 1][j - 1] + indicator(a, b)
                )
        return distance[len_a][len_b]

    def read_data(self, fle):
        with open(fle, encoding='iso-8859-2') as f:
            self.raw_data = f.readlines()

    def calculate_statistics(self):
        for line in self.raw_data:
            err, corr = line.split(';')
            dist = self.levenshtein_distance(err, corr)
            self.error_probability[dist] += 1
        length = len(self.raw_data)
        for k, v in self.error_probability.items():
            self.error_probability[k] = v / length
        return self.error_probability

    def calculate_probability(self, sample, correct):
        dist = self.levenshtein_distance(sample, correct)
        return self.error_probability[dist]

    def dump_statistics(self, path):
        with open(path, 'wb') as f:
            dill.dump(self.error_probability, f)

if __name__ == '__main__':
    e = ErrorProbabilityCalculator()
    e.read_data(sys.argv[1])
    e.calculate_statistics()
    e.dump_statistics('cache/ep.data')
    with open('cache/ep.data', 'rb') as f:
        print(dill.load(f))
