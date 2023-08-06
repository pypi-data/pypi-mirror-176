from Engine import Framework,Table

from Engine import Cylinder as C

W=C.Combustion.ZeroD.SingleWiebe()

W.init(-20,40,2,6.908)

W.data.plot(1)

WW=C.HeatReleaseData(W.data)

WW.analyze()

