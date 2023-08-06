from Engine import Framework
from Engine.Framework import Connection,Engine

class ValveSimple(Connection):
    def __init__(self, engine: Engine) -> None: ...
    def init(self,Area:str,type:int)->ValveSimple:...

    