# %%file is an Ipython magic function that saves the code cell as a file

from mrjob.job import MRJob
from mrjob.step import MRStep

TOP_N = 20

class MRMostTalkativeCharacters(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_characters,
                   combiner=self.combiner_count_phrases,
                   reducer=self.reducer_count_phrases),
            MRStep(reducer=self.reducer_top_talkative_characters)
        ]

    def mapper_get_characters(self, _, line):
        line_words = line.replace('"', '').split()
        character = line_words[1]
        yield (character, 1)

    def combiner_count_phrases(self, character, phrases_counts):
        # optimization: sum the characters we've seen so far
        yield (character, sum(phrases_counts))

    def reducer_count_phrases(self, character, phrases_counts):
        # send all (character, phrases_counts) pairs to the same reducer.
        yield None, (character, sum(phrases_counts))

    # discard the key; it is just None
    def reducer_top_talkative_characters(self, _, character_phrases_count_pairs):
        # each item of character_phrases_count_pairs is (character, total_phrases_count)
        # convert to list bc 'generator' object is not subscriptable
        character_phrases_count_pairs = list(character_phrases_count_pairs)
        
        # sort by total phrases count
        character_phrases_count_pairs.sort(
            key=lambda pair: pair[1],
            reverse=True
        )

        # get top N talkative characters
        top_talkative_characters = character_phrases_count_pairs[:TOP_N]
        
        # return the result
        for character_count_pair in top_talkative_characters:
            yield character_count_pair


if __name__ == '__main__':
    MRMostTalkativeCharacters.run()
