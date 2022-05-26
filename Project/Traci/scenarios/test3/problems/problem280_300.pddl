(define
(problem problem280_300)
(:domain utc)
(:objects
v431 v444 v1203 v450 v1222 v1223 v436 v1214 v445 v451 v776 v779 v790 v1220 v1226 v1227 v1221 v1230 v1237 v447 v781 v432 v777 v782 v783 v791 v429 v430 v775 v1212 v1228 v435 v437 v446 v449 v772 v774 v785 v773 v789 v1217 v1224 v434 v443 v455 v769 v778 v438 v454 v766 v770 v1233 v433 v441 v1231 v453 v456 v767 v1219 v1235 v771 v1216 v1232 v784 v1225 v440 v787 v442 v768 v780 v1229 v1234 v448 v786 v1236 v452 v457 v788 v1211 v439 v1213 v1215 v1218 - car
use0 use1 use2 use3 use4 use5 use6 use7 use8 use9 use10 use11 use12 use13 use14 use15 use16 use17 use18 use19 use20 use21 use22 use23 use24 use25 use26 use27 use28 use29 use30 use31 use32 use33 use34 use35 use36 use37 use38 use39 use40 use41 use42 use43 use44 use45 use46 use47 use48 use49 use50 use51 use52 use53 use54 use55 use56 use57 use58 use59 use60 use61 use62 use63 use64 use65 use66 use67 use68 use69 use70 use71 use72 use73 use74 use75 use76 use77 use78 use79 use80 use81 use82 use83 use84 use85 use86 use87 use88 use89 use90 use91 use92 use93 use94 use95 use96 use97 use98 use99 use100 use101 use102 use103 use104 use105 use106 use107 use108 use109 use110 use111 use112 use113 use114 use115 use116 use117 - use
j0 j23 j3 j33 j37 j38 j39 j40 j41 j42 j43 j44 j45 j46 j47 j48 j49 j50 j51 j52 j54 j64 j65 j77 j8 j84 j88 j91 j93 j94 - junction
r8 r9 r10 r12 r13 r15 r16 r17 r18 r19 r20 r21 r22 r23 r24 r25 r26 r27 r28 r29 r31 r32 r33 r34 r35 r37 r38 r39 r40 r41 r42 r43 r44 r45 r46 r47 r48 r49 r50 r51 r52 r53 r54 r55 r56 r57 r58 r59 r61 r63 r64 r65 r66 r67 r68 r69 r70 r71 - road
)
(:init
(= (total-cost) 0)
(connected j23 r8 j47)
(connected j46 r9 j42)
(connected j77 r10 j94)
(connected j84 r12 j65)
(connected j65 r13 j64)
(connected j23 r15 j88)
(connected j88 r16 j50)
(connected j50 r17 j8)
(connected j8 r18 j84)
(connected j39 r19 j93)
(connected j45 r20 j23)
(connected j3 r21 j8)
(connected j49 r22 j50)
(connected j93 r23 j49)
(connected j88 r24 j91)
(connected j44 r25 j46)
(connected j46 r26 j33)
(connected j43 r27 j51)
(connected j41 r28 j54)
(connected j54 r29 j52)
(connected j52 r31 j49)
(connected j48 r32 j51)
(connected j51 r33 j54)
(connected j52 r34 j38)
(connected j38 r35 j40)
(connected j64 r37 j39)
(connected j39 r38 j40)
(connected j93 r39 j40)
(connected j23 r40 j45)
(connected j88 r41 j23)
(connected j84 r42 j93)
(connected j50 r43 j88)
(connected j8 r44 j50)
(connected j84 r45 j8)
(connected j94 r46 j45)
(connected j93 r47 j39)
(connected j50 r48 j49)
(connected j49 r49 j93)
(connected j51 r50 j43)
(connected j49 r51 j52)
(connected j42 r52 j41)
(connected j40 r53 j38)
(connected j65 r54 j64)
(connected j43 r55 j42)
(connected j38 r56 j0)
(connected j49 r57 j48)
(connected j48 r58 j47)
(connected j47 r59 j44)
(connected j44 r61 j43)
(connected j40 r63 j93)
(connected j93 r64 j84)
(connected j37 r65 j41)
(connected j41 r66 j42)
(connected j42 r67 j43)
(connected j43 r68 j44)
(connected j44 r69 j45)
(connected j45 r70 j44)
(connected j94 r71 j84)
(= (length-light r8) 5)
(= (length-medium r8) 53)
(= (length-heavy r8) 539)
(light r8 use0)
(light r8 use1)
(light r8 use2)
(light r8 use3)
(light r8 use4)
(medium r8 use5)
(medium r8 use6)
(medium r8 use7)
(medium r8 use8)
(heavy r8 use9)
(heavy r8 use10)
(cap r8 use10)
(using r8 use0)
(= (length-light r9) 11)
(= (length-medium r9) 119)
(= (length-heavy r9) 1198)
(light r9 use0)
(light r9 use1)
(light r9 use2)
(light r9 use3)
(light r9 use4)
(light r9 use5)
(light r9 use6)
(light r9 use7)
(light r9 use8)
(medium r9 use9)
(medium r9 use10)
(medium r9 use11)
(medium r9 use12)
(medium r9 use13)
(medium r9 use14)
(medium r9 use15)
(medium r9 use16)
(medium r9 use17)
(heavy r9 use18)
(heavy r9 use19)
(heavy r9 use20)
(heavy r9 use21)
(heavy r9 use22)
(heavy r9 use23)
(cap r9 use23)
(using r9 use0)
(= (length-light r10) 9)
(= (length-medium r10) 99)
(= (length-heavy r10) 997)
(light r10 use0)
(light r10 use1)
(light r10 use2)
(light r10 use3)
(light r10 use4)
(light r10 use5)
(light r10 use6)
(light r10 use7)
(light r10 use8)
(light r10 use9)
(light r10 use10)
(light r10 use11)
(light r10 use12)
(light r10 use13)
(medium r10 use14)
(medium r10 use15)
(medium r10 use16)
(medium r10 use17)
(medium r10 use18)
(medium r10 use19)
(medium r10 use20)
(medium r10 use21)
(medium r10 use22)
(medium r10 use23)
(medium r10 use24)
(medium r10 use25)
(medium r10 use26)
(medium r10 use27)
(medium r10 use28)
(heavy r10 use29)
(heavy r10 use30)
(heavy r10 use31)
(heavy r10 use32)
(heavy r10 use33)
(heavy r10 use34)
(heavy r10 use35)
(heavy r10 use36)
(heavy r10 use37)
(heavy r10 use38)
(cap r10 use38)
(using r10 use0)
(= (length-light r12) 6)
(= (length-medium r12) 60)
(= (length-heavy r12) 601)
(light r12 use0)
(light r12 use1)
(light r12 use2)
(light r12 use3)
(light r12 use4)
(medium r12 use5)
(medium r12 use6)
(medium r12 use7)
(medium r12 use8)
(heavy r12 use9)
(heavy r12 use10)
(heavy r12 use11)
(cap r12 use11)
(using r12 use0)
(= (length-light r13) 19)
(= (length-medium r13) 190)
(= (length-heavy r13) 1901)
(light r13 use0)
(light r13 use1)
(light r13 use2)
(light r13 use3)
(light r13 use4)
(light r13 use5)
(light r13 use6)
(light r13 use7)
(light r13 use8)
(light r13 use9)
(light r13 use10)
(light r13 use11)
(light r13 use12)
(light r13 use13)
(medium r13 use14)
(medium r13 use15)
(medium r13 use16)
(medium r13 use17)
(medium r13 use18)
(medium r13 use19)
(medium r13 use20)
(medium r13 use21)
(medium r13 use22)
(medium r13 use23)
(medium r13 use24)
(medium r13 use25)
(medium r13 use26)
(medium r13 use27)
(medium r13 use28)
(heavy r13 use29)
(heavy r13 use30)
(heavy r13 use31)
(heavy r13 use32)
(heavy r13 use33)
(heavy r13 use34)
(heavy r13 use35)
(heavy r13 use36)
(heavy r13 use37)
(cap r13 use37)
(using r13 use0)
(= (length-light r15) 2)
(= (length-medium r15) 29)
(= (length-heavy r15) 299)
(light r15 use0)
(light r15 use1)
(light r15 use2)
(medium r15 use3)
(medium r15 use4)
(heavy r15 use5)
(cap r15 use5)
(using r15 use0)
(= (length-light r16) 2)
(= (length-medium r16) 28)
(= (length-heavy r16) 285)
(light r16 use0)
(light r16 use1)
(light r16 use2)
(medium r16 use3)
(medium r16 use4)
(heavy r16 use5)
(cap r16 use5)
(using r16 use0)
(= (length-light r17) 1)
(= (length-medium r17) 14)
(= (length-heavy r17) 140)
(light r17 use0)
(light r17 use1)
(medium r17 use2)
(cap r17 use2)
(using r17 use0)
(= (length-light r18) 7)
(= (length-medium r18) 76)
(= (length-heavy r18) 764)
(light r18 use0)
(light r18 use1)
(light r18 use2)
(light r18 use3)
(light r18 use4)
(light r18 use5)
(medium r18 use6)
(medium r18 use7)
(medium r18 use8)
(medium r18 use9)
(medium r18 use10)
(medium r18 use11)
(heavy r18 use12)
(heavy r18 use13)
(heavy r18 use14)
(heavy r18 use15)
(cap r18 use15)
(using r18 use0)
(= (length-light r19) 8)
(= (length-medium r19) 83)
(= (length-heavy r19) 832)
(light r19 use0)
(light r19 use1)
(light r19 use2)
(light r19 use3)
(light r19 use4)
(light r19 use5)
(light r19 use6)
(medium r19 use7)
(medium r19 use8)
(medium r19 use9)
(medium r19 use10)
(medium r19 use11)
(medium r19 use12)
(heavy r19 use13)
(heavy r19 use14)
(heavy r19 use15)
(heavy r19 use16)
(cap r19 use16)
(using r19 use0)
(= (length-light r20) 9)
(= (length-medium r20) 91)
(= (length-heavy r20) 913)
(light r20 use0)
(light r20 use1)
(light r20 use2)
(light r20 use3)
(light r20 use4)
(light r20 use5)
(light r20 use6)
(medium r20 use7)
(medium r20 use8)
(medium r20 use9)
(medium r20 use10)
(medium r20 use11)
(medium r20 use12)
(medium r20 use13)
(heavy r20 use14)
(heavy r20 use15)
(heavy r20 use16)
(heavy r20 use17)
(heavy r20 use18)
(cap r20 use18)
(using r20 use0)
(= (length-light r21) 9)
(= (length-medium r21) 91)
(= (length-heavy r21) 916)
(light r21 use0)
(light r21 use1)
(light r21 use2)
(light r21 use3)
(light r21 use4)
(light r21 use5)
(light r21 use6)
(medium r21 use7)
(medium r21 use8)
(medium r21 use9)
(medium r21 use10)
(medium r21 use11)
(medium r21 use12)
(medium r21 use13)
(heavy r21 use14)
(heavy r21 use15)
(heavy r21 use16)
(heavy r21 use17)
(heavy r21 use18)
(cap r21 use18)
(using r21 use0)
(= (length-light r22) 5)
(= (length-medium r22) 56)
(= (length-heavy r22) 562)
(light r22 use0)
(light r22 use1)
(light r22 use2)
(light r22 use3)
(light r22 use4)
(medium r22 use5)
(medium r22 use6)
(medium r22 use7)
(medium r22 use8)
(heavy r22 use9)
(heavy r22 use10)
(heavy r22 use11)
(cap r22 use11)
(using r22 use0)
(= (length-light r23) 12)
(= (length-medium r23) 126)
(= (length-heavy r23) 1262)
(light r23 use0)
(light r23 use1)
(light r23 use2)
(light r23 use3)
(light r23 use4)
(light r23 use5)
(light r23 use6)
(light r23 use7)
(light r23 use8)
(light r23 use9)
(medium r23 use10)
(medium r23 use11)
(medium r23 use12)
(medium r23 use13)
(medium r23 use14)
(medium r23 use15)
(medium r23 use16)
(medium r23 use17)
(medium r23 use18)
(medium r23 use19)
(heavy r23 use20)
(heavy r23 use21)
(heavy r23 use22)
(heavy r23 use23)
(heavy r23 use24)
(heavy r23 use25)
(cap r23 use25)
(using r23 use0)
(= (length-light r24) 20)
(= (length-medium r24) 209)
(= (length-heavy r24) 2095)
(light r24 use0)
(light r24 use1)
(light r24 use2)
(light r24 use3)
(light r24 use4)
(light r24 use5)
(light r24 use6)
(light r24 use7)
(light r24 use8)
(light r24 use9)
(light r24 use10)
(light r24 use11)
(light r24 use12)
(light r24 use13)
(light r24 use14)
(medium r24 use15)
(medium r24 use16)
(medium r24 use17)
(medium r24 use18)
(medium r24 use19)
(medium r24 use20)
(medium r24 use21)
(medium r24 use22)
(medium r24 use23)
(medium r24 use24)
(medium r24 use25)
(medium r24 use26)
(medium r24 use27)
(medium r24 use28)
(medium r24 use29)
(medium r24 use30)
(heavy r24 use31)
(heavy r24 use32)
(heavy r24 use33)
(heavy r24 use34)
(heavy r24 use35)
(heavy r24 use36)
(heavy r24 use37)
(heavy r24 use38)
(heavy r24 use39)
(heavy r24 use40)
(heavy r24 use41)
(cap r24 use41)
(using r24 use0)
(= (length-light r25) 4)
(= (length-medium r25) 44)
(= (length-heavy r25) 443)
(light r25 use0)
(light r25 use1)
(light r25 use2)
(light r25 use3)
(medium r25 use4)
(medium r25 use5)
(medium r25 use6)
(heavy r25 use7)
(heavy r25 use8)
(cap r25 use8)
(using r25 use0)
(= (length-light r26) 5)
(= (length-medium r26) 57)
(= (length-heavy r26) 575)
(light r26 use0)
(light r26 use1)
(light r26 use2)
(light r26 use3)
(light r26 use4)
(medium r26 use5)
(medium r26 use6)
(medium r26 use7)
(medium r26 use8)
(heavy r26 use9)
(heavy r26 use10)
(heavy r26 use11)
(cap r26 use11)
(using r26 use0)
(= (length-light r27) 13)
(= (length-medium r27) 139)
(= (length-heavy r27) 1398)
(light r27 use0)
(light r27 use1)
(light r27 use2)
(light r27 use3)
(light r27 use4)
(light r27 use5)
(light r27 use6)
(light r27 use7)
(light r27 use8)
(light r27 use9)
(medium r27 use10)
(medium r27 use11)
(medium r27 use12)
(medium r27 use13)
(medium r27 use14)
(medium r27 use15)
(medium r27 use16)
(medium r27 use17)
(medium r27 use18)
(medium r27 use19)
(medium r27 use20)
(heavy r27 use21)
(heavy r27 use22)
(heavy r27 use23)
(heavy r27 use24)
(heavy r27 use25)
(heavy r27 use26)
(heavy r27 use27)
(cap r27 use27)
(using r27 use0)
(= (length-light r28) 15)
(= (length-medium r28) 155)
(= (length-heavy r28) 1550)
(light r28 use0)
(light r28 use1)
(light r28 use2)
(light r28 use3)
(light r28 use4)
(light r28 use5)
(light r28 use6)
(light r28 use7)
(light r28 use8)
(light r28 use9)
(light r28 use10)
(medium r28 use11)
(medium r28 use12)
(medium r28 use13)
(medium r28 use14)
(medium r28 use15)
(medium r28 use16)
(medium r28 use17)
(medium r28 use18)
(medium r28 use19)
(medium r28 use20)
(medium r28 use21)
(medium r28 use22)
(heavy r28 use23)
(heavy r28 use24)
(heavy r28 use25)
(heavy r28 use26)
(heavy r28 use27)
(heavy r28 use28)
(heavy r28 use29)
(heavy r28 use30)
(cap r28 use30)
(using r28 use0)
(= (length-light r29) 7)
(= (length-medium r29) 74)
(= (length-heavy r29) 741)
(light r29 use0)
(light r29 use1)
(light r29 use2)
(light r29 use3)
(light r29 use4)
(light r29 use5)
(medium r29 use6)
(medium r29 use7)
(medium r29 use8)
(medium r29 use9)
(medium r29 use10)
(medium r29 use11)
(heavy r29 use12)
(heavy r29 use13)
(heavy r29 use14)
(cap r29 use14)
(using r29 use0)
(= (length-light r31) 4)
(= (length-medium r31) 46)
(= (length-heavy r31) 461)
(light r31 use0)
(light r31 use1)
(light r31 use2)
(light r31 use3)
(medium r31 use4)
(medium r31 use5)
(medium r31 use6)
(medium r31 use7)
(heavy r31 use8)
(heavy r31 use9)
(cap r31 use9)
(using r31 use0)
(= (length-light r32) 5)
(= (length-medium r32) 52)
(= (length-heavy r32) 522)
(light r32 use0)
(light r32 use1)
(light r32 use2)
(light r32 use3)
(light r32 use4)
(medium r32 use5)
(medium r32 use6)
(medium r32 use7)
(medium r32 use8)
(heavy r32 use9)
(heavy r32 use10)
(cap r32 use10)
(using r32 use0)
(= (length-light r33) 4)
(= (length-medium r33) 48)
(= (length-heavy r33) 484)
(light r33 use0)
(light r33 use1)
(light r33 use2)
(light r33 use3)
(medium r33 use4)
(medium r33 use5)
(medium r33 use6)
(medium r33 use7)
(heavy r33 use8)
(heavy r33 use9)
(cap r33 use9)
(using r33 use0)
(= (length-light r34) 10)
(= (length-medium r34) 102)
(= (length-heavy r34) 1026)
(light r34 use0)
(light r34 use1)
(light r34 use2)
(light r34 use3)
(light r34 use4)
(light r34 use5)
(light r34 use6)
(light r34 use7)
(medium r34 use8)
(medium r34 use9)
(medium r34 use10)
(medium r34 use11)
(medium r34 use12)
(medium r34 use13)
(medium r34 use14)
(medium r34 use15)
(heavy r34 use16)
(heavy r34 use17)
(heavy r34 use18)
(heavy r34 use19)
(heavy r34 use20)
(cap r34 use20)
(using r34 use0)
(= (length-light r35) 3)
(= (length-medium r35) 38)
(= (length-heavy r35) 385)
(light r35 use0)
(light r35 use1)
(light r35 use2)
(medium r35 use3)
(medium r35 use4)
(medium r35 use5)
(heavy r35 use6)
(heavy r35 use7)
(cap r35 use7)
(using r35 use0)
(= (length-light r37) 6)
(= (length-medium r37) 61)
(= (length-heavy r37) 619)
(light r37 use0)
(light r37 use1)
(light r37 use2)
(light r37 use3)
(light r37 use4)
(medium r37 use5)
(medium r37 use6)
(medium r37 use7)
(medium r37 use8)
(medium r37 use9)
(heavy r37 use10)
(heavy r37 use11)
(heavy r37 use12)
(cap r37 use12)
(using r37 use0)
(= (length-light r38) 12)
(= (length-medium r38) 121)
(= (length-heavy r38) 1218)
(light r38 use0)
(light r38 use1)
(light r38 use2)
(light r38 use3)
(light r38 use4)
(light r38 use5)
(light r38 use6)
(light r38 use7)
(medium r38 use8)
(medium r38 use9)
(medium r38 use10)
(medium r38 use11)
(medium r38 use12)
(medium r38 use13)
(medium r38 use14)
(medium r38 use15)
(heavy r38 use16)
(heavy r38 use17)
(heavy r38 use18)
(heavy r38 use19)
(cap r38 use19)
(using r38 use0)
(= (length-light r39) 8)
(= (length-medium r39) 85)
(= (length-heavy r39) 856)
(light r39 use0)
(light r39 use1)
(light r39 use2)
(light r39 use3)
(light r39 use4)
(medium r39 use5)
(medium r39 use6)
(medium r39 use7)
(medium r39 use8)
(heavy r39 use9)
(heavy r39 use10)
(cap r39 use10)
(using r39 use0)
(= (length-light r40) 9)
(= (length-medium r40) 91)
(= (length-heavy r40) 913)
(light r40 use0)
(light r40 use1)
(light r40 use2)
(light r40 use3)
(light r40 use4)
(light r40 use5)
(light r40 use6)
(medium r40 use7)
(medium r40 use8)
(medium r40 use9)
(medium r40 use10)
(medium r40 use11)
(medium r40 use12)
(medium r40 use13)
(heavy r40 use14)
(heavy r40 use15)
(heavy r40 use16)
(heavy r40 use17)
(heavy r40 use18)
(cap r40 use18)
(using r40 use0)
(= (length-light r41) 3)
(= (length-medium r41) 30)
(= (length-heavy r41) 301)
(light r41 use0)
(light r41 use1)
(light r41 use2)
(medium r41 use3)
(medium r41 use4)
(heavy r41 use5)
(cap r41 use5)
(using r41 use0)
(= (length-light r42) 7)
(= (length-medium r42) 70)
(= (length-heavy r42) 709)
(light r42 use0)
(light r42 use1)
(light r42 use2)
(light r42 use3)
(medium r42 use4)
(medium r42 use5)
(medium r42 use6)
(heavy r42 use7)
(heavy r42 use8)
(cap r42 use8)
(using r42 use0)
(= (length-light r43) 2)
(= (length-medium r43) 28)
(= (length-heavy r43) 284)
(light r43 use0)
(light r43 use1)
(light r43 use2)
(medium r43 use3)
(medium r43 use4)
(heavy r43 use5)
(cap r43 use5)
(using r43 use0)
(= (length-light r44) 1)
(= (length-medium r44) 14)
(= (length-heavy r44) 140)
(light r44 use0)
(light r44 use1)
(medium r44 use2)
(cap r44 use2)
(using r44 use0)
(= (length-light r45) 7)
(= (length-medium r45) 76)
(= (length-heavy r45) 768)
(light r45 use0)
(light r45 use1)
(light r45 use2)
(light r45 use3)
(light r45 use4)
(light r45 use5)
(medium r45 use6)
(medium r45 use7)
(medium r45 use8)
(medium r45 use9)
(medium r45 use10)
(medium r45 use11)
(heavy r45 use12)
(heavy r45 use13)
(heavy r45 use14)
(heavy r45 use15)
(cap r45 use15)
(using r45 use0)
(= (length-light r46) 6)
(= (length-medium r46) 63)
(= (length-heavy r46) 632)
(light r46 use0)
(light r46 use1)
(light r46 use2)
(light r46 use3)
(light r46 use4)
(medium r46 use5)
(medium r46 use6)
(medium r46 use7)
(medium r46 use8)
(medium r46 use9)
(heavy r46 use10)
(heavy r46 use11)
(heavy r46 use12)
(cap r46 use12)
(using r46 use0)
(= (length-light r47) 8)
(= (length-medium r47) 84)
(= (length-heavy r47) 843)
(light r47 use0)
(light r47 use1)
(light r47 use2)
(light r47 use3)
(light r47 use4)
(light r47 use5)
(light r47 use6)
(medium r47 use7)
(medium r47 use8)
(medium r47 use9)
(medium r47 use10)
(medium r47 use11)
(medium r47 use12)
(heavy r47 use13)
(heavy r47 use14)
(heavy r47 use15)
(heavy r47 use16)
(cap r47 use16)
(using r47 use0)
(= (length-light r48) 5)
(= (length-medium r48) 56)
(= (length-heavy r48) 561)
(light r48 use0)
(light r48 use1)
(light r48 use2)
(light r48 use3)
(light r48 use4)
(medium r48 use5)
(medium r48 use6)
(medium r48 use7)
(medium r48 use8)
(heavy r48 use9)
(heavy r48 use10)
(heavy r48 use11)
(cap r48 use11)
(using r48 use0)
(= (length-light r49) 12)
(= (length-medium r49) 126)
(= (length-heavy r49) 1265)
(light r49 use0)
(light r49 use1)
(light r49 use2)
(light r49 use3)
(light r49 use4)
(light r49 use5)
(light r49 use6)
(light r49 use7)
(light r49 use8)
(light r49 use9)
(medium r49 use10)
(medium r49 use11)
(medium r49 use12)
(medium r49 use13)
(medium r49 use14)
(medium r49 use15)
(medium r49 use16)
(medium r49 use17)
(medium r49 use18)
(medium r49 use19)
(heavy r49 use20)
(heavy r49 use21)
(heavy r49 use22)
(heavy r49 use23)
(heavy r49 use24)
(heavy r49 use25)
(cap r49 use25)
(using r49 use0)
(= (length-light r50) 14)
(= (length-medium r50) 140)
(= (length-heavy r50) 1401)
(light r50 use0)
(light r50 use1)
(light r50 use2)
(light r50 use3)
(light r50 use4)
(light r50 use5)
(light r50 use6)
(light r50 use7)
(light r50 use8)
(light r50 use9)
(medium r50 use10)
(medium r50 use11)
(medium r50 use12)
(medium r50 use13)
(medium r50 use14)
(medium r50 use15)
(medium r50 use16)
(medium r50 use17)
(medium r50 use18)
(medium r50 use19)
(medium r50 use20)
(heavy r50 use21)
(heavy r50 use22)
(heavy r50 use23)
(heavy r50 use24)
(heavy r50 use25)
(heavy r50 use26)
(heavy r50 use27)
(cap r50 use27)
(using r50 use0)
(= (length-light r51) 4)
(= (length-medium r51) 46)
(= (length-heavy r51) 461)
(light r51 use0)
(light r51 use1)
(light r51 use2)
(light r51 use3)
(medium r51 use4)
(medium r51 use5)
(medium r51 use6)
(medium r51 use7)
(heavy r51 use8)
(heavy r51 use9)
(cap r51 use9)
(using r51 use0)
(= (length-light r52) 4)
(= (length-medium r52) 42)
(= (length-heavy r52) 429)
(light r52 use0)
(light r52 use1)
(light r52 use2)
(light r52 use3)
(medium r52 use4)
(medium r52 use5)
(medium r52 use6)
(heavy r52 use7)
(heavy r52 use8)
(cap r52 use8)
(using r52 use0)
(= (length-light r53) 3)
(= (length-medium r53) 38)
(= (length-heavy r53) 381)
(light r53 use0)
(light r53 use1)
(light r53 use2)
(medium r53 use3)
(medium r53 use4)
(medium r53 use5)
(heavy r53 use6)
(heavy r53 use7)
(cap r53 use7)
(using r53 use0)
(= (length-light r54) 7)
(= (length-medium r54) 78)
(= (length-heavy r54) 786)
(light r54 use0)
(light r54 use1)
(light r54 use2)
(light r54 use3)
(light r54 use4)
(light r54 use5)
(medium r54 use6)
(medium r54 use7)
(medium r54 use8)
(medium r54 use9)
(medium r54 use10)
(medium r54 use11)
(heavy r54 use12)
(heavy r54 use13)
(heavy r54 use14)
(heavy r54 use15)
(cap r54 use15)
(using r54 use0)
(= (length-light r55) 2)
(= (length-medium r55) 20)
(= (length-heavy r55) 200)
(light r55 use0)
(light r55 use1)
(medium r55 use2)
(heavy r55 use3)
(cap r55 use3)
(using r55 use0)
(= (length-light r56) 8)
(= (length-medium r56) 88)
(= (length-heavy r56) 882)
(light r56 use0)
(light r56 use1)
(light r56 use2)
(light r56 use3)
(light r56 use4)
(light r56 use5)
(light r56 use6)
(medium r56 use7)
(medium r56 use8)
(medium r56 use9)
(medium r56 use10)
(medium r56 use11)
(medium r56 use12)
(medium r56 use13)
(heavy r56 use14)
(heavy r56 use15)
(heavy r56 use16)
(heavy r56 use17)
(cap r56 use17)
(using r56 use0)
(= (length-light r57) 1)
(= (length-medium r57) 17)
(= (length-heavy r57) 175)
(light r57 use0)
(light r57 use1)
(medium r57 use2)
(heavy r57 use3)
(cap r57 use3)
(using r57 use0)
(= (length-light r58) 3)
(= (length-medium r58) 39)
(= (length-heavy r58) 393)
(light r58 use0)
(light r58 use1)
(light r58 use2)
(medium r58 use3)
(medium r58 use4)
(medium r58 use5)
(heavy r58 use6)
(heavy r58 use7)
(cap r58 use7)
(using r58 use0)
(= (length-light r59) 8)
(= (length-medium r59) 89)
(= (length-heavy r59) 891)
(light r59 use0)
(light r59 use1)
(light r59 use2)
(light r59 use3)
(light r59 use4)
(light r59 use5)
(light r59 use6)
(medium r59 use7)
(medium r59 use8)
(medium r59 use9)
(medium r59 use10)
(medium r59 use11)
(medium r59 use12)
(medium r59 use13)
(heavy r59 use14)
(heavy r59 use15)
(heavy r59 use16)
(heavy r59 use17)
(cap r59 use17)
(using r59 use0)
(= (length-light r61) 5)
(= (length-medium r61) 52)
(= (length-heavy r61) 529)
(light r61 use0)
(light r61 use1)
(light r61 use2)
(light r61 use3)
(light r61 use4)
(medium r61 use5)
(medium r61 use6)
(medium r61 use7)
(medium r61 use8)
(heavy r61 use9)
(heavy r61 use10)
(cap r61 use10)
(using r61 use0)
(= (length-light r63) 8)
(= (length-medium r63) 85)
(= (length-heavy r63) 858)
(light r63 use0)
(light r63 use1)
(light r63 use2)
(light r63 use3)
(light r63 use4)
(medium r63 use5)
(medium r63 use6)
(medium r63 use7)
(medium r63 use8)
(heavy r63 use9)
(heavy r63 use10)
(cap r63 use10)
(using r63 use0)
(= (length-light r64) 7)
(= (length-medium r64) 70)
(= (length-heavy r64) 709)
(light r64 use0)
(light r64 use1)
(light r64 use2)
(light r64 use3)
(medium r64 use4)
(medium r64 use5)
(medium r64 use6)
(heavy r64 use7)
(heavy r64 use8)
(cap r64 use8)
(using r64 use0)
(= (length-light r65) 19)
(= (length-medium r65) 193)
(= (length-heavy r65) 1938)
(light r65 use0)
(light r65 use1)
(light r65 use2)
(light r65 use3)
(light r65 use4)
(light r65 use5)
(light r65 use6)
(light r65 use7)
(light r65 use8)
(light r65 use9)
(light r65 use10)
(light r65 use11)
(light r65 use12)
(light r65 use13)
(medium r65 use14)
(medium r65 use15)
(medium r65 use16)
(medium r65 use17)
(medium r65 use18)
(medium r65 use19)
(medium r65 use20)
(medium r65 use21)
(medium r65 use22)
(medium r65 use23)
(medium r65 use24)
(medium r65 use25)
(medium r65 use26)
(medium r65 use27)
(medium r65 use28)
(heavy r65 use29)
(heavy r65 use30)
(heavy r65 use31)
(heavy r65 use32)
(heavy r65 use33)
(heavy r65 use34)
(heavy r65 use35)
(heavy r65 use36)
(heavy r65 use37)
(heavy r65 use38)
(cap r65 use38)
(using r65 use0)
(= (length-light r66) 4)
(= (length-medium r66) 43)
(= (length-heavy r66) 433)
(light r66 use0)
(light r66 use1)
(light r66 use2)
(light r66 use3)
(medium r66 use4)
(medium r66 use5)
(medium r66 use6)
(heavy r66 use7)
(heavy r66 use8)
(cap r66 use8)
(using r66 use0)
(= (length-light r67) 2)
(= (length-medium r67) 20)
(= (length-heavy r67) 200)
(light r67 use0)
(light r67 use1)
(medium r67 use2)
(heavy r67 use3)
(cap r67 use3)
(using r67 use0)
(= (length-light r68) 5)
(= (length-medium r68) 52)
(= (length-heavy r68) 529)
(light r68 use0)
(light r68 use1)
(light r68 use2)
(light r68 use3)
(light r68 use4)
(medium r68 use5)
(medium r68 use6)
(medium r68 use7)
(medium r68 use8)
(heavy r68 use9)
(heavy r68 use10)
(cap r68 use10)
(using r68 use0)
(= (length-light r69) 5)
(= (length-medium r69) 52)
(= (length-heavy r69) 521)
(light r69 use0)
(light r69 use1)
(light r69 use2)
(light r69 use3)
(light r69 use4)
(medium r69 use5)
(medium r69 use6)
(medium r69 use7)
(medium r69 use8)
(heavy r69 use9)
(heavy r69 use10)
(cap r69 use10)
(using r69 use0)
(= (length-light r70) 5)
(= (length-medium r70) 52)
(= (length-heavy r70) 521)
(light r70 use0)
(light r70 use1)
(light r70 use2)
(light r70 use3)
(light r70 use4)
(medium r70 use5)
(medium r70 use6)
(medium r70 use7)
(medium r70 use8)
(heavy r70 use9)
(heavy r70 use10)
(cap r70 use10)
(using r70 use0)
(= (length-light r71) 59)
(= (length-medium r71) 590)
(= (length-heavy r71) 5906)
(light r71 use0)
(light r71 use1)
(light r71 use2)
(light r71 use3)
(light r71 use4)
(light r71 use5)
(light r71 use6)
(light r71 use7)
(light r71 use8)
(light r71 use9)
(light r71 use10)
(light r71 use11)
(light r71 use12)
(light r71 use13)
(light r71 use14)
(light r71 use15)
(light r71 use16)
(light r71 use17)
(light r71 use18)
(light r71 use19)
(light r71 use20)
(light r71 use21)
(light r71 use22)
(light r71 use23)
(light r71 use24)
(light r71 use25)
(light r71 use26)
(light r71 use27)
(light r71 use28)
(light r71 use29)
(light r71 use30)
(light r71 use31)
(light r71 use32)
(light r71 use33)
(light r71 use34)
(light r71 use35)
(light r71 use36)
(light r71 use37)
(light r71 use38)
(light r71 use39)
(light r71 use40)
(light r71 use41)
(medium r71 use42)
(medium r71 use43)
(medium r71 use44)
(medium r71 use45)
(medium r71 use46)
(medium r71 use47)
(medium r71 use48)
(medium r71 use49)
(medium r71 use50)
(medium r71 use51)
(medium r71 use52)
(medium r71 use53)
(medium r71 use54)
(medium r71 use55)
(medium r71 use56)
(medium r71 use57)
(medium r71 use58)
(medium r71 use59)
(medium r71 use60)
(medium r71 use61)
(medium r71 use62)
(medium r71 use63)
(medium r71 use64)
(medium r71 use65)
(medium r71 use66)
(medium r71 use67)
(medium r71 use68)
(medium r71 use69)
(medium r71 use70)
(medium r71 use71)
(medium r71 use72)
(medium r71 use73)
(medium r71 use74)
(medium r71 use75)
(medium r71 use76)
(medium r71 use77)
(medium r71 use78)
(medium r71 use79)
(medium r71 use80)
(medium r71 use81)
(medium r71 use82)
(medium r71 use83)
(medium r71 use84)
(medium r71 use85)
(medium r71 use86)
(medium r71 use87)
(medium r71 use88)
(heavy r71 use89)
(heavy r71 use90)
(heavy r71 use91)
(heavy r71 use92)
(heavy r71 use93)
(heavy r71 use94)
(heavy r71 use95)
(heavy r71 use96)
(heavy r71 use97)
(heavy r71 use98)
(heavy r71 use99)
(heavy r71 use100)
(heavy r71 use101)
(heavy r71 use102)
(heavy r71 use103)
(heavy r71 use104)
(heavy r71 use105)
(heavy r71 use106)
(heavy r71 use107)
(heavy r71 use108)
(heavy r71 use109)
(heavy r71 use110)
(heavy r71 use111)
(heavy r71 use112)
(heavy r71 use113)
(heavy r71 use114)
(heavy r71 use115)
(heavy r71 use116)
(heavy r71 use117)
(cap r71 use117)
(using r71 use0)
(next use0 use1)
(next use1 use2)
(next use2 use3)
(next use3 use4)
(next use4 use5)
(next use5 use6)
(next use6 use7)
(next use7 use8)
(next use8 use9)
(next use9 use10)
(next use10 use11)
(next use11 use12)
(next use12 use13)
(next use13 use14)
(next use14 use15)
(next use15 use16)
(next use16 use17)
(next use17 use18)
(next use18 use19)
(next use19 use20)
(next use20 use21)
(next use21 use22)
(next use22 use23)
(next use23 use24)
(next use24 use25)
(next use25 use26)
(next use26 use27)
(next use27 use28)
(next use28 use29)
(next use29 use30)
(next use30 use31)
(next use31 use32)
(next use32 use33)
(next use33 use34)
(next use34 use35)
(next use35 use36)
(next use36 use37)
(next use37 use38)
(next use38 use39)
(next use39 use40)
(next use40 use41)
(next use41 use42)
(next use42 use43)
(next use43 use44)
(next use44 use45)
(next use45 use46)
(next use46 use47)
(next use47 use48)
(next use48 use49)
(next use49 use50)
(next use50 use51)
(next use51 use52)
(next use52 use53)
(next use53 use54)
(next use54 use55)
(next use55 use56)
(next use56 use57)
(next use57 use58)
(next use58 use59)
(next use59 use60)
(next use60 use61)
(next use61 use62)
(next use62 use63)
(next use63 use64)
(next use64 use65)
(next use65 use66)
(next use66 use67)
(next use67 use68)
(next use68 use69)
(next use69 use70)
(next use70 use71)
(next use71 use72)
(next use72 use73)
(next use73 use74)
(next use74 use75)
(next use75 use76)
(next use76 use77)
(next use77 use78)
(next use78 use79)
(next use79 use80)
(next use80 use81)
(next use81 use82)
(next use82 use83)
(next use83 use84)
(next use84 use85)
(next use85 use86)
(next use86 use87)
(next use87 use88)
(next use88 use89)
(next use89 use90)
(next use90 use91)
(next use91 use92)
(next use92 use93)
(next use93 use94)
(next use94 use95)
(next use95 use96)
(next use96 use97)
(next use97 use98)
(next use98 use99)
(next use99 use100)
(next use100 use101)
(next use101 use102)
(next use102 use103)
(next use103 use104)
(next use104 use105)
(next use105 use106)
(next use106 use107)
(next use107 use108)
(next use108 use109)
(next use109 use110)
(next use110 use111)
(next use111 use112)
(next use112 use113)
(next use113 use114)
(next use114 use115)
(next use115 use116)
(next use116 use117)
(at v431 j77)
(togo v431 j0)
(at v444 j77)
(togo v444 j0)
(at v1203 j37)
(togo v1203 j91)
(at v450 j77)
(togo v450 j0)
(at v1222 j37)
(togo v1222 j91)
(at v1223 j37)
(togo v1223 j91)
(at v436 j77)
(togo v436 j0)
(at v1214 j37)
(togo v1214 j91)
(at v445 j77)
(togo v445 j0)
(at v451 j77)
(togo v451 j0)
(at v776 j3)
(togo v776 j33)
(at v779 j3)
(togo v779 j33)
(at v790 j3)
(togo v790 j33)
(at v1220 j37)
(togo v1220 j91)
(at v1226 j37)
(togo v1226 j91)
(at v1227 j37)
(togo v1227 j91)
(at v1221 j37)
(togo v1221 j91)
(at v1230 j37)
(togo v1230 j91)
(at v1237 j37)
(togo v1237 j91)
(at v447 j77)
(togo v447 j0)
(at v781 j3)
(togo v781 j33)
(at v432 j77)
(togo v432 j0)
(at v777 j3)
(togo v777 j33)
(at v782 j3)
(togo v782 j33)
(at v783 j3)
(togo v783 j33)
(at v791 j3)
(togo v791 j33)
(at v429 j77)
(togo v429 j0)
(at v430 j77)
(togo v430 j0)
(at v775 j3)
(togo v775 j33)
(at v1212 j37)
(togo v1212 j91)
(at v1228 j37)
(togo v1228 j91)
(at v435 j77)
(togo v435 j0)
(at v437 j77)
(togo v437 j0)
(at v446 j77)
(togo v446 j0)
(at v449 j77)
(togo v449 j0)
(at v772 j3)
(togo v772 j33)
(at v774 j3)
(togo v774 j33)
(at v785 j3)
(togo v785 j33)
(at v773 j3)
(togo v773 j33)
(at v789 j3)
(togo v789 j33)
(at v1217 j37)
(togo v1217 j91)
(at v1224 j37)
(togo v1224 j91)
(at v434 j77)
(togo v434 j0)
(at v443 j77)
(togo v443 j0)
(at v455 j77)
(togo v455 j0)
(at v769 j3)
(togo v769 j33)
(at v778 j3)
(togo v778 j33)
(at v438 j77)
(togo v438 j0)
(at v454 j77)
(togo v454 j0)
(at v766 j3)
(togo v766 j33)
(at v770 j3)
(togo v770 j33)
(at v1233 j37)
(togo v1233 j91)
(at v433 j77)
(togo v433 j0)
(at v441 j77)
(togo v441 j0)
(at v1231 j37)
(togo v1231 j91)
(at v453 j77)
(togo v453 j0)
(at v456 j77)
(togo v456 j0)
(at v767 j3)
(togo v767 j33)
(at v1219 j37)
(togo v1219 j91)
(at v1235 j37)
(togo v1235 j91)
(at v771 j3)
(togo v771 j33)
(at v1216 j37)
(togo v1216 j91)
(at v1232 j37)
(togo v1232 j91)
(at v784 j3)
(togo v784 j33)
(at v1225 j37)
(togo v1225 j91)
(at v440 j77)
(togo v440 j0)
(at v787 j3)
(togo v787 j33)
(at v442 j77)
(togo v442 j0)
(at v768 j3)
(togo v768 j33)
(at v780 j3)
(togo v780 j33)
(at v1229 j37)
(togo v1229 j91)
(at v1234 j37)
(togo v1234 j91)
(at v448 j77)
(togo v448 j0)
(at v786 j3)
(togo v786 j33)
(at v1236 j37)
(togo v1236 j91)
(at v452 j77)
(togo v452 j0)
(at v457 j77)
(togo v457 j0)
(at v788 j3)
(togo v788 j33)
(at v1211 j37)
(togo v1211 j91)
(at v439 j77)
(togo v439 j0)
(at v1213 j37)
(togo v1213 j91)
(at v1215 j37)
(togo v1215 j91)
(at v1218 j37)
(togo v1218 j91)
)
(:goal (and
(at v431 j0)
(at v444 j0)
(at v1203 j91)
(at v450 j0)
(at v1222 j91)
(at v1223 j91)
(at v436 j0)
(at v1214 j91)
(at v445 j0)
(at v451 j0)
(at v776 j33)
(at v779 j33)
(at v790 j33)
(at v1220 j91)
(at v1226 j91)
(at v1227 j91)
(at v1221 j91)
(at v1230 j91)
(at v1237 j91)
(at v447 j0)
(at v781 j33)
(at v432 j0)
(at v777 j33)
(at v782 j33)
(at v783 j33)
(at v791 j33)
(at v429 j0)
(at v430 j0)
(at v775 j33)
(at v1212 j91)
(at v1228 j91)
(at v435 j0)
(at v437 j0)
(at v446 j0)
(at v449 j0)
(at v772 j33)
(at v774 j33)
(at v785 j33)
(at v773 j33)
(at v789 j33)
(at v1217 j91)
(at v1224 j91)
(at v434 j0)
(at v443 j0)
(at v455 j0)
(at v769 j33)
(at v778 j33)
(at v438 j0)
(at v454 j0)
(at v766 j33)
(at v770 j33)
(at v1233 j91)
(at v433 j0)
(at v441 j0)
(at v1231 j91)
(at v453 j0)
(at v456 j0)
(at v767 j33)
(at v1219 j91)
(at v1235 j91)
(at v771 j33)
(at v1216 j91)
(at v1232 j91)
(at v784 j33)
(at v1225 j91)
(at v440 j0)
(at v787 j33)
(at v442 j0)
(at v768 j33)
(at v780 j33)
(at v1229 j91)
(at v1234 j91)
(at v448 j0)
(at v786 j33)
(at v1236 j91)
(at v452 j0)
(at v457 j0)
(at v788 j33)
(at v1211 j91)
(at v439 j0)
(at v1213 j91)
(at v1215 j91)
(at v1218 j91)
))
(:metric minimize (total-cost))
)