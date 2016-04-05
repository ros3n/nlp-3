from collections import defaultdict
from levenshtein import levenshtein_distance


class ErrorProbabilityCalculator(object):
    def __init__(self):
        self.error_probability = defaultdict(lambda: 0)
        self.raw_data = []

    def read_data(self, fle):
        with open(fle, encoding='iso-8859-2') as f:
            self.raw_data = f.readlines()

    def calculate_probability(self):
        for line in self.raw_data:
            err, corr = line.split(';')
            dist = levenshtein_distance(err, corr)
            self.error_probability[dist] += 1
        length = len(self.raw_data)
        for k, v in self.error_probability.items():
            self.error_probability[k] = v / length
        return self.error_probability
