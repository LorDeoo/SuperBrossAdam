
#Création des 4 niveaux et définition des dimensions de la fenêtre
level_map = [   
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                            RRRR        ',
'                     O                  ',
'         XXXX      XXXX                 ',   
'                  XX                    ',
'                 XXX     T       O    D ', 
'GGGGXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXX']

level_map2 = [   
'                                                                                                               X     ',
'                                                                                                              RX     ',
'                                                                                                               X     ',
'                                                 O                                                       R     X     ',
'                       O   O                   XXXX         O             O                                    XR    ',
'                      XXXXXXRRRXXXXX                      XXXX         XXXXX         XRXX                     RX     ',   
'                  O            XX  XXX        RRRRR      RXX                                       P           XR    ',
'     XXX          X            X    XXXT                  XX  R               H                 XXXXXX         X     ', 
'                 XX           X      XXX     O            XX                                                  XXX    ',
'                XXXX       P X        XXX    X   PX    P XX        OX  OX    P   X  OX  OXP            P X   PXXXXX D ',
'GGGGGGGXXXXXXXXXXXXXXXXXXXXXX          XXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXGGGXXXXXXXX']






level_map3 = [   
'                                                                                                                            ',
'                          O                                                                                              D  ',
'                    XXXXXXX                                  C                   C                             XXXXXXXXXXX  ',
'                                                   X       P X               A                                 C            ',
'                      O                            XXXXXXXXXXXX                     C                   H   A               ',
'                    XXXXXXX                        C                      C                                    C            ',
'                     C                          A  X              H      A        H                          C              ',
'                X    X            C      H                                                                 C                ',   
'                                  X                                                             C     A                     ',
'           H                 A                C                                                                             ', 
'XXXXXXXXX                           A         X                                            XX   H                           ']

level_map4 = [   
'                  XXXXXXXXXXXXXXXXXXXX',
'                  X                  X',
'                  X                  X',
'                  X                  X',
'                  X                  X',
'                  X         RR       X',
'                  X                  X',
'                  XXXX            XXXX',   
'                              B     XX',
'                                    XX     D      ', 
'GGGGGGGGGGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']



block_size = 50
screen_width = 1200
screen_height = len(level_map) * block_size