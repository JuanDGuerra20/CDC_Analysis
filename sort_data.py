"""
Author: Juan David Guerra. First year Computer Science and Neuroscience student at McGill University B.Sc.
Start Date: December 28, 2020
Outline: This module will hold the classes and methods needed to organize the data so we can easily access it

UPDATES: Have added a class to manage data from the USGS in the states. This handles the pesticide data they give
"""


class DiseaseTypeArea:
    """
    This class will hold all the data of the given area for a given disease type
    The name of the class should include the disease type and the area that the data is being taken in
    This class should be used for data taken by the CDC by area
    """
    highest_incidence_year = 0
    highest_mortality_year = 0

    def __init__(self, area_name, disease_type, age_adjusted_rate, count, count_type, population, race,
                 sex, data_year, crude_rate):
        """
        Constructor making the class. -1 means that there was no data for that given column
        :param area_name: String
        :param disease_type: String
        :param data_year: int
        :param age_adjusted_rate: float
        :param count: int
        :param count_type: string
        :param population: int
        :param race: string
        :param sex: string
        :param crude_rate: float
        """

        # creating the attributes that are simple
        self.area = area_name
        self.disease = {}

        # creating the dictionaries that will hold the incidence and mortality data
        incidence_data = {}
        mortality_data = {}

        # making sure that the parameters are the proper type
        try:
            age_adjusted_rate = float(age_adjusted_rate)

        except:
            raise TypeError("Incorrect data type: age adjusted rate must be a float")

        try:
            count = int(count)
        except:
            raise TypeError("Incorrect data type: count must be an int")

        try:
            population = int(population)
        except:
            raise TypeError("Incorrect data type: population must be an int")

        try:
            data_year = int(data_year)
        except:
            raise TypeError("Incorrect data type: data_year must be an int")

        try:
            crude_rate = float(crude_rate)
        except:
            raise TypeError("Incorrect data type: crude rate must be a float")

        # we sort the types of data by the parameter count_type which will either be incidence or mortality
        if count_type == "Incidence":
            # adding all the desired information to the incidence data dictionary at the specific year
            incidence_data[data_year] = {'count': count, 'population': population,
                                         'age adjusted rate': age_adjusted_rate, 'crude rate': crude_rate,
                                         'race': race, 'sex': sex}
            self.disease[disease_type] = {'Incidence': incidence_data, 'Mortality': {}}

            # Checking if the count is higher than the highest recorded incidence count
            if count > DiseaseTypeArea.highest_incidence_year:
                DiseaseTypeArea.highest_incidence_year = count

        # doing the same as the above if statement but in the mortality_data dictionary
        elif count_type == "Mortality":
            mortality_data[data_year] = {'count': count, 'population': population,
                                         'age adjusted rate': age_adjusted_rate, 'crude rate': crude_rate,
                                         'race': race, 'sex': sex}
            self.disease[disease_type] = {'Incidence': {}, 'Mortality': mortality_data}

            # Checking if the count is higher than the highest recorded mortality count
            if count > DiseaseTypeArea.highest_mortality_year:
                DiseaseTypeArea.highest_mortality_year = count

        # if the count_type is not Incidence or Mortality, we want to raise a value error since those are the only types
        # of count_types we are taking into account for this type of disease
        else:
            raise ValueError("Unsupported count_type: must be either Incidence or Mortality")

    def __str__(self):
        """
        overloading the str function to output what I want it to.
        :return:
        """

        # This list will have all the diseases currently recorded in the class
        diseases = []

        # adding all the diseases in the class to the list
        for disease_type in self.disease:
            diseases.append(disease_type)

        diseases = ', '.join(diseases)

        return 'Area: ' + self.area + '\nDiseases: ' + diseases

    def add_yearly_data(self, data):
        """
        This static method will allow us to add a set of data for a specific year
        It takes in a string in the format of the CDC files in Cancer_Data_By_Area and takes the information and adds it
        to the appropriate instance attributes
        :param data: String
        :return: None
        Example:
        >>> area = DiseaseTypeArea('Alabama', 'All Cancer Sites Combined', 367.2, 9299, 'Incidence', 2293259,\
        "All Races", 'Female', 1999, 405.5)
        >>> area.add_yearly_data('Alabama|359.7|374.7|367.2|9299|Incidence|2293259|All Races|Female|All Cancer Sites Combined|2000|397.3|413.8|405.5')
        >>> area.add_yearly_data('Alabama|359.7|374.7|367.2|9299|Incidence|2293259|All Races|Female|Melanoma|2000|397.3|413.8|405.5')
        >>> area.disease['Incidence']
        {1999: {'count': 9299, 'population': 2293259, 'age adjusted rate': 367.2, 'crude rate': 405.5,
         'race': 'All Races', 'sex': 'Female'}, 2000: {'count': 9299, 'population': 2293259, 'age adjusted rate': 367.2,
          'crude rate': 405.5, 'race': 'All Races', 'sex': 'Female'}}
        """

        # ~ is in the CDC data if there was insufficient data to report
        # Replacing it with a -1 so we can construct the area
        if '~' in data:
            data = data.replace('~', '-1')

        # + appears in the CDC data if the sex counterpart is suppressed due to low numbers
        # replacing it with a -1 so we can keep going with the code and not hit errors
        if '+' in data:
            data = data.replace('+', '-1')

        # - appears in the CDC data if the state requested that the certain ethnicity or race not be reported
        if '|-|' in data:
            data = data.replace('|-', '|-1')

        # splitting the input data at the delimiter (|)
        data = data.split('|')

        # assigning the desired data types to the proper variables and making sure they are the correct type
        age_adjusted_rate = data[3]
        try:
            age_adjusted_rate = float(age_adjusted_rate)

        except:
            raise TypeError("Incorrect data type: age adjusted rate must be a float: " + age_adjusted_rate)

        population = data[6]
        try:
            population = int(population)
        except:
            raise TypeError("Incorrect data type: population must be an int")

        data_year = data[10]
        try:
            data_year = int(data_year)

        except:
            raise TypeError("Incorrect data type: data_year must be an int")

        crude_rate = data[13]
        try:
            crude_rate = float(crude_rate)

        except:
            raise TypeError("Incorrect data type: crude rate must be a float: " + str(data))

        count = data[4]
        if count == '.':
            count = (crude_rate * population) / 100000
        try:
            count = int(count)
        except:
            raise TypeError("Incorrect data type: count must be an int: " + count)

        # all the following variables should be strings
        count_type = data[5]
        race = data[7]
        sex = data[8]
        disease_type = data[9]

        # Have to check if the disease is already in the dictionary
        if disease_type in self.disease:
            # adding a year of data to the incidence dictionary or replacing the data year with the new input
            if count_type == "Incidence":
                self.disease[disease_type]['Incidence'][data_year] = {'count': count, 'population': population,
                                                                      'age adjusted rate': age_adjusted_rate,
                                                                      'crude rate':
                                                                          crude_rate, 'race': race, 'sex': sex}

                # Checking if the count is higher than the highest recorded incidence count
                if count > DiseaseTypeArea.highest_incidence_year:
                    DiseaseTypeArea.highest_incidence_year = count

            # adding a year of data to the mortality dictionary or replacing the data year with the new input
            elif count_type == "Mortality":
                self.disease[disease_type]['Mortality'][data_year] = {'count': count, 'population': population,
                                                                      'age adjusted rate': age_adjusted_rate,
                                                                      'crude rate': crude_rate,
                                                                      'race': race, 'sex': sex}

                # Checking if the count is higher than the highest recorded mortality count
                if count > DiseaseTypeArea.highest_mortality_year:
                    DiseaseTypeArea.highest_mortality_year = count

            # if the count_type is not Incidence or Mortality, we want to raise a value error since those are the
            # only types of count_types we are taking into account for this type of disease
            else:
                raise ValueError("Unsupported count_type: must be either Incidence or Mortality")

        # If the disease type has not been added to the dictionary,
        # we have to format the new dictionary and then add the data
        else:
            self.disease[disease_type] = {'Incidence': {}, 'Mortality': {}}

            if count_type == 'Incidence':
                self.disease[disease_type]['Incidence'][data_year] = {'count': count, 'population': population,
                                                                      'age adjusted rate': age_adjusted_rate,
                                                                      'crude rate':
                                                                          crude_rate, 'race': race, 'sex': sex}
            elif count_type == 'Mortality':
                self.disease[disease_type]['Mortality'][data_year] = {'count': count, 'population': population,
                                                                      'age adjusted rate': age_adjusted_rate,
                                                                      'crude rate': crude_rate,
                                                                      'race': race, 'sex': sex}

            # if the count_type is not Incidence or Mortality, we want to raise a value error since those are the
            # only types of count_types we are taking into account for this type of disease
            else:
                raise ValueError("Unsupported count_type: must be either Incidence or Mortality")

    def get_data_by_disease_year(self, disease, cr_type, year, data):
        """
        This instance method will get the count of a input count_type for a given disease and year
        Will return a KeyError if there is no count for that year
        :param disease: This string represents the disease that the user is searching for the crude rate
        :param cr_type: This string represents the crude rate type that the user wants. This represents either mortality
                        or incidence data as inputs
        :param year: int representing the year of the desired crude rate
        :param data: This is the data type that the user wants to collect (count, population, race, etc)
        :return: int - The crude rate of the disease type
        """

        if disease not in self.disease:
            raise KeyError("The disease has not been added to the list of diseases for this area")

        # getting the count for the given parameters
        count = self.disease[disease][cr_type][year][data]

        return count

    def get_data_between_years_by_disease_type(self, disease, data_type, count_type, lower_end, upper_end):
        """
        This function will get the total count numbers between the lower_end and upper_end years
        :param disease: This is the disease type that the user will be searching for
        :param data_type: The data that the user wants to obtain. Could be 'count' or 'population', etc.
        :param count_type: The count type (whether it be incidence or mortality counts)
        :param lower_end: The year that the person wants to start getting the data from
        :param upper_end: The last year that data is to be obtained
        :return: int that represents the total number of incidences between the given years
        """

        if disease not in self.disease:
            raise KeyError("The disease has not been added to the list of diseases for this area")

        data_sum = 0

        # looping through all the years for the given disease and checking if it is within the range given
        for year in self.disease[disease][count_type]:

            if lower_end <= year <= upper_end:
                # adding the count for the year iteration that meets the requirements to the sum of counts
                data_sum += self.disease[disease][count_type][year][data_type]

        return data_sum

    @classmethod
    def get_disease_from_data(cls, data):
        """
        This class method creates a new class from the data given in the CDC file
        :param data: this is the single line string taken from the data
        :return: returns a class method
        """

        # ~ is in the CDC data if there was no data to report. Replacing it with a -1 so we can construct the area
        if '~' in data:
            data.replace('~', '-1')

        # + appears in the CDC data if the sex counterpart is suppressed due to low numbers
        # replacing it with a -1 so we can keep going with the code and not hit errors
        if '+' in data:
            data = data.replace('+', '-1')

        # - appears in the CDC data if the state requested that the certain ethnicity or race not be reported
        if '|-' in data:
            data = data.replace('|-', '|-1')

        # splitting the input data at the delimiter (|)
        data = data.split('|')

        # assigning the desired data types to the proper variables and making sure they are the correct type
        age_adjusted_rate = data[3]
        try:
            age_adjusted_rate = float(age_adjusted_rate)

        except:
            raise TypeError("Incorrect data type: age adjusted rate must be a float")

        population = data[6]
        try:
            population = int(population)
        except:
            raise TypeError("Incorrect data type: population must be an int")

        data_year = data[10]
        try:
            data_year = int(data_year)

        except:
            raise TypeError("Incorrect data type: data_year must be an int")

        crude_rate = data[13]
        try:
            crude_rate = float(crude_rate)

        except:
            raise TypeError("Incorrect data type: crude rate must be a float: " + data)

        count = data[4]
        if count == '.':
            count = (crude_rate * population) / 100000
        try:
            count = int(count)
        except:
            raise TypeError("Incorrect data type: count must be an int")

        # all the following variables should be strings
        area_name = data[0]
        count_type = data[5]
        race = data[7]
        sex = data[8]
        disease_type = data[9]

        return cls(area_name, disease_type, age_adjusted_rate, count, count_type, population,
                   race, sex, data_year, crude_rate)


