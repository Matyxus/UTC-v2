(define
(problem dejvice_test_similarity_planned_problem20_40)
(:domain utc)
(:objects
j15 j23 j24 j27 j31 j36 j37 j4 j41 j42 j43 j44 j45 j46 j47 j48 j49 j50 j51 j52 j53 j55 j6 j60 j62 j63 j65 j69 j70 j73 j76 j78 j8 j83 j87 j89 j90 j91 j93 j94 - junction
r0 r1 r3 r5 r7 r8 r9 r10 r14 r16 r17 r18 r19 r21 r22 r23 r25 r26 r27 r30 r31 r32 r34 r35 r36 r37 r39 r40 r42 r43 r44 r45 r46 r47 r49 r55 r56 r57 r58 r60 r61 r62 r63 r64 r66 r67 r68 r70 r72 r73 r74 r75 r76 r77 r78 r79 r80 r81 r82 r83 r84 r85 r86 r87 r88 r89 r90 r91 r92 r96 r97 r98 r99 r100 r101 r102 - road
use0 use1 use2 use3 use4 use5 use6 use7 use8 use9 use10 use11 use12 use13 use14 use15 use16 use17 use18 use19 use20 use21 use22 use23 use24 use25 use26 use27 use28 use29 use30 use31 use32 use33 use34 use35 use36 use37 use38 use39 use40 use41 use42 use43 use44 use45 use46 use47 use48 use49 - use
v164 v250 v5 v103 v66 v6 v104 v165 v251 v7 v105 v8 v166 v252 v106 - car
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
(connected j31 r21 j37)
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
(connected j6 r37 j36)
(connected j15 r39 j27)
(connected j49 r40 j93)
(connected j55 r42 j52)
(connected j48 r43 j55)
(connected j63 r44 j42)
(connected j41 r45 j43)
(connected j44 r46 j45)
(connected j46 r47 j93)
(connected j48 r49 j47)
(connected j89 r55 j90)
(connected j65 r56 j90)
(connected j45 r57 j60)
(connected j91 r58 j31)
(connected j36 r60 j94)
(connected j78 r61 j93)
(connected j53 r62 j52)
(connected j24 r63 j53)
(connected j23 r64 j91)
(connected j23 r66 j24)
(connected j46 r67 j44)
(connected j50 r68 j52)
(connected j46 r70 j47)
(connected j94 r72 j89)
(connected j4 r73 j50)
(connected j87 r74 j50)
(connected j70 r75 j87)
(connected j43 r76 j42)
(connected j52 r77 j55)
(connected j55 r78 j48)
(connected j42 r79 j63)
(connected j41 r80 j42)
(connected j47 r81 j48)
(connected j37 r82 j36)
(connected j91 r83 j37)
(connected j45 r84 j62)
(connected j83 r85 j90)
(connected j46 r86 j45)
(connected j87 r87 j49)
(connected j42 r88 j43)
(connected j42 r89 j41)
(connected j50 r90 j49)
(connected j36 r91 j42)
(connected j90 r92 j73)
(connected j60 r96 j63)
(connected j91 r97 j23)
(connected j42 r98 j36)
(connected j4 r99 j27)
(connected j27 r100 j15)
(connected j90 r101 j8)
(connected j76 r102 j53)
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
(= (length-medium r14) 108)
(= (length-heavy r14) 1088)
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
(medium r14 use13)
(heavy r14 use14)
(heavy r14 use15)
(heavy r14 use16)
(heavy r14 use17)
(cap r14 use17)
(using r14 use0)
(= (length-light r16) 8)
(= (length-medium r16) 88)
(= (length-heavy r16) 882)
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
(medium r16 use13)
(heavy r16 use14)
(heavy r16 use15)
(heavy r16 use16)
(heavy r16 use17)
(cap r16 use17)
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
(= (length-light r21) 16)
(= (length-medium r21) 165)
(= (length-heavy r21) 1652)
(light r21 use0)
(light r21 use1)
(light r21 use2)
(light r21 use3)
(light r21 use4)
(light r21 use5)
(light r21 use6)
(light r21 use7)
(light r21 use8)
(medium r21 use9)
(medium r21 use10)
(medium r21 use11)
(medium r21 use12)
(medium r21 use13)
(medium r21 use14)
(medium r21 use15)
(medium r21 use16)
(medium r21 use17)
(medium r21 use18)
(heavy r21 use19)
(heavy r21 use20)
(heavy r21 use21)
(heavy r21 use22)
(heavy r21 use23)
(heavy r21 use24)
(cap r21 use24)
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
(= (length-medium r26) 274)
(= (length-heavy r26) 2744)
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
(= (length-light r37) 16)
(= (length-medium r37) 164)
(= (length-heavy r37) 1643)
(light r37 use0)
(light r37 use1)
(light r37 use2)
(light r37 use3)
(light r37 use4)
(light r37 use5)
(light r37 use6)
(light r37 use7)
(medium r37 use8)
(medium r37 use9)
(medium r37 use10)
(medium r37 use11)
(medium r37 use12)
(medium r37 use13)
(medium r37 use14)
(medium r37 use15)
(heavy r37 use16)
(heavy r37 use17)
(heavy r37 use18)
(heavy r37 use19)
(cap r37 use19)
(using r37 use0)
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
(= (length-light r40) 24)
(= (length-medium r40) 247)
(= (length-heavy r40) 2471)
(light r40 use0)
(light r40 use1)
(light r40 use2)
(light r40 use3)
(light r40 use4)
(light r40 use5)
(light r40 use6)
(light r40 use7)
(light r40 use8)
(light r40 use9)
(light r40 use10)
(light r40 use11)
(light r40 use12)
(light r40 use13)
(light r40 use14)
(light r40 use15)
(light r40 use16)
(light r40 use17)
(medium r40 use18)
(medium r40 use19)
(medium r40 use20)
(medium r40 use21)
(medium r40 use22)
(medium r40 use23)
(medium r40 use24)
(medium r40 use25)
(medium r40 use26)
(medium r40 use27)
(medium r40 use28)
(medium r40 use29)
(medium r40 use30)
(medium r40 use31)
(medium r40 use32)
(medium r40 use33)
(medium r40 use34)
(medium r40 use35)
(medium r40 use36)
(medium r40 use37)
(heavy r40 use38)
(heavy r40 use39)
(heavy r40 use40)
(heavy r40 use41)
(heavy r40 use42)
(heavy r40 use43)
(heavy r40 use44)
(heavy r40 use45)
(heavy r40 use46)
(heavy r40 use47)
(heavy r40 use48)
(heavy r40 use49)
(cap r40 use49)
(using r40 use0)
(= (length-light r42) 4)
(= (length-medium r42) 41)
(= (length-heavy r42) 417)
(light r42 use0)
(light r42 use1)
(medium r42 use2)
(medium r42 use3)
(heavy r42 use4)
(cap r42 use4)
(using r42 use0)
(= (length-light r43) 5)
(= (length-medium r43) 58)
(= (length-heavy r43) 581)
(light r43 use0)
(light r43 use1)
(light r43 use2)
(medium r43 use3)
(medium r43 use4)
(heavy r43 use5)
(heavy r43 use6)
(cap r43 use6)
(using r43 use0)
(= (length-light r44) 10)
(= (length-medium r44) 107)
(= (length-heavy r44) 1076)
(light r44 use0)
(light r44 use1)
(light r44 use2)
(light r44 use3)
(light r44 use4)
(medium r44 use5)
(medium r44 use6)
(medium r44 use7)
(medium r44 use8)
(medium r44 use9)
(heavy r44 use10)
(heavy r44 use11)
(heavy r44 use12)
(cap r44 use12)
(using r44 use0)
(= (length-light r45) 4)
(= (length-medium r45) 46)
(= (length-heavy r45) 461)
(light r45 use0)
(light r45 use1)
(light r45 use2)
(medium r45 use3)
(medium r45 use4)
(heavy r45 use5)
(cap r45 use5)
(using r45 use0)
(= (length-light r46) 1)
(= (length-medium r46) 18)
(= (length-heavy r46) 186)
(light r46 use0)
(light r46 use1)
(medium r46 use2)
(heavy r46 use3)
(cap r46 use3)
(using r46 use0)
(= (length-light r47) 5)
(= (length-medium r47) 57)
(= (length-heavy r47) 576)
(light r47 use0)
(light r47 use1)
(light r47 use2)
(light r47 use3)
(light r47 use4)
(medium r47 use5)
(medium r47 use6)
(medium r47 use7)
(medium r47 use8)
(heavy r47 use9)
(heavy r47 use10)
(heavy r47 use11)
(cap r47 use11)
(using r47 use0)
(= (length-light r49) 16)
(= (length-medium r49) 165)
(= (length-heavy r49) 1650)
(light r49 use0)
(light r49 use1)
(light r49 use2)
(light r49 use3)
(light r49 use4)
(light r49 use5)
(light r49 use6)
(light r49 use7)
(medium r49 use8)
(medium r49 use9)
(medium r49 use10)
(medium r49 use11)
(medium r49 use12)
(medium r49 use13)
(medium r49 use14)
(medium r49 use15)
(heavy r49 use16)
(heavy r49 use17)
(heavy r49 use18)
(heavy r49 use19)
(cap r49 use19)
(using r49 use0)
(= (length-light r55) 3)
(= (length-medium r55) 35)
(= (length-heavy r55) 351)
(light r55 use0)
(light r55 use1)
(light r55 use2)
(light r55 use3)
(light r55 use4)
(light r55 use5)
(light r55 use6)
(light r55 use7)
(light r55 use8)
(medium r55 use9)
(medium r55 use10)
(medium r55 use11)
(medium r55 use12)
(medium r55 use13)
(medium r55 use14)
(medium r55 use15)
(medium r55 use16)
(medium r55 use17)
(heavy r55 use18)
(heavy r55 use19)
(heavy r55 use20)
(heavy r55 use21)
(heavy r55 use22)
(cap r55 use22)
(using r55 use0)
(= (length-light r56) 1)
(= (length-medium r56) 19)
(= (length-heavy r56) 198)
(light r56 use0)
(light r56 use1)
(light r56 use2)
(medium r56 use3)
(medium r56 use4)
(medium r56 use5)
(heavy r56 use6)
(heavy r56 use7)
(cap r56 use7)
(using r56 use0)
(= (length-light r57) 12)
(= (length-medium r57) 127)
(= (length-heavy r57) 1270)
(light r57 use0)
(light r57 use1)
(light r57 use2)
(light r57 use3)
(light r57 use4)
(light r57 use5)
(light r57 use6)
(light r57 use7)
(light r57 use8)
(light r57 use9)
(medium r57 use10)
(medium r57 use11)
(medium r57 use12)
(medium r57 use13)
(medium r57 use14)
(medium r57 use15)
(medium r57 use16)
(medium r57 use17)
(medium r57 use18)
(medium r57 use19)
(heavy r57 use20)
(heavy r57 use21)
(heavy r57 use22)
(heavy r57 use23)
(heavy r57 use24)
(heavy r57 use25)
(cap r57 use25)
(using r57 use0)
(= (length-light r58) 23)
(= (length-medium r58) 232)
(= (length-heavy r58) 2320)
(light r58 use0)
(light r58 use1)
(light r58 use2)
(light r58 use3)
(light r58 use4)
(light r58 use5)
(light r58 use6)
(light r58 use7)
(light r58 use8)
(light r58 use9)
(light r58 use10)
(light r58 use11)
(light r58 use12)
(light r58 use13)
(light r58 use14)
(light r58 use15)
(light r58 use16)
(light r58 use17)
(medium r58 use18)
(medium r58 use19)
(medium r58 use20)
(medium r58 use21)
(medium r58 use22)
(medium r58 use23)
(medium r58 use24)
(medium r58 use25)
(medium r58 use26)
(medium r58 use27)
(medium r58 use28)
(medium r58 use29)
(medium r58 use30)
(medium r58 use31)
(medium r58 use32)
(medium r58 use33)
(medium r58 use34)
(medium r58 use35)
(medium r58 use36)
(medium r58 use37)
(heavy r58 use38)
(heavy r58 use39)
(heavy r58 use40)
(heavy r58 use41)
(heavy r58 use42)
(heavy r58 use43)
(heavy r58 use44)
(heavy r58 use45)
(heavy r58 use46)
(heavy r58 use47)
(heavy r58 use48)
(heavy r58 use49)
(cap r58 use49)
(using r58 use0)
(= (length-light r60) 4)
(= (length-medium r60) 49)
(= (length-heavy r60) 496)
(light r60 use0)
(light r60 use1)
(light r60 use2)
(light r60 use3)
(medium r60 use4)
(medium r60 use5)
(medium r60 use6)
(medium r60 use7)
(heavy r60 use8)
(heavy r60 use9)
(cap r60 use9)
(using r60 use0)
(= (length-light r61) 11)
(= (length-medium r61) 118)
(= (length-heavy r61) 1188)
(light r61 use0)
(light r61 use1)
(light r61 use2)
(light r61 use3)
(light r61 use4)
(light r61 use5)
(light r61 use6)
(medium r61 use7)
(medium r61 use8)
(medium r61 use9)
(medium r61 use10)
(medium r61 use11)
(medium r61 use12)
(medium r61 use13)
(heavy r61 use14)
(heavy r61 use15)
(heavy r61 use16)
(heavy r61 use17)
(heavy r61 use18)
(cap r61 use18)
(using r61 use0)
(= (length-light r62) 11)
(= (length-medium r62) 111)
(= (length-heavy r62) 1112)
(light r62 use0)
(light r62 use1)
(light r62 use2)
(light r62 use3)
(light r62 use4)
(light r62 use5)
(light r62 use6)
(light r62 use7)
(medium r62 use8)
(medium r62 use9)
(medium r62 use10)
(medium r62 use11)
(medium r62 use12)
(medium r62 use13)
(medium r62 use14)
(medium r62 use15)
(heavy r62 use16)
(heavy r62 use17)
(heavy r62 use18)
(heavy r62 use19)
(cap r62 use19)
(using r62 use0)
(= (length-light r63) 9)
(= (length-medium r63) 96)
(= (length-heavy r63) 967)
(light r63 use0)
(light r63 use1)
(light r63 use2)
(light r63 use3)
(light r63 use4)
(light r63 use5)
(light r63 use6)
(medium r63 use7)
(medium r63 use8)
(medium r63 use9)
(medium r63 use10)
(medium r63 use11)
(medium r63 use12)
(medium r63 use13)
(heavy r63 use14)
(heavy r63 use15)
(heavy r63 use16)
(heavy r63 use17)
(cap r63 use17)
(using r63 use0)
(= (length-light r64) 5)
(= (length-medium r64) 54)
(= (length-heavy r64) 542)
(light r64 use0)
(light r64 use1)
(light r64 use2)
(light r64 use3)
(light r64 use4)
(medium r64 use5)
(medium r64 use6)
(medium r64 use7)
(medium r64 use8)
(heavy r64 use9)
(heavy r64 use10)
(cap r64 use10)
(using r64 use0)
(= (length-light r66) 8)
(= (length-medium r66) 88)
(= (length-heavy r66) 881)
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
(medium r66 use13)
(heavy r66 use14)
(heavy r66 use15)
(heavy r66 use16)
(heavy r66 use17)
(cap r66 use17)
(using r66 use0)
(= (length-light r67) 1)
(= (length-medium r67) 10)
(= (length-heavy r67) 107)
(light r67 use0)
(light r67 use1)
(medium r67 use2)
(cap r67 use2)
(using r67 use0)
(= (length-light r68) 6)
(= (length-medium r68) 60)
(= (length-heavy r68) 609)
(light r68 use0)
(light r68 use1)
(light r68 use2)
(light r68 use3)
(medium r68 use4)
(medium r68 use5)
(medium r68 use6)
(medium r68 use7)
(heavy r68 use8)
(heavy r68 use9)
(cap r68 use9)
(using r68 use0)
(= (length-light r70) 19)
(= (length-medium r70) 196)
(= (length-heavy r70) 1967)
(light r70 use0)
(light r70 use1)
(light r70 use2)
(light r70 use3)
(light r70 use4)
(light r70 use5)
(light r70 use6)
(light r70 use7)
(light r70 use8)
(medium r70 use9)
(medium r70 use10)
(medium r70 use11)
(medium r70 use12)
(medium r70 use13)
(medium r70 use14)
(medium r70 use15)
(medium r70 use16)
(medium r70 use17)
(heavy r70 use18)
(heavy r70 use19)
(heavy r70 use20)
(heavy r70 use21)
(heavy r70 use22)
(heavy r70 use23)
(cap r70 use23)
(using r70 use0)
(= (length-light r72) 3)
(= (length-medium r72) 34)
(= (length-heavy r72) 349)
(light r72 use0)
(light r72 use1)
(light r72 use2)
(medium r72 use3)
(medium r72 use4)
(heavy r72 use5)
(heavy r72 use6)
(cap r72 use6)
(using r72 use0)
(= (length-light r73) 4)
(= (length-medium r73) 40)
(= (length-heavy r73) 409)
(light r73 use0)
(light r73 use1)
(light r73 use2)
(light r73 use3)
(medium r73 use4)
(medium r73 use5)
(medium r73 use6)
(heavy r73 use7)
(heavy r73 use8)
(cap r73 use8)
(using r73 use0)
(= (length-light r74) 8)
(= (length-medium r74) 80)
(= (length-heavy r74) 809)
(light r74 use0)
(light r74 use1)
(light r74 use2)
(light r74 use3)
(light r74 use4)
(medium r74 use5)
(medium r74 use6)
(medium r74 use7)
(medium r74 use8)
(medium r74 use9)
(heavy r74 use10)
(heavy r74 use11)
(heavy r74 use12)
(cap r74 use12)
(using r74 use0)
(= (length-light r75) 5)
(= (length-medium r75) 52)
(= (length-heavy r75) 525)
(light r75 use0)
(light r75 use1)
(light r75 use2)
(light r75 use3)
(medium r75 use4)
(medium r75 use5)
(medium r75 use6)
(heavy r75 use7)
(heavy r75 use8)
(cap r75 use8)
(using r75 use0)
(= (length-light r76) 1)
(= (length-medium r76) 16)
(= (length-heavy r76) 166)
(light r76 use0)
(light r76 use1)
(cap r76 use1)
(using r76 use0)
(= (length-light r77) 4)
(= (length-medium r77) 41)
(= (length-heavy r77) 417)
(light r77 use0)
(light r77 use1)
(medium r77 use2)
(medium r77 use3)
(heavy r77 use4)
(cap r77 use4)
(using r77 use0)
(= (length-light r78) 5)
(= (length-medium r78) 58)
(= (length-heavy r78) 581)
(light r78 use0)
(light r78 use1)
(light r78 use2)
(medium r78 use3)
(medium r78 use4)
(heavy r78 use5)
(heavy r78 use6)
(cap r78 use6)
(using r78 use0)
(= (length-light r79) 10)
(= (length-medium r79) 107)
(= (length-heavy r79) 1076)
(light r79 use0)
(light r79 use1)
(light r79 use2)
(light r79 use3)
(light r79 use4)
(medium r79 use5)
(medium r79 use6)
(medium r79 use7)
(medium r79 use8)
(medium r79 use9)
(heavy r79 use10)
(heavy r79 use11)
(heavy r79 use12)
(cap r79 use12)
(using r79 use0)
(= (length-light r80) 1)
(= (length-medium r80) 18)
(= (length-heavy r80) 180)
(light r80 use0)
(light r80 use1)
(medium r80 use2)
(cap r80 use2)
(using r80 use0)
(= (length-light r81) 16)
(= (length-medium r81) 164)
(= (length-heavy r81) 1649)
(light r81 use0)
(light r81 use1)
(light r81 use2)
(light r81 use3)
(light r81 use4)
(light r81 use5)
(light r81 use6)
(light r81 use7)
(medium r81 use8)
(medium r81 use9)
(medium r81 use10)
(medium r81 use11)
(medium r81 use12)
(medium r81 use13)
(medium r81 use14)
(medium r81 use15)
(heavy r81 use16)
(heavy r81 use17)
(heavy r81 use18)
(heavy r81 use19)
(cap r81 use19)
(using r81 use0)
(= (length-light r82) 5)
(= (length-medium r82) 55)
(= (length-heavy r82) 557)
(light r82 use0)
(light r82 use1)
(light r82 use2)
(light r82 use3)
(light r82 use4)
(light r82 use5)
(light r82 use6)
(medium r82 use7)
(medium r82 use8)
(medium r82 use9)
(medium r82 use10)
(medium r82 use11)
(medium r82 use12)
(medium r82 use13)
(heavy r82 use14)
(heavy r82 use15)
(heavy r82 use16)
(heavy r82 use17)
(cap r82 use17)
(using r82 use0)
(= (length-light r83) 5)
(= (length-medium r83) 56)
(= (length-heavy r83) 564)
(light r83 use0)
(light r83 use1)
(light r83 use2)
(light r83 use3)
(light r83 use4)
(light r83 use5)
(light r83 use6)
(medium r83 use7)
(medium r83 use8)
(medium r83 use9)
(medium r83 use10)
(medium r83 use11)
(medium r83 use12)
(medium r83 use13)
(heavy r83 use14)
(heavy r83 use15)
(heavy r83 use16)
(heavy r83 use17)
(cap r83 use17)
(using r83 use0)
(= (length-light r84) 21)
(= (length-medium r84) 215)
(= (length-heavy r84) 2150)
(light r84 use0)
(light r84 use1)
(light r84 use2)
(light r84 use3)
(light r84 use4)
(light r84 use5)
(light r84 use6)
(light r84 use7)
(light r84 use8)
(light r84 use9)
(light r84 use10)
(light r84 use11)
(light r84 use12)
(light r84 use13)
(light r84 use14)
(light r84 use15)
(medium r84 use16)
(medium r84 use17)
(medium r84 use18)
(medium r84 use19)
(medium r84 use20)
(medium r84 use21)
(medium r84 use22)
(medium r84 use23)
(medium r84 use24)
(medium r84 use25)
(medium r84 use26)
(medium r84 use27)
(medium r84 use28)
(medium r84 use29)
(medium r84 use30)
(medium r84 use31)
(medium r84 use32)
(heavy r84 use33)
(heavy r84 use34)
(heavy r84 use35)
(heavy r84 use36)
(heavy r84 use37)
(heavy r84 use38)
(heavy r84 use39)
(heavy r84 use40)
(heavy r84 use41)
(heavy r84 use42)
(cap r84 use42)
(using r84 use0)
(= (length-light r85) 1)
(= (length-medium r85) 12)
(= (length-heavy r85) 127)
(light r85 use0)
(light r85 use1)
(light r85 use2)
(light r85 use3)
(medium r85 use4)
(medium r85 use5)
(medium r85 use6)
(heavy r85 use7)
(heavy r85 use8)
(cap r85 use8)
(using r85 use0)
(= (length-light r86) 1)
(= (length-medium r86) 15)
(= (length-heavy r86) 154)
(light r86 use0)
(light r86 use1)
(medium r86 use2)
(heavy r86 use3)
(cap r86 use3)
(using r86 use0)
(= (length-light r87) 11)
(= (length-medium r87) 111)
(= (length-heavy r87) 1119)
(light r87 use0)
(light r87 use1)
(light r87 use2)
(light r87 use3)
(light r87 use4)
(light r87 use5)
(light r87 use6)
(light r87 use7)
(light r87 use8)
(medium r87 use9)
(medium r87 use10)
(medium r87 use11)
(medium r87 use12)
(medium r87 use13)
(medium r87 use14)
(medium r87 use15)
(medium r87 use16)
(medium r87 use17)
(heavy r87 use18)
(heavy r87 use19)
(heavy r87 use20)
(heavy r87 use21)
(heavy r87 use22)
(cap r87 use22)
(using r87 use0)
(= (length-light r88) 1)
(= (length-medium r88) 16)
(= (length-heavy r88) 166)
(light r88 use0)
(light r88 use1)
(cap r88 use1)
(using r88 use0)
(= (length-light r89) 1)
(= (length-medium r89) 18)
(= (length-heavy r89) 180)
(light r89 use0)
(light r89 use1)
(medium r89 use2)
(cap r89 use2)
(using r89 use0)
(= (length-light r90) 5)
(= (length-medium r90) 56)
(= (length-heavy r90) 562)
(light r90 use0)
(light r90 use1)
(light r90 use2)
(light r90 use3)
(light r90 use4)
(medium r90 use5)
(medium r90 use6)
(medium r90 use7)
(medium r90 use8)
(heavy r90 use9)
(heavy r90 use10)
(heavy r90 use11)
(cap r90 use11)
(using r90 use0)
(= (length-light r91) 11)
(= (length-medium r91) 112)
(= (length-heavy r91) 1126)
(light r91 use0)
(light r91 use1)
(light r91 use2)
(light r91 use3)
(light r91 use4)
(light r91 use5)
(medium r91 use6)
(medium r91 use7)
(medium r91 use8)
(medium r91 use9)
(medium r91 use10)
(heavy r91 use11)
(heavy r91 use12)
(heavy r91 use13)
(cap r91 use13)
(using r91 use0)
(= (length-light r92) 8)
(= (length-medium r92) 83)
(= (length-heavy r92) 838)
(light r92 use0)
(light r92 use1)
(light r92 use2)
(light r92 use3)
(light r92 use4)
(light r92 use5)
(light r92 use6)
(light r92 use7)
(light r92 use8)
(light r92 use9)
(light r92 use10)
(light r92 use11)
(light r92 use12)
(medium r92 use13)
(medium r92 use14)
(medium r92 use15)
(medium r92 use16)
(medium r92 use17)
(medium r92 use18)
(medium r92 use19)
(medium r92 use20)
(medium r92 use21)
(medium r92 use22)
(medium r92 use23)
(medium r92 use24)
(medium r92 use25)
(heavy r92 use26)
(heavy r92 use27)
(heavy r92 use28)
(heavy r92 use29)
(heavy r92 use30)
(heavy r92 use31)
(heavy r92 use32)
(heavy r92 use33)
(cap r92 use33)
(using r92 use0)
(= (length-light r96) 4)
(= (length-medium r96) 47)
(= (length-heavy r96) 473)
(light r96 use0)
(light r96 use1)
(light r96 use2)
(light r96 use3)
(medium r96 use4)
(medium r96 use5)
(medium r96 use6)
(medium r96 use7)
(heavy r96 use8)
(heavy r96 use9)
(cap r96 use9)
(using r96 use0)
(= (length-light r97) 5)
(= (length-medium r97) 54)
(= (length-heavy r97) 542)
(light r97 use0)
(light r97 use1)
(light r97 use2)
(light r97 use3)
(light r97 use4)
(medium r97 use5)
(medium r97 use6)
(medium r97 use7)
(medium r97 use8)
(heavy r97 use9)
(heavy r97 use10)
(cap r97 use10)
(using r97 use0)
(= (length-light r98) 11)
(= (length-medium r98) 112)
(= (length-heavy r98) 1127)
(light r98 use0)
(light r98 use1)
(light r98 use2)
(light r98 use3)
(light r98 use4)
(light r98 use5)
(medium r98 use6)
(medium r98 use7)
(medium r98 use8)
(medium r98 use9)
(medium r98 use10)
(heavy r98 use11)
(heavy r98 use12)
(heavy r98 use13)
(cap r98 use13)
(using r98 use0)
(= (length-light r99) 5)
(= (length-medium r99) 52)
(= (length-heavy r99) 522)
(light r99 use0)
(light r99 use1)
(light r99 use2)
(light r99 use3)
(light r99 use4)
(light r99 use5)
(light r99 use6)
(medium r99 use7)
(medium r99 use8)
(medium r99 use9)
(medium r99 use10)
(medium r99 use11)
(medium r99 use12)
(heavy r99 use13)
(heavy r99 use14)
(heavy r99 use15)
(heavy r99 use16)
(cap r99 use16)
(using r99 use0)
(= (length-light r100) 11)
(= (length-medium r100) 113)
(= (length-heavy r100) 1137)
(light r100 use0)
(light r100 use1)
(light r100 use2)
(light r100 use3)
(light r100 use4)
(light r100 use5)
(light r100 use6)
(light r100 use7)
(light r100 use8)
(light r100 use9)
(light r100 use10)
(light r100 use11)
(light r100 use12)
(light r100 use13)
(medium r100 use14)
(medium r100 use15)
(medium r100 use16)
(medium r100 use17)
(medium r100 use18)
(medium r100 use19)
(medium r100 use20)
(medium r100 use21)
(medium r100 use22)
(medium r100 use23)
(medium r100 use24)
(medium r100 use25)
(medium r100 use26)
(medium r100 use27)
(heavy r100 use28)
(heavy r100 use29)
(heavy r100 use30)
(heavy r100 use31)
(heavy r100 use32)
(heavy r100 use33)
(heavy r100 use34)
(heavy r100 use35)
(heavy r100 use36)
(cap r100 use36)
(using r100 use0)
(= (length-light r101) 4)
(= (length-medium r101) 41)
(= (length-heavy r101) 417)
(light r101 use0)
(light r101 use1)
(light r101 use2)
(light r101 use3)
(light r101 use4)
(light r101 use5)
(medium r101 use6)
(medium r101 use7)
(medium r101 use8)
(medium r101 use9)
(medium r101 use10)
(heavy r101 use11)
(heavy r101 use12)
(heavy r101 use13)
(cap r101 use13)
(using r101 use0)
(= (length-light r102) 13)
(= (length-medium r102) 131)
(= (length-heavy r102) 1313)
(light r102 use0)
(light r102 use1)
(light r102 use2)
(light r102 use3)
(light r102 use4)
(light r102 use5)
(medium r102 use6)
(medium r102 use7)
(medium r102 use8)
(medium r102 use9)
(medium r102 use10)
(medium r102 use11)
(heavy r102 use12)
(heavy r102 use13)
(heavy r102 use14)
(heavy r102 use15)
(cap r102 use15)
(using r102 use0)
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
(at v164 j69)
(togo v164 j15)
(at v250 j78)
(togo v250 j8)
(at v5 j83)
(togo v5 j73)
(at v103 j70)
(togo v103 j73)
(at v66 j15)
(togo v66 j73)
(at v6 j83)
(togo v6 j73)
(at v104 j70)
(togo v104 j73)
(at v165 j69)
(togo v165 j15)
(at v251 j78)
(togo v251 j8)
(at v7 j83)
(togo v7 j73)
(at v105 j70)
(togo v105 j73)
(at v8 j83)
(togo v8 j73)
(at v166 j69)
(togo v166 j15)
(at v252 j78)
(togo v252 j8)
(at v106 j70)
(togo v106 j73)
)
(:goal (and
(at v164 j15)
(at v250 j8)
(at v5 j73)
(at v103 j73)
(at v66 j73)
(at v6 j73)
(at v104 j73)
(at v165 j15)
(at v251 j8)
(at v7 j73)
(at v105 j73)
(at v8 j73)
(at v166 j15)
(at v252 j8)
(at v106 j73)
))
(:metric minimize (total-cost))
)