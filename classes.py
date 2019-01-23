import math
from config import T1,T2,T3,T4

class Rhyme_pair:
    """
    A pair of rhyming chunks, according to specified rhyming thresholds.
    """
    def __init__(self,idx,chunk1,chunk2,rhyme_nums):
        self.idx=idx
        if chunk1.color==chunk2.color:
            self.color=chunk1.color
        else:
            self.color=chunk1.color #maybe make half rhymes grey (128,128,128)
        self.rhyme_nums=rhyme_nums  #the distance, allit score, and stress score for the rhyme pair
        self.idx1=chunk1.idx
        self.idx2=chunk2.idx 
        self.chunk1=chunk1
        self.chunk2=chunk2
        

class Alliteration_pair:
    """
    A pair of alliterating consonant groups, according to specified alliteration threshold.
    """
    def __init__(self,congrp1,congrp2,score):
        self.score=score
        self.idx1=congrp1.idx
        self.idx2=congrp2.idx
        self.color=congrp1.color
        self.congrp1=congrp1
    
    def get_color(self):
        return self.congrp1.get_color()

class Chunk:
    """
    A chunk consisting of a vowel and the consonant group which appears after it.
    """
    def __init__(self,vowel,congrp,idx): 
        self.vowel=vowel
        self.congrp=congrp
        self.color=vowel.color
        self.root_word=vowel.root_word
        self.name=vowel.name
        self.idx=idx
        self.vowel_idx=vowel.idx
        
    def __lt__(self,other): # allows sorting based on class attributes
        return self.idx < other.idx
    
    def compare_to_chunk(self,other_chunk): #USE FOR RHYME DETECTION
        """
        Look at how similar the vowels in each chunk are, and how similar the consonants in each chunks congrp is.
        These comparisons are compared to a threshold to decide if two chunks rhyme or not.
        """
        vowel_dist=self.vowel.distanceFromPoint(other_chunk.vowel)
        con_dist=self.congrp.compare_to_congrp(other_chunk.congrp)
        stress_dist=self.vowel.stressCompare(other_chunk.vowel)
        return vowel_dist, con_dist, stress_dist
         
class Con_grp:
    """
    A group of consonants, either occuring before (bv) or after a vowel.
    """
    def __init__(self,idx): 
        self.congrp_list=[]
        self.consonant_list=[]
        self.idx=idx
        self.color=(255,255,255)
    
    def __lt__(self,other): # allows sorting based on class attributes
        return self.idx < other.idx
        
    def add_consonant(self,consonant):
        self.consonant_list.append(consonant)
        return self.consonant_list
    
    def get_consonant(self,idx): 
        return self.consonant_list[idx]
    
    def get_color(self): 
        if len(self.consonant_list)>0:
            self.color=self.consonant_list[0].color
        else:
            self.color=(255,255,255)
        return self.color
    
    def compare_to_congrp(self,other_congrp): #USE FOR ALLITERATION DETECTION
        """
        The consonant similarities are calculated and compared to the alliteration threshold.
        """
        con_list=self.consonant_list
        other_list=other_congrp.consonant_list
        compar_list=[(n,m) for n in con_list for m in other_list]
        con_compars=[compar_list[i][0].distanceFromPoint(compar_list[i][1]) for i in range(len(compar_list))]
        
        if len(self.consonant_list)>0 or len(other_list)>0:
            if len(self.consonant_list)==0 or len(other_list)==0:
                score=3
            else:
                score=sum(con_compars)/max(len(self.consonant_list),len(other_list))#ensure that all the consonants score highly for similarity in congrp, avoids things like get and hemmed showing up as rhyme
        else:
            if len(other_list)==0: #if both lists are empty say they alliterate
                score=3
#            else:
#                score=0 #if one is empty and the other isn't then they can't alliterate  
        return score
        
class Consonant:
    """
    A single consonant object.
    """
    def __init__(self, idx, name, position, color, root_word): #name as in the representative arpabet symbol
        self.position = position
        self.name = name
        self.color= color
        self.root_word = root_word
        self.idx = idx #position in lyric
        
    def __lt__(self,other): # allows sorting based on class attributes
        return self.idx < other.idx
        
    def getX(self): #used only for shorthand 
        return self.position[0]

    def getY(self): #used only for shorthand 
        return self.position[1]    
        
    def getZ(self): #used only for shorthand 
        return self.position[2] 
        
    def distanceFromPoint(self, otherP):
        """
        Get the 'distance' from this consonant to an another, i.e. compare the coordinates 
        of each consonant as they lie in the consonant space defined by consonant_color_dict
        """
        score=0
        if otherP.getX()==self.position[0]:
            score+=1
            if otherP.getY()==self.position[1]:
                score+=1
                if otherP.getZ()==self.position[2]:
                    score+=1
        return score #Same group; score 1, same subgp; score 2, same consonant; score 3
    
class Vowel:
    """
    A single vowel object.
    """
    def __init__(self, idx, name, position, color, root_word, stress):
        self.position = position
        self.name = name
        self.color= color
        self.root_word = root_word
        self.idx = idx
        self.stress = stress
        
    def getX(self): #used only for shorthand
        return self.position[0]

    def getY(self): #used only for shorthand 
        return self.position[1]    
        
    def getZ(self): #used only for shorthand 
        return self.position[2] 
    
    def getStress(self): #used only for shorthand 
        return self.stress
        
    def distanceFromPoint(self, otherP):
        """
        Get the 'distance' from this vowel to an another, i.e. compare the coordinates 
        of each vowel as they lie in the vowel space defined by vowel_color_dict
        """
        dx = (otherP.getX() - self.position[0])
        dy = (otherP.getY() - self.position[1])
        dz = (otherP.getZ() - self.position[2])
        return math.sqrt(dz**2 + dy**2 + dx**2)
    
    def stressCompare(self, other):
        return abs(other.stress-self.stress), other.stress+self.stress #if the sum is zero, then we know both stresses are zero.
        
    