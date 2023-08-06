from numpy import arange
from Engine import Framework, Table,Cylinder,CrankTrain,GasProperty
# from Engine.Cylinder import CylinderPressure,CylinderGeometry,HeatReleaseData

eng=Framework.Engine("single")

C1=Cylinder.Cylinder(eng)

Geo=Cylinder.CylinderGeometry("single").init(126e-3,155e-3,17,310e-3)

mix=GasProperty.DieselMixture(Geo.VH*1.e5/287.15/300,0,30e-6)

Cran=CrankTrain.CrankTrain(eng).init(1400,
-110,
Geo,
[C1],
[0])


T=Table.ArrayTable().init(".//data//1400pre.csv")

T.table[1]*=1.e5

# T.plot(1)


# print(T.interp1(arange(360,540)))


Pre=Cylinder.Combustion.CylinderPressure(C1).init(T)

# Pre.PVDiagram().open()
# Pre.smooth(4).plot()

Pre.netHRR(mix).plot()

Pre.analyze()

# Pre.ploytropicIndex().plot()

Pre.PVDiagram().plot()

Pre.LogPLogV().plot()


# T.show()

# T.readcsv("1400intake.csv")

# T.plot()