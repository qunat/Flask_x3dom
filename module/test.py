from CADcreator import CADcreatorClass

myCADProc=CADcreatorClass()
newfile=myCADProc.Output_stp_data('./files/test',series= 'SFU01604-4',fixted_side='BK型号',support_side='BF型号',trip_distance=1000)
json=myCADProc.return_json()
print(newfile)

