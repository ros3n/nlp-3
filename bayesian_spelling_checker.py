from error_probability import ErrorProbabilityCalculator
from text_corpus_statistics import TextCorpusStatisticsCalculator
import dill


class BayesianSpellingChecker(object):
    def __init__(self, words_file, ep_cache_file, occ_cache_file, accuracy):
        with open(ep_cache_file, 'rb') as f:
            self.error_probability = dill.load(f)
        with open(occ_cache_file, 'rb') as f:
            self.occurrneces = dill.load(f)
        self.words = TextCorpusStatisticsCalculator([]).read_words(words_file)
        self.accuracy = accuracy
        self.n = sum([v for k, v in self.occurrneces.items()])
        self.m = len(self.words)
        self.calc = ErrorProbabilityCalculator()

    def correct_error(self, word):
        candidates1 = self.edits(word)
        candidates_n = self.n_edits(candidates1, self.accuracy)
        max_prob = 0.0
        correct = ''
        for candidate in candidates1 | candidates_n:
            dist = self.calc.levenshtein_distance(candidate, word)
            prob = self.error_probability[dist] * (self.occurrneces[candidate] + 1) / (self.n + self.m)
            if prob > max_prob:
                max_prob = prob
                correct = candidate
        return max_prob, correct

    def edits(self, word):
        alphabet = 'aąbcćdeęfghijklłmnoópqrsśtuvwxyzżź'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts = [a + c + b for a, b in splits for c in alphabet]
        candidates = deletes + transposes + replaces + inserts
        return set(filter(lambda x: x in self.words, candidates))

    def n_edits(self, edits, n):
        if n < 2:
            return set([])
        else:
            candidates = set(e2 for e1 in edits for e2 in self.edits(e1) if e2 in self.words)
            candidates |= self.n_edits(candidates, n - 1)
            return edits | candidates
