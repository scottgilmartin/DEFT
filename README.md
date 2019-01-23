# What is this?
Some simple code that recognizes and quantifies rhymes, slant rhymes and varying degrees of alliteration by 
using the CMU Pronouncing Dictionary (part of the nltk libraries) to convert words to their phonetic components (phones) as
represented by the ARPAbet symbols found here: http://www.speech.cs.cmu.edu/cgi-bin/cmudict 
and here: https://en.wikipedia.org/wiki/ARPABET

Information about different types of rhymes and various examples can be found here: https://en.wikipedia.org/wiki/Perfect_and_imperfect_rhymes 
and here: https://www.litcharts.com/literary-devices-and-terms/slant-rhyme

# Why?
To learn about the characteristics of rhymes, and the media which employs them. Potential applications include analysing and generating rhyme schemes automatically, visulization of song structure and phonetic sounds (i.e. simulating synesthesia), measuring the rhyme and alliteration density of a given lyric or poem, and looking at the particular rhyming style of an artist. 

# How does it work?
Lyrics are split into phonetic components (phones), and split into two types of groups; groups of consonants which appear before a vowel, and chunks which consist of a vowel and the consonants which appear after it. Every syllable (vowel) is accounted for by grouping it with two groups of consonants this way, for example the phrase "relax and strive" would become [R][IH][L] [L][AE][K,S] [AH][N,D] [S,T,R][AY][V], where every vowel is preceeded by the group of consonants that appear before it and followed by the group of consonants which appear after it.

# Caveats
The code in its current form does not take into account every consonant individually, but rather judges by the "average" consonant of a group. This can lead to false positives and negatives in rhyme and alliteration detection.
In the case where chunk A rhymes with chunk B, chunk B rhymes with chunk C but chunk A does not rhyme with chunk C, one of the rhymes may be assigned an unrepresentative color.
The code is also not equipped to recognize the position of a word in a line.

# Examples
