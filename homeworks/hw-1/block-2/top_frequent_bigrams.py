# %%file is an Ipython magic function that saves the code cell as a file

from mrjob.job import MRJob
from mrjob.step import MRStep
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams

TOP_N = 20

class MRTopFrequentBigrams(MRJob):
    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper_clean_text_and_split_by_bigramms,
                   combiner=self.combiner_count_bigrams,
                   reducer=self.reducer_count_bigrams),
            MRStep(reducer=self.reducer_top_frequent_bigrams)
        ]

    def mapper_init(self):
        nltk.download('punkt')
        nltk.download('stopwords')

    def mapper_clean_text_and_split_by_bigramms(self, _, line):
        # text preprocessing
        line = line.lower()
        
        # cleaning from punctuation
        line = line.translate(str.maketrans('', '', string.punctuation))
        # splitting into words
        line_words = line.split()

        phrase = ' '.join(line_words[2:])
        # tokenizing
        phrase_tokens = word_tokenize(phrase)
        # cleaning from the stop words
        stop_words = set(stopwords.words('english'))
        phrase_tokens = [token for token in phrase_tokens if token not in stop_words]

        # splitting to bigrams
        phrase_bigrams = list(ngrams(phrase_tokens, 2))

        # returning res
        for bigram in phrase_bigrams:
            yield (bigram, 1)

    def combiner_count_bigrams(self, bigram, bigram_counts):
        # optimization: sum the characters we've seen so far
        yield (bigram, sum(bigram_counts))

    def reducer_count_bigrams(self, bigram, bigram_counts):
        # send all (character, phrases_counts) pairs to the same reducer.
        yield None, (bigram, sum(bigram_counts))

    # discard the key; it is just None
    def reducer_top_frequent_bigrams(self, _, bigram_count_pairs):
        # each item of bigram_count_pairs is (bigram, count)
        # convert to list bc 'generator' object is not subscriptable
        bigram_count_pairs = list(bigram_count_pairs)
        
        # sort by bigram count
        bigram_count_pairs.sort(
            key=lambda pair: pair[1],
            reverse=True
        )

        # get top N frequent bigrams
        top_frequent_bigrams = bigram_count_pairs[:TOP_N]

        # return the result
        for bigram_count_pair in top_frequent_bigrams:
            yield bigram_count_pair


if __name__ == '__main__':
    MRTopFrequentBigrams.run()
