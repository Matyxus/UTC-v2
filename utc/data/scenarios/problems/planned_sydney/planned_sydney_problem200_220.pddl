(define
(problem planned_sydney_problem200_220)
(:domain utc)
(:objects
 - junction
 - road
use0 - use
v473 v56 v206 v351 v474 v57 v207 v352 v475 v208 v58 v209 v476 v59 v353 v210 v477 v60 v354 v211 v478 v61 v212 - car
)
(:init
(= (total-cost) 0)
(at v473 j77)
(togo v473 j358)
(at v56 j357)
(togo v56 j248)
(at v206 j241)
(togo v206 j316)
(at v351 j87)
(togo v351 j315)
(at v474 j77)
(togo v474 j358)
(at v57 j357)
(togo v57 j248)
(at v207 j241)
(togo v207 j316)
(at v352 j87)
(togo v352 j315)
(at v475 j77)
(togo v475 j358)
(at v208 j241)
(togo v208 j316)
(at v58 j357)
(togo v58 j248)
(at v209 j241)
(togo v209 j316)
(at v476 j77)
(togo v476 j358)
(at v59 j357)
(togo v59 j248)
(at v353 j87)
(togo v353 j315)
(at v210 j241)
(togo v210 j316)
(at v477 j77)
(togo v477 j358)
(at v60 j357)
(togo v60 j248)
(at v354 j87)
(togo v354 j315)
(at v211 j241)
(togo v211 j316)
(at v478 j77)
(togo v478 j358)
(at v61 j357)
(togo v61 j248)
(at v212 j241)
(togo v212 j316)
)
(:goal (and
(at v473 j358)
(at v56 j248)
(at v206 j316)
(at v351 j315)
(at v474 j358)
(at v57 j248)
(at v207 j316)
(at v352 j315)
(at v475 j358)
(at v208 j316)
(at v58 j248)
(at v209 j316)
(at v476 j358)
(at v59 j248)
(at v353 j315)
(at v210 j316)
(at v477 j358)
(at v60 j248)
(at v354 j315)
(at v211 j316)
(at v478 j358)
(at v61 j248)
(at v212 j316)
))
(:metric minimize (total-cost))
)