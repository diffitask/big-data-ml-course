# %%file is an Ipython magic function that saves the code cell as a file

from mrjob.job import MRJob
from mrjob.step import MRStep

class MRLongestCharacterPhrase(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_character_phrase,
                   combiner=self.combiner_longest_phrase,
                   reducer=self.reducer_longest_phrase),
            MRStep(reducer=self.reducer_sort_characters_by_phrase_len)
        ]

    def mapper_get_character_phrase(self, _, line):
        line_words = line.replace('"', '').split()
        character = line_words[1]
        phrase = ' '.join(line_words[2:])
        yield (character, phrase)

    def combiner_longest_phrase(self, character, phrases):
        # optimization: longest character phrase we've seen so far
        longest_character_phrase = max(phrases, key=len)
        yield (character, longest_character_phrase)

    def reducer_longest_phrase(self, character, longest_phrases):
        # the longest character phrase among all data
        longest_character_phrase = max(longest_phrases, key=len)
        yield None, (character, longest_character_phrase)

    # discard the key; it is just None
    def reducer_sort_characters_by_phrase_len(self, _, character_longest_phrase_pairs):
        # each item of character_longest_phrase_pairs is (character, longest_phrase)
        # convert to list bc 'generator' object is not subscriptable
        character_longest_phrase_pairs = list(character_longest_phrase_pairs)
        
        # sort by total phrases count
        character_longest_phrase_pairs.sort(
            key=lambda pair: len(pair[1]),
            reverse=True
        )

        # return the result
        for character_phrase_pair in character_longest_phrase_pairs:
            yield character_phrase_pair


if __name__ == '__main__':
    MRLongestCharacterPhrase.run()
