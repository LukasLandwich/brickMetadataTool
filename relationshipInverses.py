"""
Defining Brick relationships
"""
inverses = {

    "isLocationOf": "hasLocation",
    "hasLocation":"isLocationOf",
    "feeds": "isFedBy",
    "isFedBy": "feeds",
    "hasPoint": "isPointOf",
    "isPointOf": "hasPoint",
    "hasPart": "isPartOf",
    "isPartOf": "hasPart",
    "hasTag": "isTagOf",
    "hasAssociatedTag": "isAssociatedWith",
    "isAssociatedWith": "hasAssociatedTag",
    "meters": "isMeteredBy",
    "isMeteredBy":"meters",  
    "hasSubMeter": "isSubMeterOf",
    "isSubMeterOf":"hasSubMeter",
}

def gotInverse(label:str) -> bool:
    print("Label: " + label)
    gotInverse = inverses.keys().__contains__(label)
    print(gotInverse)
    return gotInverse

def getInverse(label:str) -> str:
    if gotInverse(label):
        return inverses.get(label)
    else:
        return None