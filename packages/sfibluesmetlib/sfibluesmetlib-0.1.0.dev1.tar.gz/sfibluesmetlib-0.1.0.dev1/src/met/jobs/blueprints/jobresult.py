# 
# Generated with JobResultBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class JobResultBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="JobResult", package_path="met/jobs", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string","",default=None))
        self.add_attribute(Attribute("progress","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("result","string","",optional=False,default=None))
        self.add_attribute(Attribute("wind_speed","number","",Dimension("*"),default=0.0))
        self.add_attribute(Attribute("wind_direction","number","",Dimension("*"),default=0.0))