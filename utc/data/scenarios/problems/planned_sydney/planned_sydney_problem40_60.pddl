(define
(problem planned_sydney_problem40_60)
(:domain utc)
(:objects
 - junction
 - road
use0 - use
v427 v150 v12 v315 v428 v151 v13 v152 v429 v316 v14 v153 v430 v317 v15 v154 v431 v155 v318 v16 v432 v156 - car
)
(:init
(= (total-cost) 0)
(at v427 j77)
(togo v427 j358)
(at v150 j241)
(togo v150 j316)
(at v12 j357)
(togo v12 j248)
(at v315 j87)
(togo v315 j315)
(at v428 j77)
(togo v428 j358)
(at v151 j241)
(togo v151 j316)
(at v13 j357)
(togo v13 j248)
(at v152 j241)
(togo v152 j316)
(at v429 j77)
(togo v429 j358)
(at v316 j87)
(togo v316 j315)
(at v14 j357)
(togo v14 j248)
(at v153 j241)
(togo v153 j316)
(at v430 j77)
(togo v430 j358)
(at v317 j87)
(togo v317 j315)
(at v15 j357)
(togo v15 j248)
(at v154 j241)
(togo v154 j316)
(at v431 j77)
(togo v431 j358)
(at v155 j241)
(togo v155 j316)
(at v318 j87)
(togo v318 j315)
(at v16 j357)
(togo v16 j248)
(at v432 j77)
(togo v432 j358)
(at v156 j241)
(togo v156 j316)
)
(:goal (and
(at v427 j358)
(at v150 j316)
(at v12 j248)
(at v315 j315)
(at v428 j358)
(at v151 j316)
(at v13 j248)
(at v152 j316)
(at v429 j358)
(at v316 j315)
(at v14 j248)
(at v153 j316)
(at v430 j358)
(at v317 j315)
(at v15 j248)
(at v154 j316)
(at v431 j358)
(at v155 j316)
(at v318 j315)
(at v16 j248)
(at v432 j358)
(at v156 j316)
))
(:metric minimize (total-cost))
)