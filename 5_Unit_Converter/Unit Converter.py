import questionary
from pint import UnitRegistry
import time

Separator = "----------------------"
ureg = UnitRegistry()

length_map = {
    "mm (millimeter)": "millimeter",
    "cm (centimeter)": "centimeter",
    "m (meter)": "meter",
    "km (kilometer)": "kilometer",
    "in (inch)": "inch",
    "ft (foot)": "foot",
    "yd (yard)": "yard",
    "mi (mile)": "mile"
}

mass_map = {
    "mg (milligram)": "milligram",
    "g (gram)": "gram",
    "kg (kilogram)": "kilogram",
    "lb (pound)": "pound",
    "oz (ounce)": "ounce"
}

time_map = {
    "ms (millisecond)": "millisecond",
    "s (second)": "second",
    "min (minute)": "minute",
    "h (hour)": "hour",
    "d (day)": "day",
    "wk (week)": "week",
    "mo (month)": "month",
    "y (year)": "year"
}

temperature_map = {
    "K (kelvin)": "kelvin",
    "C (celsius)": "degC",
    "F (fahrenheit)": "degF"
}

speed_map = {
    "m/s (meters per second)": "meter/second",
    "km/h (kilometers per hour)": "kilometer/hour",
    "mi/h (miles per hour)": "mile/hour",
    "ft/s (feet per second)": "foot/second"
}

orig_maps = {
    "Length": list(length_map.keys()),
    "Mass": list(mass_map.keys()),
    "Time": list(time_map.keys()),
    "Temperature": list(temperature_map.keys()),
    "Speed": list(speed_map.keys())
}

unit_maps = {
    "Length": length_map,
    "Mass": mass_map,
    "Time": time_map,
    "Temperature": temperature_map,
    "Speed": speed_map
}


def converter():
    print()
    print(f"{Separator} UNIT CONVERTER {Separator}")
    
    select = questionary.select("What do you want to do?", choices=["Convert units", "Turn off"]).ask()
    if select == "Convert units":
        category = questionary.select("Choose a category to convert:", choices=list(orig_maps.keys()) + ["Back to main menu"]).ask()
        if category == "Back to main menu":
            converter()

        
        local_units = orig_maps[category].copy()
        unit_map = unit_maps[category]

        from_unit = questionary.select("From unit:", choices=local_units + ["Back to the main menu"]).ask()
        if from_unit == "Back to the main menu":
            return converter()
        local_units.remove(from_unit)
        to_unit = questionary.select("To unit:", choices=local_units + ["Back to the main menu"]).ask()

        if to_unit == "Back to the main menu":
            return converter()

        while True:
            try:
                print()
                print("Converting from", from_unit, "to", to_unit)
                value = input("Enter the value to convert (or 'back' to return): ")
                if value.lower() == 'back':
                    return converter()
                else:
                    value = float(value)

                if category == "Temperature":
                    quantity = ureg.Quantity(value, unit_map[from_unit])
                    result = quantity.to(unit_map[to_unit])
                else:
                    result = (value * ureg(unit_map[from_unit])).to(unit_map[to_unit])

                print("Converting...")
                time.sleep(1)

    
                result_value = result.magnitude

                if value.is_integer():
                    value = int(value)
                if result_value.is_integer():
                    result_value = int(result_value)

                print(f"\n ✅ Done {value} {from_unit} is equal to {result_value} {to_unit}\n")


            except Exception as error:
                print(f"❌ Invalid input or error: {error}")

    elif select == "Turn off":
        turn_off()

def turn_off():
    print()
    print(f"{Separator} TURN OFF {Separator}")
    turn_off_or = questionary.select("Are you sure you want to exit the Unit Converter application?:", choices=["Yes, I would like to exit", "No, please keep it open"]).ask()
    if turn_off_or == "Yes, I would like to exit":
        print("Thank you for using the Unit Converter application! 😊")
        time.sleep(3)
        print("...")
        quit()
    elif turn_off_or == "No, please keep it open":
        converter()


print()
print("Hello! Welcome to the Unit Converter application!")

converter()
