#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 00:26:41 2018

@author: scottgilmartin
"""
from classes import Vowel,Consonant,Con_grp,Chunk,Alliteration_pair,Rhyme_pair
from config import vowel_color_dict,consonant_color_dict,T1,T2,T3,T4,T5
from helper_functions import split_lyrics,contain_nums,generate_pairs
import nltk
import re #strip numbers from string using reg expression
from sty import bg #used to print rhyme schemes with color highlights

with open('/Users/scottgilmartin/Desktop/sample.txt') as myfile:
 w = myfile.read().split()

entries = nltk.corpus.cmudict.entries()

lyric1 = ["relax","and","strive"]
lyric2 = ["jackson","five","alive","and","pal"]
lyric=lyric1
lyric.extend(lyric2)

line_arpas=split_lyrics(w,entries)[0]
arpa_words=split_lyrics(w,entries)[1]


def get_components(line_arpas,arpa_words):
    """
    Extract the vowels and consonants from the lyrics
    """

    vowels=[Vowel(i,line_arpas[i],vowel_color_dict[re.sub(r'\d+', '',line_arpas[i])][1], #have to strip num to get dict key
            vowel_color_dict[re.sub(r'\d+', '',line_arpas[i])][0],arpa_words[i],int(re.sub('[^0-9]','', line_arpas[i]))) #strip non num to get stress
            for i in range(len(line_arpas)) if contain_nums(line_arpas[i])]
    
    consonants=[Consonant(i,line_arpas[i],consonant_color_dict[re.sub(r'\d+', '',line_arpas[i])][1],#have to strip num to get dict key
                consonant_color_dict[re.sub(r'\d+', '',line_arpas[i])][0],arpa_words[i])
                for i in range(len(line_arpas)) if not contain_nums(line_arpas[i])]
    
    vowel_words=[vow.root_word for vow in vowels] 
    
    return vowels, consonants, vowel_words


def group_components(vowels,consonants,vowel_words): 
    """
    group the component vowels and consonants into 3 groups; the group of consonants that come after each vowel in a word,
    the group of consonants that come before each vowel in a word, and chunks, which are pairings of vowels and the
    consonant group which immediately follows it.
    """
    
    congrps=[Con_grp(i) for i in range(len(vowel_words))] #these are the groups of consonants that come after a vowel in a word, 1 letter words like "a" will generate an empty group
                                                          

    for i in range(len(vowel_words)): #add consonants that appear after vowels to the consonant groups
        for con in consonants:
            if con.root_word==vowel_words[i] and con.idx>vowels[i].idx:
                if i<(len(vowel_words)-1): 
                    if con.idx<vowels[i+1].idx: #make sure we don't get consonants after next syllables in word too
                        congrps[i].add_consonant(con)
                else:
                     congrps[i].add_consonant(con)
                     
                               
    congrps_bv=[Con_grp(i) for i in range(len(vowel_words))]

    
    for i in range(len(vowel_words)): #add consonants that appear before vowels to the consonant groups
        for con in consonants:
            if con.root_word==vowel_words[i] and con.idx<vowels[i].idx:
                if i>0: 
                    if con.idx>vowels[i-1].idx: #make sure we don't get repeats for the same word
                        congrps_bv[i].add_consonant(con)
                else:
                    congrps_bv[i].add_consonant(con)
    
    
    chunks=[Chunk(vowels[i],congrps[i],i) for i in range(len(vowels))] #define the chunks, i.e. the vowel and end consonant group pairs
    
    return congrps, congrps_bv, chunks

def generate_goodness_pairs(congrps, congrps_bv, chunks, t1,t2,t3,t4): #thresholds for rhyming strictness, see config
    """
    Generate rhyming and alliterating pairs by comparing every possible permutation of chunks and before vowel congrps
    and taking the ones that score highly enough in similarity as specified by the thresholds.
    """
    #generate every pair (permutation) of chunks and compare them
    pairs=list(generate_pairs(chunks))
    
    #Compare the chunks in each pair, and store the result with the index of each
    chunk_compar=sorted([(pairs[i][0].compare_to_chunk(pairs[i][1]),pairs[i][0].idx,pairs[i][1].idx) for i in range(len(pairs))])
    
    pairs_bv=list(generate_pairs(congrps_bv)) 
    
    #Compare the before vowel consonant groups in each pair, and store the comparison score with the index of each
    congrp_bv_compar=sorted([(pairs_bv[i][0].compare_to_congrp(pairs_bv[i][1]),pairs_bv[i][0].idx,pairs_bv[i][1].idx)
    for i in range(len(pairs_bv))]) 
     
    #get the ids of the chunks associated with each ith comparison pair
    ids=[(i,chunk_compar[i][1],chunk_compar[i][2]) for i in range(len(chunk_compar))] 
    scores=[chunk_compar[i][0] for i in range(len(chunk_compar))] #just the scores returned from the class method
    
    rhymes=[]
    for i in range(len(ids)): 
        if scores[i][2][1]==0: #if both stresses are zero in the pair
            if scores[i][0]<t3 and scores[i][1]>t4: #rhyme threshold, more lenient for 0 stress
                rhymes.append((ids[i][1],ids[i][2],i)) 
        else:
            if scores[i][0]<t1 and scores[i][1]>t2: #stricter rhyme threshold, higher stress
                rhymes.append((ids[i][1],ids[i][2],i))
                
    alliterations=[]
    for i in range(len(congrp_bv_compar)):
        if congrp_bv_compar[i][0]>T5: #alliteration threshold, i.e.e require consonants to be in the same group
            alliterations.append((congrp_bv_compar[i][1],congrp_bv_compar[i][2],congrp_bv_compar[i][0]))
    
    rhyme_pairs=[Rhyme_pair(i,chunks[rhymes[i][0]],chunks[rhymes[i][1]],chunk_compar[rhymes[i][2]][0]) for i in range(len(rhymes))] #arranged as (COLOR, (DIST,ALLIT,STRESS), IDX OF THIS, IDX OF MATCH)
    
    alliteration_pairs=[Alliteration_pair(congrps_bv[alliterations[i][0]],congrps_bv[alliterations[i][1]],alliterations[i][2]) #arranged as (ALLIT SCORE, THIS IDX, IDX OF MATCH)
    for i in range(len(alliterations))]
    
    return rhyme_pairs, alliteration_pairs



def reconstruct_lyrics(vowels,congrps,congrps_bv,chunks,rhyme_pairs,alliteration_pairs):
    """
    Prints the lyrics in arpabet form, with rhyme and alliteration pairing information printed next to each component.
    Printed in the form: (COLOR), SCORE, INDEX OF COMPONENTS INVOLVED IN PAIR
    e.g. the IH1 in pink matching with the IH1 in shift looks like (color of IH1, 
    (distance from IH1 to IH1=0,alliteration score which=1 since K and T share a group, and stress diff=0), 
    idx of pink's IH1 in the vowel list, idx of shift's IH1 in the vowel list)
    """
    #word reconstruction
    for j in range(len(vowels)):
        print(vowels[j].root_word)
        print([congrps_bv[j].consonant_list[i].name for i in range(len(congrps_bv[j].consonant_list))],'bv',
                           [(altr.score,altr.idx1,altr.idx2) for altr in alliteration_pairs if altr.idx1==j or altr.idx2==j])
        print([chunks[j].vowel.name],'v',[(rhyme.rhyme_nums,rhyme.idx1,rhyme.idx2) for rhyme in rhyme_pairs if rhyme.idx1==j or rhyme.idx2==j])
        print([chunks[j].congrp.consonant_list[i].name for i in range(len(chunks[j].congrp.consonant_list))],'av')     
    return


def color_rhymes(vowels,rhyme_pairs,chunks):
    """
    Get the color for each vowel that is a member of a rhyme pair.
    """         
    colorids=[]
    
    for j in range(len(vowels)):
        l=[rhyme.color for rhyme in rhyme_pairs if rhyme.idx1==j or rhyme.idx2==j]
        if len(l)>0:
            colorids.append(l[0])
        else:
            colorids.append((255,255,255))
            
    return colorids 

def scheme(vowels,congrps_bv,chunks,colorids):
    """
    Prints the ARPA with rhyme colors assigned
    """
    
    for j in range(len(vowels)):
        print([congrps_bv[j].consonant_list[i].name for i in range(len(congrps_bv[j].consonant_list))],end=" ")
        print(bg(colorids[j][0],colorids[j][1],colorids[j][2]) +                 
        str([chunks[j].vowel.name]) +   
        str([chunks[j].congrp.consonant_list[i].name for i in range(len(chunks[j].congrp.consonant_list))])+ bg.rs,end=" ") 
        
#test print 
       
#vowels,consonants,vowel_words = get_components(line_arpas,arpa_words)
#congrps, congrps_bv, chunks = group_components(vowels,consonants,vowel_words)
#rhyme_pairs, alliteration_pairs = generate_goodness_pairs(congrps, congrps_bv, chunks,T1,T2,T3,T4)
#reconstruct_lyrics(vowels,congrps,congrps_bv,chunks,rhyme_pairs,alliteration_pairs)  
#colorids = color_rhymes(vowels,rhyme_pairs,chunks)
#scheme(vowels,congrps_bv,chunks,colorids)