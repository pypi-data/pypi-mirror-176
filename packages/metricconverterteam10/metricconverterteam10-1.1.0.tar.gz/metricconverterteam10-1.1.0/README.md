
![Python build & test](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-10/actions/workflows/build.yaml/badge.svg)

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9129447&assignment_repo_type=AssignmentRepo)

# Python Package Exercise

A little exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

# Teammates

* Jonason Wu (jw5911): [Github Profile](https://github.com/JonasonWu)
* Alejandro Olazabal (ajo351): [Github Profile](https://github.com/aleolazabal)
* Junyi Dong (jd4634): [Github Profile](https://github.com/junyid) 
* Fatema Nassar (fan6236) : [Github Profile](https://github.com/fnassar)

# Import the Project
<!-- how a developer who wants to import your project into their own code can do so - include documentation for all functions in your package and a link to an example Python program that uses each of them. -->
<!-- functions -->
## Package Name:
* metricconverterteam10

## Package content(functions):
* age_converter, number_converter, time_zone_converter, distance_converter

## How to Install:
> Activate a `pipenv` shell: <br>
```
$ pipenv shell
```
> Install our package: <br>
```
$ pipenv install metricconverterteam10
```

## Possible imports
* `You can test out these imports either on a python file or test the on the python shell with the following command:`
```
$ python
```
* You can now run: 
* `from metricconverterteam10 import age_converter`
    * `age_converter.calc_age(dob: str, unit: str)`
        * dob: Date Of Birth (e.g., Jan 10 2000 12:00AM)
        * unit: The unit to convert into. Choices: 'actual', 'years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds'.
    * `age_converter.help()`
* `from metricconverterteam10 import number_converter`
    * `number_converter.convert_number(toUnit: str, value: Any)`
        * toUnit: The unit to convert value into. Choices: 'binary', 'decimal', 'hexadecimal', 'octal'
        * value: The value to convert. It could be in binary, octal, decimal, or hexadecimal form.
* `from metricconverterteam10 import time_zone_converter`
    * `time_zone_converter.convert_timezone(code: str)`
        * code: the ISO Alpha 2 code of the country.
* `from metricconverterteam10 import distance_converter`
    * `distance_converter.allowed_distance_conversions()`
    * `distance_converter.convert_distance(num: float | int | str, unit1: str, unit2: str)`
        * num: A number that is convertible to a float value.
        * unit1: The unit to convert from
        * unit2: The unit to convert to


## Link to project:
* Link to the Test PyPi project: [link](https://test.pypi.org/project/metricconverterteam10/)
* Link to the actual PyPi project: [link](https://pypi.org/project/metricconverterteam10/)
* Link to the documentation of the functions: [Code Examples](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-10#code-examples)
* Link to an example python program: [\_\_main\_\_.py](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-10/blob/main/__main__.py)

# Contribute to this Project

* Open bash terminal
* Clone this repository
    ```
    $ git clone https://github.com/software-students-fall2022/python-package-exercise-project-3-team-10.git
    ```
* Get into the project directory
    ```
    $ cd python-package-exercise-project-3-team-10
    ```
* Create python virtual environment
    ```
    python -m venv .venv
    ```
* Activate python virtual environment:
    * On Mac:
        ```
        source .venv/bin/activate
        ```
    * On Windows:
        ```
        .venv/Scripts/activate.bat
        ```
* Install pipenv
    ```
    $ pip install pipenv
    ```
* Activate virtual enviroment
    ```
    $ pipenv shell
    ```
* Install all dependencies
    ```
    $ pipenv install -e .
    ```
* Build 
    ```
    $ python -m build
    ```
    If this doesnt work try
    ```
    $ python3 -m build
    ```
* Test
    ```
    $ pipenv run pytest
    ```

# Code Examples

## Age Converter

* The following line will give the options for the age conversions that are available:
    ```
    >> age_converter.help()
    calc_age(dob, unit):
        Input dob in the following format: MTH DAY YEAR TIME
        These are the available units to convert into: ['actual', 'years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']
        Example:
                >> calc_age('Jan 1 2000 1:33PM', 'years')
                22 years old
    ```

* The following line will give a converted description given the date of birth (at 11/8/2022):
    ```
    >> print(age_converter.calc_age('Jan 1 2000 1:33PM', 'actual'))
    22 years 10 months and 7 days old
    ```
* The following line will give the number of days someone with that birthday has lived (at 11/8/2022):
    ```
    >> print(age_converter.calc_age('Jan 1 2000 1:33PM', 'days'))
    8347 days old
    ```


## Distance Converter

* The following line will print and give all the conversions for distances that are available:
    ```
    >> li = distance_converter.allowed_distance_conversions()
    These are the allowed unit inputs for the convert_distance method: 
    inches     --> in
    feet       --> ft
    mile       --> mi
    milimeter  --> mm
    centimeter --> cm
    meter      --> m
    kilometer  --> km
    >> print(li)
    ['mm', 'm', 'mi', 'cm', 'in', 'km', 'ft']
    ```
* The following line will convert 10 feet into inches:
    ```
    >> print(distance_converter.convert_distance(10, 'ft', 'in'))
    120.0
    ```
* The following line will convert 100 centimeters into meters:
    ```
    >> print(distance_converter.convert_distance(100, 'cm', 'm'))
    1.0
    ```

## Number Converter

* The following line will convert a decimal value of 1000 into binary:
    ```
    >> print(number_converter.convert_number("binary", 1000))
    0b1111101000
    ```
* The following line will convert a decimal value of 1000 into octal:
    ```
    >> print(number_converter.convert_number("octal", 1000))
    0o1750
    ```
* The following line will convert a hexadecimal value of 0x1111 into decimal:
    ```
    >> print(number_converter.convert_number("decimal", 0x1111))
    4369
    ```

## Time Zone Converter

* The following line will print out all the possible times of the United States at the current time of 8:16PM:
    ```
    >> print(time_zone_converter.convert_timezone("US"))
    {'08:16PM': ['America/New_York', 'America/Detroit', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Indiana/Indianapolis', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Vevay'], '07:16PM': ['America/Chicago', 'America/Indiana/Tell_City', 'America/Indiana/Knox', 'America/Menominee', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/North_Dakota/Beulah'], '06:16PM': ['America/Denver', 'America/Boise', 'America/Phoenix'], '05:16PM': ['America/Los_Angeles'], '04:16PM': ['America/Anchorage', 'America/Juneau', 'America/Sitka', 'America/Metlakatla', 'America/Yakutat', 'America/Nome'], '03:16PM': ['America/Adak', 'Pacific/Honolulu']}
    ```
