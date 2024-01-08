

"""
Each is a qudt:QuantityKind
"""
quantity_definitions = {
            "Ammonia_Concentration": {
                "applicableUnit": ["PPM", "PPB"],
            },
            "CO_Concentration": {
                "applicableUnit": ["PPM", "PPB"],
                },
            "CO2_Concentration": {
                "applicableUnit": ["PPM", "PPB"],
                },
            "Formaldehyde_Concentration": {
                "applicableUnit": ["PPM", "PPB"],
            },
            "Ozone_Concentration": {
                "applicableUnit": ["PPM", "PPB"],
            },
            "Methane_Concentration": {
                "applicableUnit": ["PPM", "PPB"],
            },
            "NO2_Concentration": {
                "applicableUnit": ["PPM", "PPB"],
            },
            "PM10_Concentration": {
                "applicableUnit": ["PPM", "PPB", "MicroGM-PER-M3"],
            },
            "PM2.5_Concentration": {
                "applicableUnit": ["PPM", "PPB", "MicroGM-PER-M3"],
            },
            "PM1_Concentration": {
                "applicableUnit": ["PPM", "PPB", "MicroGM-PER-M3"],
            },
            "Radon_Concentration": {
                "applicableUnit": ["BQ-PER-M3"],
            },
            "TVOC_Concentration": {
                "applicableUnit": ["PPM", "PPB", "MicroGM-PER-M3"],
            },
            "GrainsOfMoisture": {
                "applicableUnit": "GRAIN",
            },
            "Phasor_Angle": {
                "applicableUnit": [
                    "ARCMIN",
                    "ARCSEC",
                    "DEG",
                    "GON",
                    "GRAD",
                    "MIL",
                    "RAD",
                    "MicroRAD",
                    "MilliRAD",
                    "MilliARCSEC",
                    "REV",
                ],
            },
            "Phasor_Magnitude": {
                "applicableUnit": [
                    "ARCMIN",
                    "ARCSEC",
                    "DEG",
                    "GON",
                    "GRAD",
                    "MIL",
                    "RAD",
                    "MicroRAD",
                    "MilliRAD",
                    "MilliARCSEC",
                    "REV",
                ], 
            },
            "Peak_Power": {
                "applicableUnit": ["KiloW", "MegaW", "MilliW", "W"],
            },
            "Thermal_Power": {
                "applicableUnit": [
                    "MilliW",
                    "W",
                    "KiloW",
                    "MegaW",
                    "BTU_IT",
                ],
            },
            "Current_Angle": {
                "applicableUnit": [
                    "ARCMIN",
                    "ARCSEC",
                    "DEG",
                    "GON",
                    "GRAD",
                    "MIL",
                    "RAD",
                    "MicroRAD",
                    "MilliRAD",
                    "MilliARCSEC",
                    "REV",
                ],
            },
            "Current_Imbalance": {
                "applicableUnit": ["PERCENT"],
            },
            "Current_Total_Harmonic_Distortion": {
                "applicableUnit": ["PERCENT", "DeciB_M"],
            },
            "Alternating_Current_Frequency": {
                "applicableUnit": ["GigaHZ", "MegaHZ", "KiloHZ", "HZ"],
            },
            "Voltage_Angle": {
                "applicableUnit": [
                    "ARCMIN",
                    "ARCSEC",
                    "DEG",
                    "GON",
                    "GRAD",
                    "MIL",
                    "RAD",
                    "MicroRAD",
                    "MilliRAD",
                    "MilliARCSEC",
                    "REV",
                ],
            },
            "Voltage_Imbalance": {
                "applicableUnit": ["PERCENT"],
            },
            "Wind_Direction": {
                "applicableUnit": [
                    "ARCMIN",
                    "ARCSEC",
                    "DEG",
                    "GON",
                    "GRAD",
                    "MIL",
                    "RAD",
                    "MicroRAD",
                    "MilliRAD",
                    "MilliARCSEC",
                    "REV",
                ],
            },
            "Electric_Energy": {
                "applicableUnit": [
                    "J",
                    "W-HR",
                    "KiloW-HR",
                    "MegaW-HR",
                    "V-A_Reactive-HR",
                    "KiloV-A_Reactive-HR",
                    "MegaV-A_Reactive-HR",
                    "KiloV-A-HR",
                    "V-A-HR",
                    "MegaV-A-HR",
                ],
            },
            "Active_Energy": {
                "applicableUnit": [
                    "W-HR",
                    "KiloW-HR",
                    "MegaW-HR",
                ],
            },
            "Reactive_Energy": {
                "applicableUnit": [
                    "V-A_Reactive-HR",
                    "KiloV-A_Reactive-HR",
                    "MegaV-A_Reactive-HR",
                ],
            },
            "Apparent_Energy": {
                "applicableUnit": [
                    "KiloV-A-HR",
                    "V-A-HR",
                    "MegaV-A-HR",
                ],
            },
            "Flow_Loss": {
                "applicableUnit": ["M3-PER-SEC"],
            },
        "Irradiance": {
            "applicableUnit": [
                "W-PER-M2",
                "W-PER-IN2",
                "W-PER-FT2",
                "W-PER-CentiM2",
            ],
        },
        "Solar_Irradiance": {
            "applicableUnit": [
                "W-PER-M2",
                "W-PER-IN2",
                "W-PER-FT2",
                "W-PER-CentiM2",
            ],
            
        },
        "Level": {
            "applicableUnit": [
                "CentiM",
                "DeciM",
                "MilliM",
                "MicroM",
                "KiloM",
                "M",
                "IN",
                "FT",
                "YD",
            ],
        },
        "Precipitation": {
            "applicableUnit": [
                "CentiM",
                "DeciM",
                "MilliM",
                "MicroM",
                "KiloM",
                "M",
                "IN",
                "FT",
                "YD",
            ],
        },
        "Occupancy_Percentage": {
            "applicableUnit": ["PERCENT"],
        },
        "Position": {
            "applicableUnit": ["PERCENT"],
        },
        
            

    
        "Solar_Radiance": {
            "applicableUnit": ["W-PER-M2-SR"],
            
        },
 
  
            "Linear_Speed": {
                "applicableUnit": [
                    "M-PER-HR",
                    "KiloM-PER-HR",
                    "FT-PER-HR",
                    "MI-PER-HR",
                    "M-PER-SEC",
                    "KiloM-PER-SEC",
                    "FT-PER-SEC",
                    "MI-PER-SEC",
                ],
            },
            "Rotational_Speed": {
                "applicableUnit": [
                    "RAD-PER-HR",
                    "RAD-PER-SEC",
                    "RAD-PER-MIN",
                    "DEG-PER-HR",
                    "DEG-PER-MIN",
                    "DEG-PER-SEC",
                ],
            },       
            "Operative_Temperature": {
                "applicableUnit": ["DEG_F", "DEG_C", "K"],
            },
            "Radiant_Temperature": {
                "applicableUnit": ["DEG_F", "DEG_C", "K"],
            },
            "Dry_Bulb_Temperature": {
                "applicableUnit": ["DEG_F", "DEG_C", "K"],
            },
            "Wet_Bulb_Temperature": {
                "applicableUnit": ["DEG_F", "DEG_C", "K"],
            },
    "Time": {
        "applicableUnit": ["SEC", "MIN", "HR", "DAY"],
    },
    "Volume": {
        "applicableUnit": ["M3", "FT3", "IN3", "YD3"],
    },

}



def getUnitFor(quantityName:str) -> [str]:
    if quantity_definitions.keys().__contains__(quantityName):
        return quantity_definitions[quantityName]["applicableUnit"]
    else:
        return []

def allAllUnits() -> [str]:
    units = []
    for key in quantity_definitions.keys():
        for x in quantity_definitions.get(key)["applicableUnit"]:
            units.append(x)
        
    return set(units)