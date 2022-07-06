In file:
vehicle: {
	"object" : 
	"init": "(togo v{vehicle_id} {arrival_junction})"
	"goal": "(at v7 j0)"
}

process_junctions():
	raiseNot...


process_junctions():
	for junction in junctions.values():
		string = get(network["junctions"]) <- "(availableflow {incomin_route} {out_coming} {junction_id})"
		for incoming in junctions.get_incoming():
			...



network: {
	"junction" : {
		"object" : 
		"init": ["(availableflow {incomin_route} {out_coming} {junction_id})",  (= (flow r4 r6e int1) 3)]
		"goal": "(at v7 j0)"
	}
	"edge" : {
		"object" : 
		"init": "(togo v{vehicle_id} {arrival_junction})"
		"goal": "(at v7 j0)"
	}
}


;; intersection 1
    (= (greentime int1) 0)
     (= (token int1)  10)
     (= (maxtoken int1)  20)
     (= (tokenvalue r4 int1)  10)
     (= (tokenvalue r6w int1)  20) 
    (= (maxgreentime int1) 40)
    (= (mingreentime int1) 5)
    (= (flow r4 r6e int1) 3)
    (= (flow r4 r5 int1) 5)
    (= (flow r6w r5 int1) 2)
    (availableflow r4 r6e int1)
    (availableflow r4 r5 int1)
    (availableflow r6w r5 int1)
    (active int1 r4)
    (active int1 r6w)


trafic_light: {
	"object" : 
	"init": "(togo v{vehicle_id} {arrival_junction})"
	"goal": "(at v7 j0)"
}




In program:
Vehicle: {vehicle_id: 15, .....}










