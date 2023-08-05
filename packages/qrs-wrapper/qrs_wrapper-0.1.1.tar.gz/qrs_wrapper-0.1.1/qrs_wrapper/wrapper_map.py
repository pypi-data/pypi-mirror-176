#!/usr/bin/env python
# coding: utf-8

# QRS DETECTORS LIBRARIES
from biosppy.signals import ecg
from ecgdetectors import Detectors

# CATALOGUE OF AVAILABLE LIBRARIES AND METHODS WITHIN EACH OF THEM
CATALOGUE_DETECTORS = {
    "biosppy": ["default", "christov", "engzee", "gamboa", "hamilton", "ssf"],
    "neurokit": ["default", "christov", "elgendi", "engzee", "gamboa", "hamilton", "kalidas", "martinez", "nabian", "pantompkins", "promac", "rodrigues", "zong"],
    "py-ecg-detectors": ["christov", "engzee", "hamilton", "pantompkins", "swt", "twoaverage", "wqrs"]
}

# MAP BETWWEN THE METHOD'S NAME AND THE METHODS (OR PARAMETERS) TO CALL FOR EACH LIBRARY
WRAPPER_MAP = {
    
    "biosppy" : {
        "christov": ecg.christov_segmenter,
        "engzee": ecg.engzee_segmenter, 
        "gamboa": ecg.gamboa_segmenter,
        "hamilton": ecg.hamilton_segmenter,
        "ssf": ecg.ssf_segmenter
    },
    
    "neurokit" : {
        "default" : {
            "cleaner" : "neurokit",
            "method" : "neurokit"
        },
        "christov" : {
            "cleaner" : "neurokit",
            "method" : "christov2004"
        },
        "elgendi" : {
            "cleaner" : "elgendi2010",
            "method" : "elgendi2010"
        },
        "engzee" : {
            "cleaner" : "engzeemod2012",
            "method" : "engzeemod2012"
        },
        "gamboa" : {
            "cleaner" : "neurokit",
            "method" : "gamboa2008"
        },
        "hamilton" : {
            "cleaner" : "hamilton2002",
            "method" : "hamilton2002"
        },
        "kalidas" : {
            "cleaner" : "neurokit",
            "method" : "kalidas2017"
        },
        "martinez" : {
            "cleaner" : "neurokit",
            "method" : "martinez2004"
        },
        "nabian" : {
            "cleaner" : "neurokit",
            "method" : "nabian2018"
        }, 
        "pantompkins" : {
            "cleaner" : "pantompkins1985",
            "method" : "pantompkins1985"
        },
        "promac" : {
            "cleaner" : "neurokit",
            "method" : "promac"
        },
        "rodrigues" : {
            "cleaner" : "neurokit",
            "method" : "rodrigues2021"
        },
        "zong" : {
            "cleaner" : "neurokit",
            "method" : "zong2003"
        }
        
    },
    
    "py-ecg-detectors" :{
        "christov" : lambda detectors: detectors.christov_detector,
        "engzee" : lambda detectors: detectors.engzee_detector,
        "hamilton" : lambda detectors: detectors.hamilton_detector,
        "pantompkins" : lambda detectors: detectors.pan_tompkins_detector,
        "swt" : lambda detectors: detectors.swt_detector,
        "twoaverage" : lambda detectors: detectors.two_average_detector,
        "wqrs" : lambda detectors: detectors.wqrs_detector,  
    }  
    
}

