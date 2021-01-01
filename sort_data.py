"""
Author: Juan David Guerra. First year Computer Science student at McGill University B.Sc.
Start Date: December 28, 2020
Outline: This module will hold the classes and methods needed to organize the data so we can easily access it
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

        # doing the same as the above if statement but in the mortality_data dictionary
        elif count_type == "Mortality":
            mortality_data[data_year] = {'count': count, 'population': population,
                                         'age adjusted rate': age_adjusted_rate, 'crude rate': crude_rate,
                                         'race': race, 'sex': sex}
            self.disease[disease_type] = {'Incidence': {}, 'Mortality': mortality_data}

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

            # adding a year of data to the mortality dictionary or replacing the data year with the new input
            elif count_type == "Mortality":
                self.disease[disease_type]['Mortality'][data_year] = {'count': count, 'population': population,
                                                                      'age adjusted rate': age_adjusted_rate,
                                                                      'crude rate': crude_rate,
                                                                      'race': race, 'sex': sex}

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

    def get_count_by_disease_year(self, disease, count_type, year):
        """
        This instance method will get the count of a input count_type for a given disease and year
        Will return a KeyError if there is no count
        for that year
        :param disease: This string represents the disease that the user is searching for the count
        :param count_type: This string represents the count type that the user wants
        :param year: int representing the year of the desired count
        :return: int - The incidence count of the disease type
        """

        if disease not in self.disease:
            raise KeyError("The disease has not been added to the list of diseases for this area")

        # getting the count for the given parameters
        count = self.disease[disease][count_type][year]['count']

        return count

    def get_incidence_count_between_years(self, disease, count_type, lower_end, upper_end):
        """
        This function will get the total incidence numbers between the lower_end and upper_end years
        :param disease: This is the disease type that the user will be searching for
        :param count_type: The data that the user wants to obtain. Could be 'count' or 'population', etc.
        :param lower_end: The year that the person wants to start getting the data from
        :param upper_end: The last year that data is to be obtained
        :return: int that represents the total number of incidences between the given years
        """

        if disease not in self.disease:
            raise KeyError("The disease has not been added to the list of diseases for this area")

        count = 0

        # looping through all the years for the given disease and checking if it is within the range given
        for year in self.disease[disease][count_type]:

            if lower_end <= year <= upper_end:

                # adding the count for the year iteration that meets the requirements to the sum of counts
                count += self.disease[disease][count_type][year]['count']

        return count


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


def get_areas_from_file(filename):
    """
    This function will create a dictionary
    :param filename:
    :return:
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
