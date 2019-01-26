# What is this?
Some simple code that recognizes and quantifies rhymes, slant rhymes and varying degrees of alliteration by 
using the CMU Pronouncing Dictionary (part of the nltk libraries) to convert words to their phonetic components (phones) as
represented by the ARPAbet symbols found here: http://www.speech.cs.cmu.edu/cgi-bin/cmudict 
and here: https://en.wikipedia.org/wiki/ARPABET

Information about different types of rhymes and various examples can be found here: https://en.wikipedia.org/wiki/Perfect_and_imperfect_rhymes 
and here: https://www.litcharts.com/literary-devices-and-terms/slant-rhyme

The project is still a work in progress, and more features will be added over time.

# Why?
To learn about the characteristics of rhymes, and the media that employs them. Potential applications include analysing and generating rhyme schemes automatically, visulization of song structure and phonetic sounds (i.e. simulating synesthesia), measuring the rhyme and alliteration density of a given lyric or poem, and looking at the particular rhyming style of an artist. The same principles can also be applied to study phonetic properties of accents and language itself.

The goal of the project is to answer some of the following questions:

* Why does one wording of a sentence sound better than another, especially in the context of a song or poetry?
* Can we quantify how much a given set of words rhyme in a way that makes sense?
* What are the limits of rhyming? What roles to vowels and consonants play?
* Can we tell the genre or artist of a song by the phonetic patterns alone? Rhyme density, alliteration etc.
* Can we recognise rhyme schemes, including multi-syllabic and slant rhymes, automatically?
* Can we guess the accent of an artist by examining the rhymes they use?


# How does it work?
A short summary - an input string is converted into it's component ARPAbet phones, and each phone is assigned a position in a vowel (shown below) or consonant space. The distances between each phone in the original string are compared to a specified threshold value in order to determine whether or not a particular set of phones rhyme or alliterate. Rhyming phone sets (called chunks here) are then assigned a color, allowing the two rhyming chunks to be highlighted accordingly and visually associated in the final reconstruction of the word.

The following is a more in depth description of how the code works.

Lyrics are split into phonetic components (phones), and split into two types of groups; groups of consonants which appear before a vowel, and chunks which consist of a vowel and the consonants which appear after it. Every syllable (vowel) is accounted for by grouping it with two groups of consonants this way, for example the phrase "relax and strive" would become [R][IH][L] [L][AE][K,S] [AH][N,D] [S,T,R][AY][V], where every vowel is preceeded by the group of consonants that appear before it and followed by the group of consonants which appear after it. Compare "five" ([F][AY][V]) to "strive" ([S,T,R][AY][V]) and we can easily see that they rhyme since the vowel [AY] and consonant group after the vowel [V] are identical. We can see that the words do not perfectly alliterate since the consonant groups before the vowel [S,T,R] and [F] are different. (The advatnage of this approach is that it allows us to detect multi-syllabic rhymes - see examples below.)

The idea is to quantify how much a given pair of ([consonants_bv][vowel][consonants_av]) rhyme and alliterate by giving each vowel phone and each consonant phone a coordinate in a vowel/ consonant space and then measuring the distance between these coordinates. We can also assign each vowel a color by making the vowel space act doubly as an RGB color space. A logical choice for a vowel space is to follow a standard vowel diagram, which depicts where the toungue lies in the mouth when pronouncing each vowel. https://en.wikipedia.org/wiki/Vowel_diagram Here we simply assume that the closer the tongue when pronouncing two vowels, the closer they must sound, and therefore the closer they should be in the vowel space. The following vowel space (which is represented by vowel_color_dict in config.py) was constructed for this project:

<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/vowel_chart_image.png" alt="alt text" width="60%" height="50%"></p>

The consonant space is constructed based on the IPA consonant chart which can be found here: https://home.cc.umanitoba.ca/~krussll/phonetics/ipa/ipa-consonants.html
For example, B and D are closer together than B and F, but not as close as B and P or D and T. 

