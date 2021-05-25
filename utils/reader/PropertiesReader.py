'''
Created on May 19, 2020
@author: gioargyr
'''

import os
from configparser import ConfigParser


class PropertiesReader():

    """
        Initialization of PropertiesReader class
    """
    def __init__(self, properties_dir):

        self.read_properties(properties_dir)


    """
        read_properties EXPECTS to find a file called "AdaM.properties" in the properties/resources directory
        It reads the properties and stores them as class variables.
    """
    def read_properties(self, prop_dir):

        property_file = os.path.join(prop_dir, "WM.properties")
        cfg = ConfigParser()
        cfg.read(property_file)
        self.dataset_name   = cfg.get("config", "dataset_file_name")
        self.window         = cfg.get("config", "window")
        self.overlap        = cfg.get("config", "overlap")
        # self.Tmax       = cfg.get("config", "Tmax")
        # self.g          = cfg.get("config", "g")
        # self.lamda      = cfg.get("config", "lamda")
        # self.Rmin       = cfg.get("config", "Rmin")
        # self.Rmax       = cfg.get("config", "Rmax")
        # self.parameter  = cfg.get("config", "parameter")
        # self.low_limit  = cfg.get("config", "low_limit")
        # self.upper_limit= cfg.get("config", "upper_limit")
        # self.step       = cfg.get("config", "step")
#        self.v_sampl_per= cfg.get("config", "virtual_sampl_per")

