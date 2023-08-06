import age_converter
import distance_converter
import number_converter
import time_zone_converter

def view1():
  print("Calling age_converter.help()...")
  age_converter.help()

def view2():
  print("Using age_converter.calc_age(str, str)...")
  print("DOB of Jan 1 2000 1:33PM: ", age_converter.calc_age('Jan 1 2000 1:33PM', 'actual'))
  print("DOB of Jan 11 2000 1:33PM: ", age_converter.calc_age('Jan 11 2000 1:33PM', 'years'))
  print("DOB of Feb 1 2005 1:33PM: ", age_converter.calc_age('Feb 1 2005 1:33PM', 'days'))

def view3():
  print("Calling distance_converter.allowed_distance_conversions()...")
  li = distance_converter.allowed_distance_conversions()
  print("This Method Returns:", li)

def view4():
  print('Using distance_converter.convert_distance(int, str, str)...')
  print("10 feet =", distance_converter.convert_distance(10, 'ft', 'in'), "inches")
  print("100 centimeters =", distance_converter.convert_distance(100, 'cm', 'm'), "meters")

def view5():
  print("Using number_converter.convert_number(str, Any)...")
  print("Binary of 0b1111 =", number_converter.convert_number("decimal", 0b1111), "in decimal")
  print("Octal of 0o1111 =", number_converter.convert_number("decimal", 0o1111), "in decimal")
  print("Hexadecimal of 0x1111 =", number_converter.convert_number("decimal", 0x1111), "in decimal")
  print("Decimal of 1000 =", number_converter.convert_number("binary", 1000), "in binary")
  print("Decimal of 1000 =", number_converter.convert_number("octal", 1000), "in octal")
  print("Decimal of 1000 =", number_converter.convert_number("hexadecimal", 1000), "in hexadecimal")

def view6():
  print("Calling time_zone_converter.convert_timezone(str)...")
  print("Current times in the USA:", time_zone_converter.convert_timezone("US"))

funs = [view1, view2, view3, view4, view5, view6]
def operate(num):
  if (num < 1 or num > 6):
    return
  funs[num-1]()

def main():
  num = 0
  while num != 7:
    print()
    print("""Which method do you want to get usage sample of?
  (1) age_converter_help()
  (2) age_converter.calc_age(str, str)
  (3) distance_converter.allowed_distance_conversions()
  (4) distance_converter.convert_distance(int, str, str)
  (5) number_converter.convert_number(str, Any)
  (6) time_zone_converter.convert_timezone(str)
  (7) exit/quit this program
  """)
    try:
      num = int(input("Pick number: "))
      print()
    except:
      print("Invalid input")
      continue
    operate(num)
    print()
    input("Enter to continue...")
  print("Good bye!")

if __name__ == '__main__':
    main()