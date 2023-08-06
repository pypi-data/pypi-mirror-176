# 
# Generated with MetVariableBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class MetVariableBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="MetVariable", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string","",default=None))
        self.add_attribute(Attribute("max","number","",default=0.0))
        self.add_attribute(Attribute("mean","number","",default=0.0))
        self.add_attribute(Attribute("min","number","",default=0.0))
        self.add_attribute(Attribute("size","integer","",optional=False,default=0))
        self.add_attribute(Attribute("standard_name","string","",default=None))
        self.add_attribute(Attribute("std","number","",default=0.0))
        self.add_attribute(Attribute("units","string","",optional=False,default=None))