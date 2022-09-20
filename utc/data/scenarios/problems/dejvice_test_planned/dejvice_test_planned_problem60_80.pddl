(define
(problem dejvice_test_planned_problem60_80)
(:domain utc)
(:objects
j15 j23 j24 j27 j31 j32 j33 j34 j35 j36 j37 j4 j40 j41 j42 j43 j44 j45 j46 j47 j48 j49 j50 j51 j52 j53 j55 j6 j60 j62 j63 j65 j69 j70 j73 j76 j78 j8 j83 j87 j89 j90 j91 j93 j94 - junction
r0 r1 r3 r5 r7 r8 r9 r10 r14 r16 r17 r18 r19 r21 r22 r23 r25 r26 r27 r30 r31 r32 r34 r35 r36 r37 r38 r39 r41 r43 r44 r45 r46 r47 r48 r49 r50 r52 r53 r54 r55 r58 r59 r60 r61 r63 r64 r65 r66 r67 r69 r70 r71 r72 r73 r75 r76 r77 r78 r79 r80 r81 r82 r83 r84 r85 r86 r87 r88 r89 r90 r91 r93 r94 r95 r96 r97 r98 r102 r103 r104 r105 r106 r107 r108 - road
use0 use1 use2 use3 use4 use5 use6 use7 use8 use9 use10 use11 use12 use13 use14 use15 use16 use17 use18 use19 use20 use21 use22 use23 use24 use25 use26 use27 use28 use29 use30 use31 use32 use33 use34 use35 use36 use37 use38 use39 use40 use41 use42 use43 use44 use45 use46 use47 use48 use49 - use
v13 v169 v255 v111 v261 v14 v112 v177 v170 v256 v70 v262 v15 v113 v16 v171 v257 v71 v114 v17 - car
)
(:init
(= (total-cost) 0)
(connected j63 r0 j94)
(connected j31 r1 j6)
(connected j6 r3 j65)
(connected j52 r5 j53)
(connected j94 r7 j65)
(connected j93 r8 j45)
(connected j52 r9 j51)
(connected j51 r10 j4)
(connected j53 r14 j24)
(connected j24 r16 j23)
(connected j44 r17 j46)
(connected j52 r18 j50)
(connected j47 r19 j46)
(connected j31 r21 j32)
(connected j69 r22 j91)
(connected j89 r23 j94)
(connected j51 r25 j76)
(connected j43 r26 j44)
(connected j23 r27 j41)
(connected j27 r30 j76)
(connected j27 r31 j4)
(connected j50 r32 j4)
(connected j50 r34 j87)
(connected j62 r35 j89)
(connected j62 r36 j60)
(connected j6 r37 j35)
(connected j35 r38 j36)
(connected j15 r39 j27)
(connected j49 r41 j93)
(connected j55 r43 j52)
(connected j48 r44 j55)
(connected j33 r45 j35)
(connected j32 r46 j34)
(connected j63 r47 j42)
(connected j41 r48 j40)
(connected j44 r49 j45)
(connected j46 r50 j93)
(connected j48 r52 j47)
(connected j33 r53 j34)
(connected j34 r54 j37)
(connected j32 r55 j33)
(connected j89 r58 j90)
(connected j65 r59 j90)
(connected j45 r60 j60)
(connected j91 r61 j31)
(connected j36 r63 j94)
(connected j78 r64 j93)
(connected j53 r65 j52)
(connected j24 r66 j53)
(connected j23 r67 j91)
(connected j23 r69 j24)
(connected j46 r70 j44)
(connected j50 r71 j52)
(connected j40 r72 j43)
(connected j46 r73 j47)
(connected j94 r75 j89)
(connected j4 r76 j50)
(connected j87 r77 j50)
(connected j70 r78 j87)
(connected j43 r79 j42)
(connected j52 r80 j55)
(connected j55 r81 j48)
(connected j42 r82 j63)
(connected j41 r83 j42)
(connected j47 r84 j48)
(connected j37 r85 j36)
(connected j91 r86 j37)
(connected j45 r87 j62)
(connected j83 r88 j90)
(connected j46 r89 j45)
(connected j87 r90 j49)
(connected j40 r91 j24)
(connected j43 r93 j40)
(connected j42 r94 j43)
(connected j42 r95 j41)
(connected j50 r96 j49)
(connected j36 r97 j42)
(connected j90 r98 j73)
(connected j60 r102 j63)
(connected j91 r103 j23)
(connected j42 r104 j36)
(connected j4 r105 j27)
(connected j27 r106 j15)
(connected j90 r107 j8)
(connected j76 r108 j53)
(= (length-light r0) 6)
(= (length-medium r0) 69)
(= (length-heavy r0) 698)
(light r0 use0)
(light r0 use1)
(light r0 use2)
(light r0 use3)
(light r0 use4)
(light r0 use5)
(medium r0 use6)
(medium r0 use7)
(medium r0 use8)
(medium r0 use9)
(medium r0 use10)
(heavy r0 use11)
(heavy r0 use12)
(heavy r0 use13)
(cap r0 use13)
(using r0 use0)
(= (length-light r1) 4)
(= (length-medium r1) 45)
(= (length-heavy r1) 452)
(light r1 use0)
(light r1 use1)
(light r1 use2)
(light r1 use3)
(light r1 use4)
(light r1 use5)
(light r1 use6)
(medium r1 use7)
(medium r1 use8)
(medium r1 use9)
(medium r1 use10)
(medium r1 use11)
(medium r1 use12)
(medium r1 use13)
(heavy r1 use14)
(heavy r1 use15)
(heavy r1 use16)
(heavy r1 use17)
(cap r1 use17)
(using r1 use0)
(= (length-light r3) 2)
(= (length-medium r3) 25)
(= (length-heavy r3) 251)
(light r3 use0)
(light r3 use1)
(light r3 use2)
(light r3 use3)
(medium r3 use4)
(medium r3 use5)
(medium r3 use6)
(medium r3 use7)
(heavy r3 use8)
(heavy r3 use9)
(cap r3 use9)
(using r3 use0)
(= (length-light r5) 12)
(= (length-medium r5) 125)
(= (length-heavy r5) 1251)
(light r5 use0)
(light r5 use1)
(light r5 use2)
(light r5 use3)
(light r5 use4)
(light r5 use5)
(light r5 use6)
(light r5 use7)
(medium r5 use8)
(medium r5 use9)
(medium r5 use10)
(medium r5 use11)
(medium r5 use12)
(medium r5 use13)
(medium r5 use14)
(medium r5 use15)
(heavy r5 use16)
(heavy r5 use17)
(heavy r5 use18)
(heavy r5 use19)
(cap r5 use19)
(using r5 use0)
(= (length-light r7) 8)
(= (length-medium r7) 80)
(= (length-heavy r7) 803)
(light r7 use0)
(light r7 use1)
(light r7 use2)
(light r7 use3)
(light r7 use4)
(light r7 use5)
(medium r7 use6)
(medium r7 use7)
(medium r7 use8)
(medium r7 use9)
(medium r7 use10)
(medium r7 use11)
(heavy r7 use12)
(heavy r7 use13)
(heavy r7 use14)
(heavy r7 use15)
(cap r7 use15)
(using r7 use0)
(= (length-light r8) 6)
(= (length-medium r8) 69)
(= (length-heavy r8) 697)
(light r8 use0)
(light r8 use1)
(light r8 use2)
(light r8 use3)
(light r8 use4)
(light r8 use5)
(medium r8 use6)
(medium r8 use7)
(medium r8 use8)
(medium r8 use9)
(medium r8 use10)
(heavy r8 use11)
(heavy r8 use12)
(heavy r8 use13)
(cap r8 use13)
(using r8 use0)
(= (length-light r9) 3)
(= (length-medium r9) 38)
(= (length-heavy r9) 386)
(light r9 use0)
(light r9 use1)
(medium r9 use2)
(medium r9 use3)
(heavy r9 use4)
(cap r9 use4)
(using r9 use0)
(= (length-light r10) 5)
(= (length-medium r10) 56)
(= (length-heavy r10) 562)
(light r10 use0)
(light r10 use1)
(light r10 use2)
(medium r10 use3)
(medium r10 use4)
(heavy r10 use5)
(heavy r10 use6)
(cap r10 use6)
(using r10 use0)
(= (length-light r14) 10)
(= (length-medium r14) 103)
(= (length-heavy r14) 1039)
(light r14 use0)
(light r14 use1)
(light r14 use2)
(light r14 use3)
(light r14 use4)
(light r14 use5)
(light r14 use6)
(medium r14 use7)
(medium r14 use8)
(medium r14 use9)
(medium r14 use10)
(medium r14 use11)
(medium r14 use12)
(heavy r14 use13)
(heavy r14 use14)
(heavy r14 use15)
(heavy r14 use16)
(cap r14 use16)
(using r14 use0)
(= (length-light r16) 8)
(= (length-medium r16) 84)
(= (length-heavy r16) 842)
(light r16 use0)
(light r16 use1)
(light r16 use2)
(light r16 use3)
(light r16 use4)
(light r16 use5)
(light r16 use6)
(medium r16 use7)
(medium r16 use8)
(medium r16 use9)
(medium r16 use10)
(medium r16 use11)
(medium r16 use12)
(heavy r16 use13)
(heavy r16 use14)
(heavy r16 use15)
(heavy r16 use16)
(cap r16 use16)
(using r16 use0)
(= (length-light r17) 1)
(= (length-medium r17) 10)
(= (length-heavy r17) 107)
(light r17 use0)
(light r17 use1)
(medium r17 use2)
(cap r17 use2)
(using r17 use0)
(= (length-light r18) 5)
(= (length-medium r18) 58)
(= (length-heavy r18) 587)
(light r18 use0)
(light r18 use1)
(light r18 use2)
(light r18 use3)
(medium r18 use4)
(medium r18 use5)
(medium r18 use6)
(medium r18 use7)
(heavy r18 use8)
(heavy r18 use9)
(cap r18 use9)
(using r18 use0)
(= (length-light r19) 19)
(= (length-medium r19) 196)
(= (length-heavy r19) 1967)
(light r19 use0)
(light r19 use1)
(light r19 use2)
(light r19 use3)
(light r19 use4)
(light r19 use5)
(light r19 use6)
(light r19 use7)
(light r19 use8)
(medium r19 use9)
(medium r19 use10)
(medium r19 use11)
(medium r19 use12)
(medium r19 use13)
(medium r19 use14)
(medium r19 use15)
(medium r19 use16)
(medium r19 use17)
(heavy r19 use18)
(heavy r19 use19)
(heavy r19 use20)
(heavy r19 use21)
(heavy r19 use22)
(heavy r19 use23)
(cap r19 use23)
(using r19 use0)
(= (length-light r21) 2)
(= (length-medium r21) 24)
(= (length-heavy r21) 245)
(light r21 use0)
(light r21 use1)
(medium r21 use2)
(medium r21 use3)
(heavy r21 use4)
(cap r21 use4)
(using r21 use0)
(= (length-light r22) 5)
(= (length-medium r22) 53)
(= (length-heavy r22) 534)
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
(cap r22 use10)
(using r22 use0)
(= (length-light r23) 3)
(= (length-medium r23) 34)
(= (length-heavy r23) 349)
(light r23 use0)
(light r23 use1)
(light r23 use2)
(medium r23 use3)
(medium r23 use4)
(heavy r23 use5)
(heavy r23 use6)
(cap r23 use6)
(using r23 use0)
(= (length-light r25) 18)
(= (length-medium r25) 189)
(= (length-heavy r25) 1895)
(light r25 use0)
(light r25 use1)
(light r25 use2)
(light r25 use3)
(light r25 use4)
(light r25 use5)
(light r25 use6)
(light r25 use7)
(light r25 use8)
(medium r25 use9)
(medium r25 use10)
(medium r25 use11)
(medium r25 use12)
(medium r25 use13)
(medium r25 use14)
(medium r25 use15)
(medium r25 use16)
(medium r25 use17)
(heavy r25 use18)
(heavy r25 use19)
(heavy r25 use20)
(heavy r25 use21)
(heavy r25 use22)
(cap r25 use22)
(using r25 use0)
(= (length-light r26) 27)
(= (length-medium r26) 272)
(= (length-heavy r26) 2724)
(light r26 use0)
(light r26 use1)
(light r26 use2)
(light r26 use3)
(light r26 use4)
(light r26 use5)
(light r26 use6)
(light r26 use7)
(light r26 use8)
(light r26 use9)
(light r26 use10)
(light r26 use11)
(medium r26 use12)
(medium r26 use13)
(medium r26 use14)
(medium r26 use15)
(medium r26 use16)
(medium r26 use17)
(medium r26 use18)
(medium r26 use19)
(medium r26 use20)
(medium r26 use21)
(medium r26 use22)
(medium r26 use23)
(medium r26 use24)
(heavy r26 use25)
(heavy r26 use26)
(heavy r26 use27)
(heavy r26 use28)
(heavy r26 use29)
(heavy r26 use30)
(heavy r26 use31)
(heavy r26 use32)
(cap r26 use32)
(using r26 use0)
(= (length-light r27) 26)
(= (length-medium r27) 269)
(= (length-heavy r27) 2695)
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
(light r27 use10)
(light r27 use11)
(medium r27 use12)
(medium r27 use13)
(medium r27 use14)
(medium r27 use15)
(medium r27 use16)
(medium r27 use17)
(medium r27 use18)
(medium r27 use19)
(medium r27 use20)
(medium r27 use21)
(medium r27 use22)
(medium r27 use23)
(medium r27 use24)
(heavy r27 use25)
(heavy r27 use26)
(heavy r27 use27)
(heavy r27 use28)
(heavy r27 use29)
(heavy r27 use30)
(heavy r27 use31)
(heavy r27 use32)
(cap r27 use32)
(using r27 use0)
(= (length-light r30) 13)
(= (length-medium r30) 139)
(= (length-heavy r30) 1397)
(light r30 use0)
(light r30 use1)
(light r30 use2)
(light r30 use3)
(light r30 use4)
(light r30 use5)
(light r30 use6)
(medium r30 use7)
(medium r30 use8)
(medium r30 use9)
(medium r30 use10)
(medium r30 use11)
(medium r30 use12)
(heavy r30 use13)
(heavy r30 use14)
(heavy r30 use15)
(heavy r30 use16)
(cap r30 use16)
(using r30 use0)
(= (length-light r31) 5)
(= (length-medium r31) 52)
(= (length-heavy r31) 522)
(light r31 use0)
(light r31 use1)
(light r31 use2)
(light r31 use3)
(light r31 use4)
(light r31 use5)
(light r31 use6)
(medium r31 use7)
(medium r31 use8)
(medium r31 use9)
(medium r31 use10)
(medium r31 use11)
(medium r31 use12)
(heavy r31 use13)
(heavy r31 use14)
(heavy r31 use15)
(heavy r31 use16)
(cap r31 use16)
(using r31 use0)
(= (length-light r32) 4)
(= (length-medium r32) 40)
(= (length-heavy r32) 409)
(light r32 use0)
(light r32 use1)
(light r32 use2)
(light r32 use3)
(medium r32 use4)
(medium r32 use5)
(medium r32 use6)
(heavy r32 use7)
(heavy r32 use8)
(cap r32 use8)
(using r32 use0)
(= (length-light r34) 8)
(= (length-medium r34) 80)
(= (length-heavy r34) 804)
(light r34 use0)
(light r34 use1)
(light r34 use2)
(light r34 use3)
(light r34 use4)
(medium r34 use5)
(medium r34 use6)
(medium r34 use7)
(medium r34 use8)
(medium r34 use9)
(heavy r34 use10)
(heavy r34 use11)
(heavy r34 use12)
(cap r34 use12)
(using r34 use0)
(= (length-light r35) 13)
(= (length-medium r35) 133)
(= (length-heavy r35) 1336)
(light r35 use0)
(light r35 use1)
(light r35 use2)
(light r35 use3)
(light r35 use4)
(light r35 use5)
(light r35 use6)
(light r35 use7)
(light r35 use8)
(light r35 use9)
(light r35 use10)
(light r35 use11)
(light r35 use12)
(medium r35 use13)
(medium r35 use14)
(medium r35 use15)
(medium r35 use16)
(medium r35 use17)
(medium r35 use18)
(medium r35 use19)
(medium r35 use20)
(medium r35 use21)
(medium r35 use22)
(medium r35 use23)
(medium r35 use24)
(medium r35 use25)
(medium r35 use26)
(heavy r35 use27)
(heavy r35 use28)
(heavy r35 use29)
(heavy r35 use30)
(heavy r35 use31)
(heavy r35 use32)
(heavy r35 use33)
(heavy r35 use34)
(cap r35 use34)
(using r35 use0)
(= (length-light r36) 11)
(= (length-medium r36) 110)
(= (length-heavy r36) 1104)
(light r36 use0)
(light r36 use1)
(light r36 use2)
(light r36 use3)
(light r36 use4)
(light r36 use5)
(light r36 use6)
(light r36 use7)
(medium r36 use8)
(medium r36 use9)
(medium r36 use10)
(medium r36 use11)
(medium r36 use12)
(medium r36 use13)
(medium r36 use14)
(medium r36 use15)
(heavy r36 use16)
(heavy r36 use17)
(heavy r36 use18)
(heavy r36 use19)
(heavy r36 use20)
(heavy r36 use21)
(cap r36 use21)
(using r36 use0)
(= (length-light r37) 7)
(= (length-medium r37) 73)
(= (length-heavy r37) 731)
(light r37 use0)
(light r37 use1)
(light r37 use2)
(light r37 use3)
(medium r37 use4)
(medium r37 use5)
(medium r37 use6)
(heavy r37 use7)
(heavy r37 use8)
(cap r37 use8)
(using r37 use0)
(= (length-light r38) 7)
(= (length-medium r38) 78)
(= (length-heavy r38) 785)
(light r38 use0)
(light r38 use1)
(light r38 use2)
(light r38 use3)
(medium r38 use4)
(medium r38 use5)
(medium r38 use6)
(medium r38 use7)
(heavy r38 use8)
(heavy r38 use9)
(cap r38 use9)
(using r38 use0)
(= (length-light r39) 11)
(= (length-medium r39) 113)
(= (length-heavy r39) 1137)
(light r39 use0)
(light r39 use1)
(light r39 use2)
(light r39 use3)
(light r39 use4)
(light r39 use5)
(light r39 use6)
(light r39 use7)
(light r39 use8)
(light r39 use9)
(light r39 use10)
(light r39 use11)
(light r39 use12)
(light r39 use13)
(medium r39 use14)
(medium r39 use15)
(medium r39 use16)
(medium r39 use17)
(medium r39 use18)
(medium r39 use19)
(medium r39 use20)
(medium r39 use21)
(medium r39 use22)
(medium r39 use23)
(medium r39 use24)
(medium r39 use25)
(medium r39 use26)
(medium r39 use27)
(heavy r39 use28)
(heavy r39 use29)
(heavy r39 use30)
(heavy r39 use31)
(heavy r39 use32)
(heavy r39 use33)
(heavy r39 use34)
(heavy r39 use35)
(heavy r39 use36)
(cap r39 use36)
(using r39 use0)
(= (length-light r41) 24)
(= (length-medium r41) 247)
(= (length-heavy r41) 2471)
(light r41 use0)
(light r41 use1)
(light r41 use2)
(light r41 use3)
(light r41 use4)
(light r41 use5)
(light r41 use6)
(light r41 use7)
(light r41 use8)
(light r41 use9)
(light r41 use10)
(light r41 use11)
(light r41 use12)
(light r41 use13)
(light r41 use14)
(light r41 use15)
(light r41 use16)
(light r41 use17)
(medium r41 use18)
(medium r41 use19)
(medium r41 use20)
(medium r41 use21)
(medium r41 use22)
(medium r41 use23)
(medium r41 use24)
(medium r41 use25)
(medium r41 use26)
(medium r41 use27)
(medium r41 use28)
(medium r41 use29)
(medium r41 use30)
(medium r41 use31)
(medium r41 use32)
(medium r41 use33)
(medium r41 use34)
(medium r41 use35)
(medium r41 use36)
(medium r41 use37)
(heavy r41 use38)
(heavy r41 use39)
(heavy r41 use40)
(heavy r41 use41)
(heavy r41 use42)
(heavy r41 use43)
(heavy r41 use44)
(heavy r41 use45)
(heavy r41 use46)
(heavy r41 use47)
(heavy r41 use48)
(heavy r41 use49)
(cap r41 use49)
(using r41 use0)
(= (length-light r43) 4)
(= (length-medium r43) 41)
(= (length-heavy r43) 417)
(light r43 use0)
(light r43 use1)
(medium r43 use2)
(medium r43 use3)
(heavy r43 use4)
(cap r43 use4)
(using r43 use0)
(= (length-light r44) 5)
(= (length-medium r44) 58)
(= (length-heavy r44) 581)
(light r44 use0)
(light r44 use1)
(light r44 use2)
(medium r44 use3)
(medium r44 use4)
(heavy r44 use5)
(heavy r44 use6)
(cap r44 use6)
(using r44 use0)
(= (length-light r45) 15)
(= (length-medium r45) 156)
(= (length-heavy r45) 1561)
(light r45 use0)
(light r45 use1)
(light r45 use2)
(light r45 use3)
(light r45 use4)
(light r45 use5)
(light r45 use6)
(medium r45 use7)
(medium r45 use8)
(medium r45 use9)
(medium r45 use10)
(medium r45 use11)
(medium r45 use12)
(medium r45 use13)
(heavy r45 use14)
(heavy r45 use15)
(heavy r45 use16)
(heavy r45 use17)
(heavy r45 use18)
(cap r45 use18)
(using r45 use0)
(= (length-light r46) 30)
(= (length-medium r46) 306)
(= (length-heavy r46) 3060)
(light r46 use0)
(light r46 use1)
(light r46 use2)
(light r46 use3)
(light r46 use4)
(light r46 use5)
(light r46 use6)
(light r46 use7)
(light r46 use8)
(light r46 use9)
(light r46 use10)
(light r46 use11)
(light r46 use12)
(light r46 use13)
(medium r46 use14)
(medium r46 use15)
(medium r46 use16)
(medium r46 use17)
(medium r46 use18)
(medium r46 use19)
(medium r46 use20)
(medium r46 use21)
(medium r46 use22)
(medium r46 use23)
(medium r46 use24)
(medium r46 use25)
(medium r46 use26)
(medium r46 use27)
(heavy r46 use28)
(heavy r46 use29)
(heavy r46 use30)
(heavy r46 use31)
(heavy r46 use32)
(heavy r46 use33)
(heavy r46 use34)
(heavy r46 use35)
(heavy r46 use36)
(cap r46 use36)
(using r46 use0)
(= (length-light r47) 10)
(= (length-medium r47) 107)
(= (length-heavy r47) 1076)
(light r47 use0)
(light r47 use1)
(light r47 use2)
(light r47 use3)
(light r47 use4)
(medium r47 use5)
(medium r47 use6)
(medium r47 use7)
(medium r47 use8)
(medium r47 use9)
(heavy r47 use10)
(heavy r47 use11)
(heavy r47 use12)
(cap r47 use12)
(using r47 use0)
(= (length-light r48) 1)
(= (length-medium r48) 15)
(= (length-heavy r48) 152)
(light r48 use0)
(light r48 use1)
(cap r48 use1)
(using r48 use0)
(= (length-light r49) 1)
(= (length-medium r49) 18)
(= (length-heavy r49) 186)
(light r49 use0)
(light r49 use1)
(medium r49 use2)
(heavy r49 use3)
(cap r49 use3)
(using r49 use0)
(= (length-light r50) 5)
(= (length-medium r50) 57)
(= (length-heavy r50) 576)
(light r50 use0)
(light r50 use1)
(light r50 use2)
(light r50 use3)
(light r50 use4)
(medium r50 use5)
(medium r50 use6)
(medium r50 use7)
(medium r50 use8)
(heavy r50 use9)
(heavy r50 use10)
(heavy r50 use11)
(cap r50 use11)
(using r50 use0)
(= (length-light r52) 16)
(= (length-medium r52) 165)
(= (length-heavy r52) 1650)
(light r52 use0)
(light r52 use1)
(light r52 use2)
(light r52 use3)
(light r52 use4)
(light r52 use5)
(light r52 use6)
(light r52 use7)
(medium r52 use8)
(medium r52 use9)
(medium r52 use10)
(medium r52 use11)
(medium r52 use12)
(medium r52 use13)
(medium r52 use14)
(medium r52 use15)
(heavy r52 use16)
(heavy r52 use17)
(heavy r52 use18)
(heavy r52 use19)
(cap r52 use19)
(using r52 use0)
(= (length-light r53) 4)
(= (length-medium r53) 42)
(= (length-heavy r53) 424)
(light r53 use0)
(light r53 use1)
(light r53 use2)
(medium r53 use3)
(medium r53 use4)
(heavy r53 use5)
(cap r53 use5)
(using r53 use0)
(= (length-light r54) 3)
(= (length-medium r54) 35)
(= (length-heavy r54) 351)
(light r54 use0)
(light r54 use1)
(light r54 use2)
(medium r54 use3)
(medium r54 use4)
(heavy r54 use5)
(cap r54 use5)
(using r54 use0)
(= (length-light r55) 3)
(= (length-medium r55) 39)
(= (length-heavy r55) 395)
(light r55 use0)
(light r55 use1)
(medium r55 use2)
(medium r55 use3)
(heavy r55 use4)
(cap r55 use4)
(using r55 use0)
(= (length-light r58) 3)
(= (length-medium r58) 35)
(= (length-heavy r58) 351)
(light r58 use0)
(light r58 use1)
(light r58 use2)
(light r58 use3)
(light r58 use4)
(light r58 use5)
(light r58 use6)
(light r58 use7)
(light r58 use8)
(medium r58 use9)
(medium r58 use10)
(medium r58 use11)
(medium r58 use12)
(medium r58 use13)
(medium r58 use14)
(medium r58 use15)
(medium r58 use16)
(medium r58 use17)
(heavy r58 use18)
(heavy r58 use19)
(heavy r58 use20)
(heavy r58 use21)
(heavy r58 use22)
(cap r58 use22)
(using r58 use0)
(= (length-light r59) 1)
(= (length-medium r59) 19)
(= (length-heavy r59) 198)
(light r59 use0)
(light r59 use1)
(light r59 use2)
(medium r59 use3)
(medium r59 use4)
(medium r59 use5)
(heavy r59 use6)
(heavy r59 use7)
(cap r59 use7)
(using r59 use0)
(= (length-light r60) 12)
(= (length-medium r60) 127)
(= (length-heavy r60) 1270)
(light r60 use0)
(light r60 use1)
(light r60 use2)
(light r60 use3)
(light r60 use4)
(light r60 use5)
(light r60 use6)
(light r60 use7)
(light r60 use8)
(light r60 use9)
(medium r60 use10)
(medium r60 use11)
(medium r60 use12)
(medium r60 use13)
(medium r60 use14)
(medium r60 use15)
(medium r60 use16)
(medium r60 use17)
(medium r60 use18)
(medium r60 use19)
(heavy r60 use20)
(heavy r60 use21)
(heavy r60 use22)
(heavy r60 use23)
(heavy r60 use24)
(heavy r60 use25)
(cap r60 use25)
(using r60 use0)
(= (length-light r61) 23)
(= (length-medium r61) 232)
(= (length-heavy r61) 2320)
(light r61 use0)
(light r61 use1)
(light r61 use2)
(light r61 use3)
(light r61 use4)
(light r61 use5)
(light r61 use6)
(light r61 use7)
(light r61 use8)
(light r61 use9)
(light r61 use10)
(light r61 use11)
(light r61 use12)
(light r61 use13)
(light r61 use14)
(light r61 use15)
(light r61 use16)
(light r61 use17)
(medium r61 use18)
(medium r61 use19)
(medium r61 use20)
(medium r61 use21)
(medium r61 use22)
(medium r61 use23)
(medium r61 use24)
(medium r61 use25)
(medium r61 use26)
(medium r61 use27)
(medium r61 use28)
(medium r61 use29)
(medium r61 use30)
(medium r61 use31)
(medium r61 use32)
(medium r61 use33)
(medium r61 use34)
(medium r61 use35)
(medium r61 use36)
(medium r61 use37)
(heavy r61 use38)
(heavy r61 use39)
(heavy r61 use40)
(heavy r61 use41)
(heavy r61 use42)
(heavy r61 use43)
(heavy r61 use44)
(heavy r61 use45)
(heavy r61 use46)
(heavy r61 use47)
(heavy r61 use48)
(heavy r61 use49)
(cap r61 use49)
(using r61 use0)
(= (length-light r63) 4)
(= (length-medium r63) 49)
(= (length-heavy r63) 496)
(light r63 use0)
(light r63 use1)
(light r63 use2)
(light r63 use3)
(medium r63 use4)
(medium r63 use5)
(medium r63 use6)
(medium r63 use7)
(heavy r63 use8)
(heavy r63 use9)
(cap r63 use9)
(using r63 use0)
(= (length-light r64) 11)
(= (length-medium r64) 118)
(= (length-heavy r64) 1188)
(light r64 use0)
(light r64 use1)
(light r64 use2)
(light r64 use3)
(light r64 use4)
(light r64 use5)
(light r64 use6)
(medium r64 use7)
(medium r64 use8)
(medium r64 use9)
(medium r64 use10)
(medium r64 use11)
(medium r64 use12)
(medium r64 use13)
(heavy r64 use14)
(heavy r64 use15)
(heavy r64 use16)
(heavy r64 use17)
(heavy r64 use18)
(cap r64 use18)
(using r64 use0)
(= (length-light r65) 11)
(= (length-medium r65) 111)
(= (length-heavy r65) 1112)
(light r65 use0)
(light r65 use1)
(light r65 use2)
(light r65 use3)
(light r65 use4)
(light r65 use5)
(light r65 use6)
(light r65 use7)
(medium r65 use8)
(medium r65 use9)
(medium r65 use10)
(medium r65 use11)
(medium r65 use12)
(medium r65 use13)
(medium r65 use14)
(medium r65 use15)
(heavy r65 use16)
(heavy r65 use17)
(heavy r65 use18)
(heavy r65 use19)
(cap r65 use19)
(using r65 use0)
(= (length-light r66) 9)
(= (length-medium r66) 92)
(= (length-heavy r66) 923)
(light r66 use0)
(light r66 use1)
(light r66 use2)
(light r66 use3)
(light r66 use4)
(light r66 use5)
(light r66 use6)
(medium r66 use7)
(medium r66 use8)
(medium r66 use9)
(medium r66 use10)
(medium r66 use11)
(medium r66 use12)
(heavy r66 use13)
(heavy r66 use14)
(heavy r66 use15)
(heavy r66 use16)
(cap r66 use16)
(using r66 use0)
(= (length-light r67) 5)
(= (length-medium r67) 54)
(= (length-heavy r67) 542)
(light r67 use0)
(light r67 use1)
(light r67 use2)
(light r67 use3)
(light r67 use4)
(medium r67 use5)
(medium r67 use6)
(medium r67 use7)
(medium r67 use8)
(heavy r67 use9)
(heavy r67 use10)
(cap r67 use10)
(using r67 use0)
(= (length-light r69) 8)
(= (length-medium r69) 84)
(= (length-heavy r69) 842)
(light r69 use0)
(light r69 use1)
(light r69 use2)
(light r69 use3)
(light r69 use4)
(light r69 use5)
(light r69 use6)
(medium r69 use7)
(medium r69 use8)
(medium r69 use9)
(medium r69 use10)
(medium r69 use11)
(medium r69 use12)
(heavy r69 use13)
(heavy r69 use14)
(heavy r69 use15)
(heavy r69 use16)
(cap r69 use16)
(using r69 use0)
(= (length-light r70) 1)
(= (length-medium r70) 10)
(= (length-heavy r70) 107)
(light r70 use0)
(light r70 use1)
(medium r70 use2)
(cap r70 use2)
(using r70 use0)
(= (length-light r71) 6)
(= (length-medium r71) 60)
(= (length-heavy r71) 609)
(light r71 use0)
(light r71 use1)
(light r71 use2)
(light r71 use3)
(medium r71 use4)
(medium r71 use5)
(medium r71 use6)
(medium r71 use7)
(heavy r71 use8)
(heavy r71 use9)
(cap r71 use9)
(using r71 use0)
(= (length-light r72) 2)
(= (length-medium r72) 20)
(= (length-heavy r72) 204)
(light r72 use0)
(light r72 use1)
(medium r72 use2)
(cap r72 use2)
(using r72 use0)
(= (length-light r73) 19)
(= (length-medium r73) 196)
(= (length-heavy r73) 1967)
(light r73 use0)
(light r73 use1)
(light r73 use2)
(light r73 use3)
(light r73 use4)
(light r73 use5)
(light r73 use6)
(light r73 use7)
(light r73 use8)
(medium r73 use9)
(medium r73 use10)
(medium r73 use11)
(medium r73 use12)
(medium r73 use13)
(medium r73 use14)
(medium r73 use15)
(medium r73 use16)
(medium r73 use17)
(heavy r73 use18)
(heavy r73 use19)
(heavy r73 use20)
(heavy r73 use21)
(heavy r73 use22)
(heavy r73 use23)
(cap r73 use23)
(using r73 use0)
(= (length-light r75) 3)
(= (length-medium r75) 34)
(= (length-heavy r75) 349)
(light r75 use0)
(light r75 use1)
(light r75 use2)
(medium r75 use3)
(medium r75 use4)
(heavy r75 use5)
(heavy r75 use6)
(cap r75 use6)
(using r75 use0)
(= (length-light r76) 4)
(= (length-medium r76) 40)
(= (length-heavy r76) 409)
(light r76 use0)
(light r76 use1)
(light r76 use2)
(light r76 use3)
(medium r76 use4)
(medium r76 use5)
(medium r76 use6)
(heavy r76 use7)
(heavy r76 use8)
(cap r76 use8)
(using r76 use0)
(= (length-light r77) 8)
(= (length-medium r77) 80)
(= (length-heavy r77) 809)
(light r77 use0)
(light r77 use1)
(light r77 use2)
(light r77 use3)
(light r77 use4)
(medium r77 use5)
(medium r77 use6)
(medium r77 use7)
(medium r77 use8)
(medium r77 use9)
(heavy r77 use10)
(heavy r77 use11)
(heavy r77 use12)
(cap r77 use12)
(using r77 use0)
(= (length-light r78) 5)
(= (length-medium r78) 52)
(= (length-heavy r78) 525)
(light r78 use0)
(light r78 use1)
(light r78 use2)
(light r78 use3)
(medium r78 use4)
(medium r78 use5)
(medium r78 use6)
(heavy r78 use7)
(heavy r78 use8)
(cap r78 use8)
(using r78 use0)
(= (length-light r79) 1)
(= (length-medium r79) 10)
(= (length-heavy r79) 106)
(light r79 use0)
(light r79 use1)
(cap r79 use1)
(using r79 use0)
(= (length-light r80) 4)
(= (length-medium r80) 41)
(= (length-heavy r80) 417)
(light r80 use0)
(light r80 use1)
(medium r80 use2)
(medium r80 use3)
(heavy r80 use4)
(cap r80 use4)
(using r80 use0)
(= (length-light r81) 5)
(= (length-medium r81) 58)
(= (length-heavy r81) 581)
(light r81 use0)
(light r81 use1)
(light r81 use2)
(medium r81 use3)
(medium r81 use4)
(heavy r81 use5)
(heavy r81 use6)
(cap r81 use6)
(using r81 use0)
(= (length-light r82) 10)
(= (length-medium r82) 107)
(= (length-heavy r82) 1076)
(light r82 use0)
(light r82 use1)
(light r82 use2)
(light r82 use3)
(light r82 use4)
(medium r82 use5)
(medium r82 use6)
(medium r82 use7)
(medium r82 use8)
(medium r82 use9)
(heavy r82 use10)
(heavy r82 use11)
(heavy r82 use12)
(cap r82 use12)
(using r82 use0)
(= (length-light r83) 1)
(= (length-medium r83) 18)
(= (length-heavy r83) 180)
(light r83 use0)
(light r83 use1)
(medium r83 use2)
(cap r83 use2)
(using r83 use0)
(= (length-light r84) 16)
(= (length-medium r84) 164)
(= (length-heavy r84) 1649)
(light r84 use0)
(light r84 use1)
(light r84 use2)
(light r84 use3)
(light r84 use4)
(light r84 use5)
(light r84 use6)
(light r84 use7)
(medium r84 use8)
(medium r84 use9)
(medium r84 use10)
(medium r84 use11)
(medium r84 use12)
(medium r84 use13)
(medium r84 use14)
(medium r84 use15)
(heavy r84 use16)
(heavy r84 use17)
(heavy r84 use18)
(heavy r84 use19)
(cap r84 use19)
(using r84 use0)
(= (length-light r85) 5)
(= (length-medium r85) 55)
(= (length-heavy r85) 557)
(light r85 use0)
(light r85 use1)
(light r85 use2)
(light r85 use3)
(light r85 use4)
(light r85 use5)
(light r85 use6)
(medium r85 use7)
(medium r85 use8)
(medium r85 use9)
(medium r85 use10)
(medium r85 use11)
(medium r85 use12)
(medium r85 use13)
(heavy r85 use14)
(heavy r85 use15)
(heavy r85 use16)
(heavy r85 use17)
(cap r85 use17)
(using r85 use0)
(= (length-light r86) 5)
(= (length-medium r86) 56)
(= (length-heavy r86) 564)
(light r86 use0)
(light r86 use1)
(light r86 use2)
(light r86 use3)
(light r86 use4)
(light r86 use5)
(light r86 use6)
(medium r86 use7)
(medium r86 use8)
(medium r86 use9)
(medium r86 use10)
(medium r86 use11)
(medium r86 use12)
(medium r86 use13)
(heavy r86 use14)
(heavy r86 use15)
(heavy r86 use16)
(heavy r86 use17)
(cap r86 use17)
(using r86 use0)
(= (length-light r87) 21)
(= (length-medium r87) 215)
(= (length-heavy r87) 2150)
(light r87 use0)
(light r87 use1)
(light r87 use2)
(light r87 use3)
(light r87 use4)
(light r87 use5)
(light r87 use6)
(light r87 use7)
(light r87 use8)
(light r87 use9)
(light r87 use10)
(light r87 use11)
(light r87 use12)
(light r87 use13)
(light r87 use14)
(light r87 use15)
(medium r87 use16)
(medium r87 use17)
(medium r87 use18)
(medium r87 use19)
(medium r87 use20)
(medium r87 use21)
(medium r87 use22)
(medium r87 use23)
(medium r87 use24)
(medium r87 use25)
(medium r87 use26)
(medium r87 use27)
(medium r87 use28)
(medium r87 use29)
(medium r87 use30)
(medium r87 use31)
(medium r87 use32)
(heavy r87 use33)
(heavy r87 use34)
(heavy r87 use35)
(heavy r87 use36)
(heavy r87 use37)
(heavy r87 use38)
(heavy r87 use39)
(heavy r87 use40)
(heavy r87 use41)
(heavy r87 use42)
(cap r87 use42)
(using r87 use0)
(= (length-light r88) 1)
(= (length-medium r88) 12)
(= (length-heavy r88) 127)
(light r88 use0)
(light r88 use1)
(light r88 use2)
(light r88 use3)
(medium r88 use4)
(medium r88 use5)
(medium r88 use6)
(heavy r88 use7)
(heavy r88 use8)
(cap r88 use8)
(using r88 use0)
(= (length-light r89) 1)
(= (length-medium r89) 15)
(= (length-heavy r89) 154)
(light r89 use0)
(light r89 use1)
(medium r89 use2)
(heavy r89 use3)
(cap r89 use3)
(using r89 use0)
(= (length-light r90) 11)
(= (length-medium r90) 111)
(= (length-heavy r90) 1119)
(light r90 use0)
(light r90 use1)
(light r90 use2)
(light r90 use3)
(light r90 use4)
(light r90 use5)
(light r90 use6)
(light r90 use7)
(light r90 use8)
(medium r90 use9)
(medium r90 use10)
(medium r90 use11)
(medium r90 use12)
(medium r90 use13)
(medium r90 use14)
(medium r90 use15)
(medium r90 use16)
(medium r90 use17)
(heavy r90 use18)
(heavy r90 use19)
(heavy r90 use20)
(heavy r90 use21)
(heavy r90 use22)
(cap r90 use22)
(using r90 use0)
(= (length-light r91) 41)
(= (length-medium r91) 419)
(= (length-heavy r91) 4191)
(light r91 use0)
(light r91 use1)
(light r91 use2)
(light r91 use3)
(light r91 use4)
(light r91 use5)
(light r91 use6)
(light r91 use7)
(light r91 use8)
(light r91 use9)
(light r91 use10)
(light r91 use11)
(light r91 use12)
(light r91 use13)
(light r91 use14)
(light r91 use15)
(light r91 use16)
(light r91 use17)
(medium r91 use18)
(medium r91 use19)
(medium r91 use20)
(medium r91 use21)
(medium r91 use22)
(medium r91 use23)
(medium r91 use24)
(medium r91 use25)
(medium r91 use26)
(medium r91 use27)
(medium r91 use28)
(medium r91 use29)
(medium r91 use30)
(medium r91 use31)
(medium r91 use32)
(medium r91 use33)
(medium r91 use34)
(medium r91 use35)
(medium r91 use36)
(medium r91 use37)
(heavy r91 use38)
(heavy r91 use39)
(heavy r91 use40)
(heavy r91 use41)
(heavy r91 use42)
(heavy r91 use43)
(heavy r91 use44)
(heavy r91 use45)
(heavy r91 use46)
(heavy r91 use47)
(heavy r91 use48)
(heavy r91 use49)
(cap r91 use49)
(using r91 use0)
(= (length-light r93) 2)
(= (length-medium r93) 20)
(= (length-heavy r93) 204)
(light r93 use0)
(light r93 use1)
(medium r93 use2)
(cap r93 use2)
(using r93 use0)
(= (length-light r94) 1)
(= (length-medium r94) 10)
(= (length-heavy r94) 106)
(light r94 use0)
(light r94 use1)
(cap r94 use1)
(using r94 use0)
(= (length-light r95) 1)
(= (length-medium r95) 18)
(= (length-heavy r95) 180)
(light r95 use0)
(light r95 use1)
(medium r95 use2)
(cap r95 use2)
(using r95 use0)
(= (length-light r96) 5)
(= (length-medium r96) 56)
(= (length-heavy r96) 562)
(light r96 use0)
(light r96 use1)
(light r96 use2)
(light r96 use3)
(light r96 use4)
(medium r96 use5)
(medium r96 use6)
(medium r96 use7)
(medium r96 use8)
(heavy r96 use9)
(heavy r96 use10)
(heavy r96 use11)
(cap r96 use11)
(using r96 use0)
(= (length-light r97) 11)
(= (length-medium r97) 112)
(= (length-heavy r97) 1126)
(light r97 use0)
(light r97 use1)
(light r97 use2)
(light r97 use3)
(light r97 use4)
(light r97 use5)
(medium r97 use6)
(medium r97 use7)
(medium r97 use8)
(medium r97 use9)
(medium r97 use10)
(heavy r97 use11)
(heavy r97 use12)
(heavy r97 use13)
(cap r97 use13)
(using r97 use0)
(= (length-light r98) 8)
(= (length-medium r98) 83)
(= (length-heavy r98) 838)
(light r98 use0)
(light r98 use1)
(light r98 use2)
(light r98 use3)
(light r98 use4)
(light r98 use5)
(light r98 use6)
(light r98 use7)
(light r98 use8)
(light r98 use9)
(light r98 use10)
(light r98 use11)
(light r98 use12)
(medium r98 use13)
(medium r98 use14)
(medium r98 use15)
(medium r98 use16)
(medium r98 use17)
(medium r98 use18)
(medium r98 use19)
(medium r98 use20)
(medium r98 use21)
(medium r98 use22)
(medium r98 use23)
(medium r98 use24)
(medium r98 use25)
(heavy r98 use26)
(heavy r98 use27)
(heavy r98 use28)
(heavy r98 use29)
(heavy r98 use30)
(heavy r98 use31)
(heavy r98 use32)
(heavy r98 use33)
(cap r98 use33)
(using r98 use0)
(= (length-light r102) 4)
(= (length-medium r102) 47)
(= (length-heavy r102) 473)
(light r102 use0)
(light r102 use1)
(light r102 use2)
(light r102 use3)
(medium r102 use4)
(medium r102 use5)
(medium r102 use6)
(medium r102 use7)
(heavy r102 use8)
(heavy r102 use9)
(cap r102 use9)
(using r102 use0)
(= (length-light r103) 5)
(= (length-medium r103) 54)
(= (length-heavy r103) 542)
(light r103 use0)
(light r103 use1)
(light r103 use2)
(light r103 use3)
(light r103 use4)
(medium r103 use5)
(medium r103 use6)
(medium r103 use7)
(medium r103 use8)
(heavy r103 use9)
(heavy r103 use10)
(cap r103 use10)
(using r103 use0)
(= (length-light r104) 11)
(= (length-medium r104) 112)
(= (length-heavy r104) 1127)
(light r104 use0)
(light r104 use1)
(light r104 use2)
(light r104 use3)
(light r104 use4)
(light r104 use5)
(medium r104 use6)
(medium r104 use7)
(medium r104 use8)
(medium r104 use9)
(medium r104 use10)
(heavy r104 use11)
(heavy r104 use12)
(heavy r104 use13)
(cap r104 use13)
(using r104 use0)
(= (length-light r105) 5)
(= (length-medium r105) 52)
(= (length-heavy r105) 522)
(light r105 use0)
(light r105 use1)
(light r105 use2)
(light r105 use3)
(light r105 use4)
(light r105 use5)
(light r105 use6)
(medium r105 use7)
(medium r105 use8)
(medium r105 use9)
(medium r105 use10)
(medium r105 use11)
(medium r105 use12)
(heavy r105 use13)
(heavy r105 use14)
(heavy r105 use15)
(heavy r105 use16)
(cap r105 use16)
(using r105 use0)
(= (length-light r106) 11)
(= (length-medium r106) 113)
(= (length-heavy r106) 1137)
(light r106 use0)
(light r106 use1)
(light r106 use2)
(light r106 use3)
(light r106 use4)
(light r106 use5)
(light r106 use6)
(light r106 use7)
(light r106 use8)
(light r106 use9)
(light r106 use10)
(light r106 use11)
(light r106 use12)
(light r106 use13)
(medium r106 use14)
(medium r106 use15)
(medium r106 use16)
(medium r106 use17)
(medium r106 use18)
(medium r106 use19)
(medium r106 use20)
(medium r106 use21)
(medium r106 use22)
(medium r106 use23)
(medium r106 use24)
(medium r106 use25)
(medium r106 use26)
(medium r106 use27)
(heavy r106 use28)
(heavy r106 use29)
(heavy r106 use30)
(heavy r106 use31)
(heavy r106 use32)
(heavy r106 use33)
(heavy r106 use34)
(heavy r106 use35)
(heavy r106 use36)
(cap r106 use36)
(using r106 use0)
(= (length-light r107) 4)
(= (length-medium r107) 41)
(= (length-heavy r107) 417)
(light r107 use0)
(light r107 use1)
(light r107 use2)
(light r107 use3)
(light r107 use4)
(light r107 use5)
(medium r107 use6)
(medium r107 use7)
(medium r107 use8)
(medium r107 use9)
(medium r107 use10)
(heavy r107 use11)
(heavy r107 use12)
(heavy r107 use13)
(cap r107 use13)
(using r107 use0)
(= (length-light r108) 13)
(= (length-medium r108) 131)
(= (length-heavy r108) 1313)
(light r108 use0)
(light r108 use1)
(light r108 use2)
(light r108 use3)
(light r108 use4)
(light r108 use5)
(medium r108 use6)
(medium r108 use7)
(medium r108 use8)
(medium r108 use9)
(medium r108 use10)
(medium r108 use11)
(heavy r108 use12)
(heavy r108 use13)
(heavy r108 use14)
(heavy r108 use15)
(cap r108 use15)
(using r108 use0)
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
(at v13 j83)
(togo v13 j73)
(at v169 j69)
(togo v169 j15)
(at v255 j78)
(togo v255 j8)
(at v111 j70)
(togo v111 j73)
(at v261 j78)
(togo v261 j8)
(at v14 j83)
(togo v14 j73)
(at v112 j70)
(togo v112 j73)
(at v177 j69)
(togo v177 j15)
(at v170 j69)
(togo v170 j15)
(at v256 j78)
(togo v256 j8)
(at v70 j15)
(togo v70 j73)
(at v262 j78)
(togo v262 j8)
(at v15 j83)
(togo v15 j73)
(at v113 j70)
(togo v113 j73)
(at v16 j83)
(togo v16 j73)
(at v171 j69)
(togo v171 j15)
(at v257 j78)
(togo v257 j8)
(at v71 j15)
(togo v71 j73)
(at v114 j70)
(togo v114 j73)
(at v17 j83)
(togo v17 j73)
)
(:goal (and
(at v13 j73)
(at v169 j15)
(at v255 j8)
(at v111 j73)
(at v261 j8)
(at v14 j73)
(at v112 j73)
(at v177 j15)
(at v170 j15)
(at v256 j8)
(at v70 j73)
(at v262 j8)
(at v15 j73)
(at v113 j73)
(at v16 j73)
(at v171 j15)
(at v257 j8)
(at v71 j73)
(at v114 j73)
(at v17 j73)
))
(:metric minimize (total-cost))
)