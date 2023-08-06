# Application entry
# Generated with MetPortalBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class MetPortalBlueprint(NamedEntityBlueprint):
    """Application entry"""

    def __init__(self, name="MetPortal", package_path="met", description="Application entry"):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string","",default=None))
        self.add_attribute(BlueprintAttribute("jobs","met/jobs/Job","",True,Dimension("*")))