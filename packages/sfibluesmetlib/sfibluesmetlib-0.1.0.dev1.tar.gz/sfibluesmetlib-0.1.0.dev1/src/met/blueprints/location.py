# 
# Generated with LocationBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class LocationBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="Location", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string","",default=None))
        self.add_attribute(Attribute("geospatial_lat_min","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("geospatial_lat_max","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("geospatial_lon_min","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("geospatial_lon_max","number","",optional=False,default=0.0))
        self.add_attribute(BlueprintAttribute("waves","met/Wave","",True,Dimension("*")))
        self.add_attribute(BlueprintAttribute("winds","met/Wind","",True,Dimension("*")))
        self.add_attribute(BlueprintAttribute("waveScatter","met/scatter/Scatter","",True))
        self.add_attribute(BlueprintAttribute("waveDirScatter","met/scatter/Wave","",True))
        self.add_attribute(Attribute("meanWaveDirection","number","",default=0.0))
        self.add_attribute(Attribute("meanHs","number","",default=0.0))
        self.add_attribute(Attribute("meanTp","number","",default=0.0))