class PesticideData:
    """
    This class is going to organize all the pesticide data for any pesticide that we want to analyze
    """
    stateMapping = ('', "ALABAMA", "ALASKA", '', "ARIZONA", "ARKANSAS", "CALIFORNIA", '', '', "COLORADO", "CONNECTICUT", \
                    "DELAWARE", '', "FLORIDA", "GEORGIA", '', "HAWAII", 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS',\
                    'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', \
                    'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', \
                    'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', \
                    'PENNSYLVANIA', '', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH',\
                    'VERMONT', 'VIRGINIA', '', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING', '','','',\
                    'AMERICAN SAMOA', '','','','','','GUAM','','','NORTHERN  MARIANA ISLANDS','','',' PUERTO RICO','',\
                    '','','','VIRGIN ISLANDS')
    highest_pesticide_year = 0
    lowest_pesticide_year = 999999

    def __init__(self, statefipscode, stateName, year, units, corn, soybeans, wheat, cotton, vegetablesandfruit, rice,
                 orchardsandgrapes, alfalfa, pastureandhay, other):
        """
        constructing the class with all the required info. input  a -1 if there was no data for that crop type that year
        :param statefipscode: the state fips code that identifies each state int
        :param stateName: the name of the state, pretty simple String
        :param year: the year that the data was taken int
        :param units: the units that the data was collected with String
        :param corn: float
        :param soybeans: float
        :param wheat: float
        :param cotton: float
        :param vegetablesandfruit: float
        :param rice: float
        :param orchardsandgrapes: float
        :param alfalfa: float
        :param pastureandhay: float
        :param other:float. All other types of food that pesticides are used on
        """

        try:
            fips = int(statefipscode)
        except:
            raise TypeError("state FIPS code is not valid, must be an integer")

        self.compound = {}

        try:
            year = int(year)
        except:
            raise TypeError("Year must be an int")

        try:
            corn = float(corn)
        except:
            raise TypeError("Corn data must be a float")

        try:
            soybeans = float(soybeans)
        except:
            raise TypeError("Soybean data must be a float")

        try:
            wheat = float(wheat)
        except:
            raise TypeError("Wheat data must be a float")

        try:
            cotton = float(cotton)
        except:
            raise TypeError("Cotton data must be a float")

        try:
            vegetablesandfruit = float(vegetablesandfruit)
        except:
            raise TypeError("Vegetable and Fruit must be a float")

        try:
            rice = float(rice)
        except:
            raise TypeError("Rice data must be a float")

        try:
            orchardsandgrapes = float(orchardsandgrapes)
        except:
            raise TypeError("Orchard and Grape data must be a float")

        try:
            alfalfa = float(alfalfa)
        except:
            raise TypeError("Alfalfa data must be a float")

        try:
            pastureandhay = float(pastureandhay)
        except:
            raise TypeError("Pasture and Hay data must be a float")

        try:
            other = float(other)
        except:
            raise TypeError("All 'other' data must be a float")

        totalData = corn + soybeans + wheat + cotton + vegetablesandfruit + rice + orchardsandgrapes + alfalfa + pastureandhay + other
        year_data = {'Corn': corn, "Soybeans": soybeans, "Wheat": wheat, "Cotton": cotton,
                     "Vegetables and Fruit": vegetablesandfruit, "Rice": rice, "Orchards and Grapes": orchardsandgrapes,
                     "Alfalfa": alfalfa, "Pasture and Hay": pastureandhay, "Other": other, "Total": totalData}

        self.compound[fips] = {year: year_data}

        if totalData > self.highest_pesticide_year:
            self.highest_pesticide_year = year
        elif totalData < self.lowest_pesticide_year:
            self.lowest_pesticide_year = year

    def add_yearly_data(self, data):
        """
        adding yearly data by an input year string. A -1 value for any pesticide means that there was no reported data
        :param data: the string that holds all the data for that year
        :return: None
        """
        data = data.split("\t")

        # Making sure that we don't get errors by changing all empty pesticide values into 0
        for i in range(len(data)):
            if data[i] == '':
                data[i] = -1

        fips = data[0]
        try:
            fips = int(fips)
        except:
            raise TypeError("FIPS must be an int")

        state = data[1]

        year = data[3]
        try:
            year = int(year)
        except:
            raise TypeError("Year must be an int")

        units = data[4]

        corn = data[5]
        try:
            corn = float(corn)
        except:
            raise TypeError("Corn data must be a float")

        soybeans = data[6]
        try:
            soybeans = float(soybeans)
        except:
            raise TypeError("Soybean data must be a float")

        wheat = data[7]
        try:
            wheat = float(wheat)
        except:
            raise TypeError("Wheat data must be a float")

        cotton = data[8]
        try:
            cotton = float(cotton)
        except:
            raise TypeError("Cotton data must be a float")

        vegetablesandfruit = data[9]
        try:
            vegetablesandfruit = float(vegetablesandfruit)
        except:
            raise TypeError("Vegetable and Fruit must be a float")

        rice = data[10]
        try:
            rice = float(rice)
        except:
            raise TypeError("Rice data must be a float")

        orchardsandgrapes = data[11]
        try:
            orchardsandgrapes = float(orchardsandgrapes)
        except:
            raise TypeError("Orchard and Grape data must be a float")

        alfalfa = data[12]
        try:
            alfalfa = float(alfalfa)
        except:
            raise TypeError("Alfalfa data must be a float")

        pastureandhay = data[13]
        try:
            pastureandhay = float(pastureandhay)
        except:
            raise TypeError("Pasture and Hay data must be a float")

        other = data[14]
        try:
            other = float(other)
        except:
            raise TypeError("All 'other' data must be a float")

        totalData = corn + soybeans + wheat + cotton + vegetablesandfruit + rice + orchardsandgrapes + alfalfa + pastureandhay + other
        year_data = {"Units": units, 'Corn': corn, "Soybeans": soybeans, "Wheat": wheat, "Cotton": cotton,
                     "Vegetables and Fruit": vegetablesandfruit, "Rice": rice, "Orchards and Grapes": orchardsandgrapes,
                     "Alfalfa": alfalfa, "Pasture and Hay": pastureandhay, "Other": other, "Total": totalData}

        # gotta check if the state already has a key in the dictionary, if not we get an error without fix
        if fips in self.compound:
            self.compound[fips][year] = year_data

        else:
            self.compound[fips] = {year: year_data}

    def getDataforStateYear(self, state, year, type):
        """
        This method will let the user get the data for the a specific year for a given state
        :param state: can be either a state name or it's fips
        :param year: the year of the desired data
        :param type: what kind of data type the user wants
        :return: float value for the amount of pesticide used that year
        """

        if state.isdigit():
            if state in self.compound:
                if year in self.compound[state]:
                    return self.compound[state][year][type]
                else:
                    raise ValueError("Given year ", year, " has not yet been recorded")
            else:
                raise ValueError("State not found")
        else:
            if state.upper() in self.stateMapping:
                state = self.stateMapping.index(state.upper())
                if state in self.compound:
                    if year in self.compound[state]:
                        return self.compound[state][year][type]
                    else:
                        raise ValueError("Given year ", year, " has not yet been recorded")
            else:
                raise ValueError("State not found")

    def getDataBetweenYear(self, state, lower_year, upper_year, type):
        """
        This will get the sum of the data for a state and data type between two given years
        :param state: can be the state fips or the state name
        :param lower_year: the lower year
        :param upper_year: the upper year bound (inclusive)
        :param type: data type that the user wants
        :return: int value for the amount of pesticides used between the given years
        """

        total = 0
        while(lower_year <= upper_year):
            total += self.getDataforStateYear(state, lower_year, type)
            lower_year += 1

        return total


    @classmethod
    def getPesticideDataFromFile(cls, data):
        """
        This file will create a new PesticideData object from the input data
        :param data: this is the raw data from the file
        :return: returns a class method
        """

        raw = data.split("\t")
        # Making sure that we don't get errors by changing all empty pesticide values into 0
        for i in range(len(raw)):
            if raw[i] == '':
                raw[i] = -1

        # catching all the errors that could occur
        fips = raw[0]
        try:
            fips = int(fips)
        except:
            raise TypeError("FIPS must be an int")

        state = raw[1]

        year = raw[3]
        try:
            year = int(year)
        except:
            raise TypeError("Year must be an int")

        units = raw[4]

        corn = raw[5]
        try:
            corn = float(corn)
        except:
            raise TypeError("Corn data must be a float")

        soybeans = raw[6]
        try:
            soybeans = float(soybeans)
        except:
            raise TypeError("Soybean data must be a float")

        wheat = raw[7]
        try:
            wheat = float(wheat)
        except:
            raise TypeError("Wheat data must be a float")

        cotton = raw[8]
        try:
            cotton = float(cotton)
        except:
            raise TypeError("Cotton data must be a float")

        vegetablesandfruit = raw[9]
        try:
            vegetablesandfruit = float(vegetablesandfruit)
        except:
            raise TypeError("Vegetable and Fruit must be a float")

        rice = raw[10]
        try:
            rice = float(rice)
        except:
            raise TypeError("Rice data must be a float")

        orchardsandgrapes = raw[11]
        try:
            orchardsandgrapes = float(orchardsandgrapes)
        except:
            raise TypeError("Orchard and Grape data must be a float")

        alfalfa = raw[12]
        try:
            alfalfa = float(alfalfa)
        except:
            raise TypeError("Alfalfa data must be a float")

        pastureandhay = raw[13]
        try:
            pastureandhay = float(pastureandhay)
        except:
            raise TypeError("Pasture and Hay data must be a float")

        other = raw[14]
        try:
            other = float(other)
        except:
            raise TypeError("All 'other' data must be a float")

        return cls(fips, state, year, units, corn, soybeans, wheat, cotton, vegetablesandfruit, rice, orchardsandgrapes,
                   alfalfa, pastureandhay, other)


def get_CDC_areas_from_file(filename):
    """
    This function will create a dictionary that has state names as the key values and will have the appropriate
    DiseaseTypeArea class as the value pair for that state key
    :param filename: This is a string that represents the filename that will be used to gather the data for the state
    class
    :return: Will return a dictionary
    """

    fobj = open(filename, 'r', encoding='utf-8')
    area_dict = {}
    for line in fobj:

        # formatting the data so that it can be used easily
        line = line.strip("\n")
        new_line = line.split('|')

        # these variables will be used to identify key things that must be fixed before adding the data
        area_name = new_line[0]
        disease_name = new_line[9]

        # This chain of if statements is to facilitate the reading of the disease name. We replace the complicated name
        # with the desired name
        if disease_name == 'Female Breast, <i>in situ</i>':
            line = line.replace('Female Breast, <i>in situ</i>', 'Female Breast - In Situ')
        elif disease_name == 'Corpus and Uterus, NOS':
            line = line.replace('Corpus and Uterus, NOS', 'Corpus and Uterus - NOS')

        # This appears in the first line of the data. It is a format line and we want to skip it
        if new_line[0] == 'AREA':
            continue

        # the lines that have these as years simply provide a summary of the data from 2013-2017. We can skip this
        elif new_line[10] == '2013-2017':
            continue

        # we want to add data if the area name already exists and create a new class instance if it hasn't
        elif area_name in area_dict:

            area_dict[area_name].add_yearly_data(line)

        else:

            area_dict[area_name] = DiseaseTypeArea.get_disease_from_data(line)

    fobj.close()
    return area_dict


def getUSGSDataFromFile(fileUSGS):
    """
    This function gets all the data from the USGS data
    :param fileUSGS: this is the filename
    :return: returns a dictionary mapping different compounds to their PesticideData class
    """
    fobj = open(fileUSGS, 'r', encoding='utf-8')
    pesticide_dict = {}
    for line in fobj:

        line = line.strip("\n")
        # each set of info is separated by a tab delimiter
        new_line = line.split('\t')
        # this dictionary is going to be sorted by compound type
        compound = new_line[2]

        # Want to skip if the first index of the new line  statefipscode because it means that it is the first line
        # and wil create errors since it will not be in the proper formats
        if compound == "Compound":
            continue
        elif compound in pesticide_dict:

            pesticide_dict[compound].add_yearly_data(line)
        else:

            pesticide_dict[compound] = PesticideData.getPesticideDataFromFile(line)

    fobj.close()

    return pesticide_dict


cdc = get_CDC_areas_from_file("BYAREA.TXT")
usgs = getUSGSDataFromFile("HighEstimate_AgPestUsebyCropGroup92to17_v2.txt")
print(usgs["2,4-D"].getDataBetweenYear("Alabama", 1992, 1993, "Corn"))
