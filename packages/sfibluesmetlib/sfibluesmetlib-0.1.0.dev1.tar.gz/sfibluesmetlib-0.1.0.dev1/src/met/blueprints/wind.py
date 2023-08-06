# 
# Generated with WindBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from .observations import ObservationsBlueprint

class WindBlueprint(ObservationsBlueprint):
    """"""

    def __init__(self, name="Wind", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string","",default=None))
        self.add_attribute(Attribute("Conventions","string","",optional=False,default=None))
        self.add_attribute(Attribute("NCO","string","",default=None))
        self.add_attribute(Attribute("buoy_manufacturer","string","",optional=False,default=None))
        self.add_attribute(Attribute("buoy_serialno","string","",optional=False,default=None))
        self.add_attribute(Attribute("buoy_type","string","",optional=False,default=None))
        self.add_attribute(Attribute("data_collecting_contractor","string","",optional=False,default=None))
        self.add_attribute(Attribute("data_owner","string","",optional=False,default=None))
        self.add_attribute(Attribute("date_created","string","",optional=False,default=None))
        self.add_attribute(Attribute("featureType","string","",default=None))
        self.add_attribute(Attribute("geospatial_lat_max","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("geospatial_lat_min","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("geospatial_lon_max","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("geospatial_lon_min","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("geospatial_vertical_positive","string","",optional=False,default=None))
        self.add_attribute(Attribute("history","string","",optional=False,default=None))
        self.add_attribute(Attribute("keywords","string","",optional=False,default=None))
        self.add_attribute(Attribute("keywords_vocabulary","string","",optional=False,default=None))
        self.add_attribute(BlueprintAttribute("latitude","met/MetVariable","",True))
        self.add_attribute(Attribute("licence","string","",optional=False,default=None))
        self.add_attribute(BlueprintAttribute("longitude","met/MetVariable","",True))
        self.add_attribute(Attribute("measurement_update_period","string","",optional=False,default=None))
        self.add_attribute(Attribute("modified","string","",optional=False,default=None))
        self.add_attribute(Attribute("netcdf_version","string","",optional=False,default=None))
        self.add_attribute(Attribute("position_ref","string","",optional=False,default=None))
        self.add_attribute(Attribute("processing_level","string","",optional=False,default=None))
        self.add_attribute(Attribute("publisher_email","string","",optional=False,default=None))
        self.add_attribute(Attribute("publisher_name","string","",optional=False,default=None))
        self.add_attribute(Attribute("publisher_url","string","",optional=False,default=None))
        self.add_attribute(Attribute("sensor_level","string","",optional=False,default=None))
        self.add_attribute(Attribute("sensor_manufacturer","string","",optional=False,default=None))
        self.add_attribute(Attribute("sensor_serialno","string","",optional=False,default=None))
        self.add_attribute(Attribute("sensor_type","string","",optional=False,default=None))
        self.add_attribute(Attribute("station_name","string","",optional=False,default=None))
        self.add_attribute(Attribute("status","string","",default=None))
        self.add_attribute(Attribute("summary","string","",optional=False,default=None))
        self.add_attribute(BlueprintAttribute("time","met/MetVariable","",True))
        self.add_attribute(Attribute("time_coverage_end","string","",optional=False,default=None))
        self.add_attribute(Attribute("time_coverage_start","string","",optional=False,default=None))
        self.add_attribute(Attribute("title","string","",optional=False,default=None))
        self.add_attribute(Attribute("url","string","",optional=False,default=None))
        self.add_attribute(Attribute("water_depth","string","",optional=False,default=None))
        self.add_attribute(BlueprintAttribute("WindDirection","met/MetVariable","",True))
        self.add_attribute(BlueprintAttribute("WindGust","met/MetVariable","",True))
        self.add_attribute(BlueprintAttribute("WindSpeed","met/MetVariable","",True))