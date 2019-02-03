import deft
from helper_functions import split_lyrics
import nltk
import unittest


class Tests(unittest.TestCase):
    def setUp(self):
        entries = nltk.corpus.cmudict.entries()
        lyric = ["a", "pink", "shift", "blacksmith", "beat", "bead", "bit", "bid", "a", "i"]
        line_arpas = split_lyrics(lyric, entries)[0]
        arpa_words = split_lyrics(lyric, entries)[1]
        self.vowels, self.consonants, vowel_words = deft.get_components(line_arpas, arpa_words)
        self.congrps, self.congrps_bv, self.chunks = deft.group_components(self.vowels, self.consonants, vowel_words)
        self.rhyme_pairs, self.alliteration_pairs = deft.generate_goodness_pairs(self.congrps, self.congrps_bv,
                                                                                 self.chunks, 2, 1, 6, 0)

    def test_alliteration(self):
        self.assertEqual(self.congrps_bv[3].compare_to_congrp(self.congrps_bv[5]), 1.5,
                         'Check blacksmith alliterates with beat, scores 1.5')
        self.assertEqual(self.congrps_bv[1].compare_to_congrp(self.congrps_bv[3]), 1,
                         'Check pink alliterates with blacksmith, scores 1')
        self.assertEqual(self.congrps_bv[1].compare_to_congrp(self.congrps_bv[5]), 2,
                         'Check pink almost perfectly alliterates with beat, scores 2')
        self.assertEqual(self.congrps_bv[5].compare_to_congrp(self.congrps_bv[7]), 3,
                         'Check beat perfectly alliterates with bit, scores 3')
        self.assertEqual(self.congrps_bv[5].compare_to_congrp(self.congrps_bv[5]), 3,
                         'Check beat perfectly alliterates with itself, scores 3')
        self.assertEqual(self.congrps_bv[9].compare_to_congrp(self.congrps_bv[10]), 3,
                         'Check the empty consonant groups from a and i alliterate perfectly, scores 3')
        self.assertEqual(self.congrps_bv[9].compare_to_congrp(self.congrps_bv[1]), 3,
                         'Check the empty consonant groups from a and i alliterate perfectly, scores 3')

    def test_rhyming(self):
        self.assertEqual(self.chunks[5].compare_to_chunk(self.chunks[6]), (0, 2, (0, 2)),
                         'Check beat and bead rhyme, the congrps score 2, and the stress difference is 0')
        self.assertEqual(self.chunks[5].compare_to_chunk(self.chunks[7]), (1.4142135623730951, 3, (0, 2)),
                         'Check the near rhyme bead and bid')


if __name__ == '__main__':
    unittest.main()
