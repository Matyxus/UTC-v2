(define
(problem planned_sydney_problem160_180)
(:domain utc)
(:objects
 - junction
 - road
use0 - use
v45 v192 v462 v342 v193 v46 v463 v343 v194 v47 v464 v195 v344 v48 v465 v196 v49 v197 v466 v345 v198 v50 v467 - car
)
(:init
(= (total-cost) 0)
(at v45 j357)
(togo v45 j248)
(at v192 j241)
(togo v192 j316)
(at v462 j77)
(togo v462 j358)
(at v342 j87)
(togo v342 j315)
(at v193 j241)
(togo v193 j316)
(at v46 j357)
(togo v46 j248)
(at v463 j77)
(togo v463 j358)
(at v343 j87)
(togo v343 j315)
(at v194 j241)
(togo v194 j316)
(at v47 j357)
(togo v47 j248)
(at v464 j77)
(togo v464 j358)
(at v195 j241)
(togo v195 j316)
(at v344 j87)
(togo v344 j315)
(at v48 j357)
(togo v48 j248)
(at v465 j77)
(togo v465 j358)
(at v196 j241)
(togo v196 j316)
(at v49 j357)
(togo v49 j248)
(at v197 j241)
(togo v197 j316)
(at v466 j77)
(togo v466 j358)
(at v345 j87)
(togo v345 j315)
(at v198 j241)
(togo v198 j316)
(at v50 j357)
(togo v50 j248)
(at v467 j77)
(togo v467 j358)
)
(:goal (and
(at v45 j248)
(at v192 j316)
(at v462 j358)
(at v342 j315)
(at v193 j316)
(at v46 j248)
(at v463 j358)
(at v343 j315)
(at v194 j316)
(at v47 j248)
(at v464 j358)
(at v195 j316)
(at v344 j315)
(at v48 j248)
(at v465 j358)
(at v196 j316)
(at v49 j248)
(at v197 j316)
(at v466 j358)
(at v345 j315)
(at v198 j316)
(at v50 j248)
(at v467 j358)
))
(:metric minimize (total-cost))
)