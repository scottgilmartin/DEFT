# What is this?
Some simple code that recognizes and quantifies rhymes, slant rhymes and varying degrees of alliteration by 
using the CMU Pronouncing Dictionary (part of the nltk libraries) to convert words to their phonetic components (phones) as
represented by the ARPAbet symbols found here: http://www.speech.cs.cmu.edu/cgi-bin/cmudict 
and here: https://en.wikipedia.org/wiki/ARPABET

Information about different types of rhymes and various examples can be found here: https://en.wikipedia.org/wiki/Perfect_and_imperfect_rhymes 
and here: https://www.litcharts.com/literary-devices-and-terms/slant-rhyme

# Why?
To learn about the characteristics of rhymes, and the media which employs them. Potential applications include analysing and generating rhyme schemes automatically, visulization of song structure and phonetic sounds (i.e. simulating synesthesia), measuring the rhyme and alliteration density of a given lyric or poem, and looking at the particular rhyming style of an artist. The same principles can also be applied to study phonetic properties of accents and language itself.

# How does it work?
Lyrics are split into phonetic components (phones), and split into two types of groups; groups of consonants which appear before a vowel, and chunks which consist of a vowel and the consonants which appear after it. Every syllable (vowel) is accounted for by grouping it with two groups of consonants this way, for example the phrase "relax and strive" would become [R][IH][L] [L][AE][K,S] [AH][N,D] [S,T,R][AY][V], where every vowel is preceeded by the group of consonants that appear before it and followed by the group of consonants which appear after it. Compare "five" ([F][AY][V]) to "strive" ([S,T,R][AY][V]) and we can easily see that they rhyme since the vowel [AY] and consonant group after the vowel [V] are identical. We can see that the words do not perfectly alliterate since the consonant groups before the vowel [S,T,R] and [F] are different. 

The idea is to quantify how much a given pair of ([consonants_bv][vowel][consonants_av]) rhyme and alliterate by giving each vowel phone and each consonant phone a coordinate in a vowel/ consonant space and then measuring the distance between these coordinates. We can also assign each vowel a color by making the vowel space act doubly as an RGB color space. A logical choice for a vowel space is to follow a standard vowel diagram, which depicts where the toungue lies in the mouth when pronouncing each vowel. https://en.wikipedia.org/wiki/Vowel_diagram Here we simply assume that the closer the tongue when pronouncing two vowels, the closer they must sound, and therefore the closer they should be in the vowel space. The following vowel space was constructed for this project:

<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/vowel_chart_image.png" alt="alt text" width="60%" height="50%"></p>

The consonant space is constructed based on the IPA consonant chart which can be found here: https://home.cc.umanitoba.ca/~krussll/phonetics/ipa/ipa-consonants.html
For example, B and D are closer together than B and F, but not as close as B and P or D and T. 

# Caveats and future work
The code currently serves as a proof of concept for measuring and quantifying slant rhymes, and will act as a foundation to build a more robust rhyme scheme detector.
In its current form does not take into account every consonant individually, but rather judges by the "average" consonant of a group. This can lead to false positives and negatives in rhyme and alliteration detection. It also simply looks for any two syllables that rhyme, even if 'insignificant' fractions of words (for example about and subliminal are detected just because the first syllable of each rhymes)  - a more sophisticated version which considers syllable counts and stress patterns is planned.
In the case where chunk A rhymes with chunk B, chunk B rhymes with chunk C but chunk A does not rhyme with chunk C, one of the rhymes may be assigned an unrepresentative color.
The code does not currently take into account the position of a word in a line.

# Examples
Y.B. Yeats
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.56.16.png" alt="alt text" width="60%" height="50%"></p>

Nas - Halftime
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.37.49.png" alt="alt text" width="60%" height="50%"></p>

Nas - Halftime
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.35.02.png" alt="alt text" width="60%" height="50%"></p>

Q-Tip - Scenario 
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2011.28.16.png" alt="alt text" width="60%" height="50%"></p>

Mike G - Oldie
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.14.44.png" alt="alt text" width="60%" height="50%"></p>

A song I wrote about an overconfident boxer who dies in the ring.
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.21.45.png" alt="alt text" width="60%" height="50%"></p>

Nas - N.Y. State of mind
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.30.59.png" alt="alt text" width="60%" height="50%"></p>


