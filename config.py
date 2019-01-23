#the position coordinate here represents (backness,closeness,roundness) of the vowel
vowel_color_dict={'AA':[(0, 255, 0),(4,0,0)],   #make all unstressed vowels (0) grey? and if multiple pronunciations use the closest?
                  'AE':[(255, 214, 0),(0,1,0)],     
                  'AH':[(0, 174, 0),(4,2,0)],
                  'AO':[(0, 171, 255),(4,2,2)],
                  'AW':[(118, 170, 255),(1.5,2.5,1)],
                  'AX':[(128, 128, 128),(2,3,1)],
                  'AY':[(209, 136, 69),(0.5,2.5,0)],
                  'EH':[(255, 166, 0),(0,2,0)],
                  'ER':[(115, 173, 0),(2,2,0)],
                  'EY':[(255, 66, 0),(0,4,0)], #E62400 (0.5,4.5,0)
                  'IH':[(208, 12, 0),(1,5,0)],
                  'IX':[(140, 0, 0),(2,6,0)],
                  'IY':[(255, 0, 0),(0,6,0)],
                  'OW':[(51, 47, 255),(3.5,4.5,2)],
                  'OY':[(137, 76, 255),(2.5,3.5,1)],
                  'UH':[(73, 21, 255),(3,5,2)],
                  'UW':[(27, 0, 255),(4,6,2)],
                  'UX':[(143, 0, 255),(2,6,2)]}
 
#the position coordinate here represents (group,subgroup,idx in subgroup)                 
consonant_color_dict={'B':[(254, 255, 0),(1,1,0)], #if in group 1, get 1 pt, elif P, get 2pts, elif B, get 3pts, else get 0 pts
                      'P':[(254, 255, 0),(1,1,1)],
                      'D':[(254, 255, 0),(1,2,0)],
                      'T':[(254, 255, 0),(1,2,1)],
                      'G':[(254, 255, 0),(1,3,0)],
                      'K':[(254, 255, 0),(1,3,1)],
                      'F':[(0, 174, 0),(2,1,0)],
                      'V':[(0, 174, 0),(2,1,1)],
                      'S':[(0, 174, 0),(2,2,0)],
                      'Z':[(0, 174, 0),(2,2,1)],
                      'SH':[(0, 174, 0),(2,3,0)],
                      'TH':[(0, 174, 0),(2,3,1)],
                      'DH':[(0, 174, 0),(2,4,0)],
                      'HH':[(0, 174, 0),(2,4,1)],
                      'CH':[(115, 171, 0),(3,1,0)],
                      'JH':[(115, 171, 0),(3,1,1)],
                      'M':[(255, 163, 255),(4,1,1)],
                      'N':[(255, 163, 255),(4,1,2)],
                      'NG':[(255, 163, 255),(4,1,3)],
                      'W':[(0, 255, 255),(5,1,0)],
                      'Y':[(0, 255, 255),(5,2,0)],
                      'L':[(0, 255, 255),(5,3,0)],
                      'R':[(0, 255, 255),(5,4,0)]}
                           
T1=1 #Rhyme stressed vowel threshold, maximum vowel distance required to count as a rhyme
T2=0.5 #Rhyme stressed vowel consonance threshold, minimum consonance score to count as a rhyme
T3=4 #Rhyme unstressed vowel threshold
T4=1 #Rhyme unstressed vowel consonance threshold
T5=1 #Alliteration threshold