Once each ([vowel][consonants_av]) chunk is assigned positions in the vowel and consonant space, every length 2 permutation of chunks is compared in terms of proximity in the space and assigned a score and color. We can then set threshold values for how close two vowels or consonants have to be in the vowel or consonant space to count as a rhyme. If a pair of chunks scores higher than the threshold, a rhyme pair object is then created which consists of the two chunk objects, the distance between their respective vowel in the vowel space, and the average distance between the consonants of their consonant groups in the consonant space.
Sty (https://github.com/feluxe/sty) is then used to highlight each chunk (that is part of a rhyme pair) with the assigned color and every phone is printed in order to reconstruct the input string with rhymes highlighted in a phonetical color code. 

# Caveats and future work
The code currently serves as a proof of concept for measuring and quantifying slant rhymes, and will act as a foundation to build a more robust rhyme scheme detector.
In its current form does not take into account every consonant individually, but rather judges by the "average" consonant of a group. This can lead to false positives and negatives in rhyme and alliteration detection. It also simply looks for any two syllables that rhyme, even if 'insignificant' fractions of words (for example about and subliminal are detected just because the first syllable of each rhymes)  - a more sophisticated version which considers syllable counts and stress patterns is planned. Additionally the code does not currently take into account the position of a word in a line and score based rhyme highlighting should be implemented - highlights should be more intense for high rhyme scores and less intense for low rhyme scores - this should make the main rhyme scheme more pronounced, while preserving the secondary rhyme schemes.

# Examples
Y.B. Yeats - Lines written in Dejection

<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.56.16.png" alt="alt text" width="60%" height="50%"></p>

Yeats uses heavily slanted rhymes in this poem - rhyming 'on' with 'moon' and 'gone' with 'sun'. For the first example we show the output when we measure how much 'on' and 'moon' rhyme. Here the first number after the vowels (6.32...) represents the distance in the vowel space from one vowel to the other. On the vowel space above we find AA on the bottom right corner and UW on the top right (and further along the z-axis). The following number (3) represents the similarity in consonants following the vowel. Here they are both followed by the same consonant 'N' - and this perfect consonance is what allows the words to 'rhyme' despite the vowels being far apart in the vowel space.


<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.37.49.png" alt="alt text" width="60%" height="50%"></p>

Here we see a multi-syllabic perfect rhyme in "relax and strive" and "jackson five". The distance between each vowel syllable is 0 and the consonance is identical in each consonant group following a vowel. Notice that each rhyme is higlighted according to it's position in the vowel space, allowing us to see the phonetic content without reading the words. Here the "ax" in relax rhyming with the "acks" in Jackson are in yellow, the "and" and "son" from Jackson are in green, and the "ive" from strive and "ive" from five are in brown.

Nas - Halftime
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2011.47.31.png" alt="alt text" width="60%" height="50%"></p>

Input string:

<p align="center">
"i used to hustle now all I do is relax and strive
when i was young i was a fan of the jackson five"
</p>

The above multi-syllabic rhyme in the context of the song.

Below are some examples of more complex rhyming schemes with varying structure, density and phonetic content, along with their respective input strings.

Q-Tip - Scenario 
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2011.28.16.png" alt="alt text" width="60%" height="50%"></p>

<p align="center">
"it's a leader quest mission and we got the goods here ,
never on the left because my rights my good ear ,
i could give a damn about a ill subliminal ,
Stay away from crime so I ain't no criminal"
</p>

Mike G - Oldie
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.14.44.png" alt="alt text" width="60%" height="50%"></p>

<p align="center">
"and you don't even need to look cause we gleam obscene 
in the light ride slow to my yellow diamond shining like 
the batman logo over gotham"
</p>

A song I wrote about an overconfident boxer who dies in the ring.
<p align="center">
<img src="https://github.com/scottgilmartin/DEFT/blob/master/images/Screen%20Shot%202019-01-23%20at%2000.21.45.png" alt="alt text" width="60%" height="50%"></p>

<p align="center">
"if i cheat i can beat them man i'm destined to defeat them hand 
to hand in a ring yeah i'll float and i'll sting"
</p>


