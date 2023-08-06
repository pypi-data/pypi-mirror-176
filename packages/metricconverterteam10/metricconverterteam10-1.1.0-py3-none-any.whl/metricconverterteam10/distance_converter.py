
''' This variable stores a set of valid conversion values. '''
__units = {"in", "ft", "mi", "mm", "cm", "m", "km"}

''' This variable stores a dictionary of aliases for the __units. '''
__alias_units = {
    "inches": "in", 
    "feet": "ft", 
    "mile": "mi", 
    "milimeter": "mm", 
    "centimeter": "cm", 
    "meter": "m", 
    "kilometer": "km"
}

''' This variable stores the conversion coefficients. '''
__conversions = {
    "in": {"in": 1, "ft": 1/12, "mi": 1/63360, "mm": 25.4, "cm": 2.54, "m": 0.0254, "km": 2.54e-5}, 
    "ft": {"in": 12, "ft": 1, "mi": 1/5280, "mm": 304.8, "cm": 30.48, "m": 0.3048, "km": 3.048e-4},
    "mi": {"in": 63360, "ft": 5280, "mi": 1, "mm": 1609344, "cm": 160934.4, "m": 1609.344, "km": 1.609344},
    "mm": {"in": 1/25.4, "ft": 1/304.8, "mi": 1/1609344, "mm": 1, "cm": 1/10, "m": 1/1000, "km": 1e-6},
    "cm": {"in": 1/2.54, "ft": 1/30.48, "mi": 1/160934.4, "mm": 10, "cm": 1, "m": 1/100, "km": 1e-5},
    "m": {"in": 1/0.0254, "ft": 3.28084, "mi": 1/1609.344, "mm": 1000, "cm": 100, "m": 1, "km": 1e-3},
    "km": {"in": 39370.1, "ft": 3280.84, "mi": 1/1.609344, "mm": 1e6, "cm": 1e5, "m": 1000, "km": 1}
}

def allowed_distance_conversions():
    """ 
    Gives a list of allowed conversions for distance and returns a list of valid conversion values. 
    """

    print("These are the allowed unit inputs for the convert_distance method: ")
    li = []
    for k, v in __alias_units.items():
        li += [f'{k:<10} --> {v}']
    print("\n".join(li))
    return list(__units)

def convert_distance(num: float | int | str, unit1: str, unit2: str) -> float:
    ''' 
    Converts a distance of num from unit1 into unit2.
    '''
    if unit1 in __units:
        if unit2 in __units:
            return float(num) * __conversions[unit1][unit2]
        else:
            raise UnitNotFound(unit2)
    else:
        raise UnitNotFound(unit1)

class UnitNotFound(Exception):
    ''' 
    This exception is thrown when the unit to convert is not found.
    '''
    def __init__(self, unit):
        ''' Set the exception message. '''
        super().__init__("The unit " + str(unit) + " is not listed as a valid convertible. Call allowed_distance_conversions to get a list of allowed conversions.")
