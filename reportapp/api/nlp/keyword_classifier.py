import string
from collections import Counter, defaultdict
from itertools import chain, groupby, product

import nltk
from functools import reduce
from enum import Enum
from nltk.tokenize import wordpunct_tokenize


class Metric(Enum):
    DEGREE_TO_FREQUENCY_RATIO = 0  # Uses d(w)/f(w) as the metric
    WORD_DEGREE = 1  # Uses d(w) alone as the metric
    WORD_FREQUENCY = 2  # Uses f(w) alone as the metric


class keyword_classify(object):
    def __init__(
        self,
        stopwords=None,
        punctuations=None,
        language="english",
        ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,
    ):
        if isinstance(ranking_metric, Metric):
            self.metric = ranking_metric
        else:
            self.metric = Metric.DEGREE_TO_FREQUENCY_RATIO
        self.stopwords = stopwords
        if self.stopwords is None:
            self.stopwords = nltk.corpus.stopwords.words(language)

        # If punctuations are not provided we ignore all punctuation symbols.
        self.punctuations = punctuations
        if self.punctuations is None:
            self.punctuations = string.punctuation

        # All things which act as sentence breaks during keyword extraction.
        self.to_ignore = set(chain(self.stopwords, self.punctuations))

        # Stuff to be extracted from the provided text.
        self.frequency_dist = None
        self.degree = None
        self.rank_dict = None
        self.ranked_phrases = None

    def extract_keywords_from_text(self, text):
        sentences = nltk.tokenize.sent_tokenize(text)
        self.extract_keywords_from_sentences(sentences)

    def extract_keywords_from_sentences(self, sentences):
        phrase_list = self._generate_phrases(sentences)
        self._build_frequency_dist(phrase_list)
        self._build_word_co_occurance_graph(phrase_list)
        self._build_ranklist(phrase_list)

    def get_ranked_phrases_with_scores(self):
        return self.rank_dict

    def get_word_frequency_distribution(self):
        return self.frequency_dist

    def get_word_degrees(self):
        return self.degree

    def _build_frequency_dist(self, phrase_list):
        self.frequency_dist = Counter(chain.from_iterable(phrase_list))

    def _build_word_co_occurance_graph(self, phrase_list):
        co_occurance_graph = defaultdict(lambda: defaultdict(lambda: 0))
        for phrase in phrase_list:
            for (word, coword) in product(phrase, phrase):
                co_occurance_graph[word][coword] += 1
        self.degree = defaultdict(lambda: 0)
        for key in co_occurance_graph:
            self.degree[key] = sum(co_occurance_graph[key].values())

    def _build_ranklist(self, phrase_list):
        self.rank_dict = {}
        for phrase in phrase_list:
            rank = 0.0
            for word in phrase:
                if self.metric == Metric.DEGREE_TO_FREQUENCY_RATIO:
                    rank += 1.0 * self.degree[word] / self.frequency_dist[word]
                elif self.metric == Metric.WORD_DEGREE:
                    rank += 1.0 * self.degree[word]
                else:
                    rank += 1.0 * self.frequency_dist[word]
            self.rank_dict[phrase] = rank 
        # self.rank_dict.sort(reverse=True)
        # self.ranked_phrases = [ph[1] for ph in self.rank_dict]

    def _generate_phrases(self, sentences):
        phrase_list = set()
        for sentence in sentences:
            word_list = [word.lower() for word in wordpunct_tokenize(sentence)]
            phrase_list.update(self._get_phrase_list_from_words(word_list))

        return phrase_list
    def _get_phrase_list_from_words(self, word_list):
        # print(type(word_list))
        group = []
        for x in word_list:
            if x not in self.to_ignore:
                group.append(x)
        # groups = groupby(word_list, lambda x: x not in self.to_ignore)
        # tuple(group[1]) for group in groups if group[0]
        return group