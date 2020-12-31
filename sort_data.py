"""
Author: Juan David Guerra. First year Computer Science student at McGill University B.Sc.
Start Date: December 28, 2020
Outline: This module will hold the classes and methods needed to organize the data so we can easily access it
"""

import doctest


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
        self.disease = disease_type
        # creating the dictionaries that will hold the incidence and mortality data
        self.incidence_data = {}
        self.mortality_data = {}
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
            self.incidence_data[data_year] = {'count': count, 'population': population,
                                              'age adjusted rate': age_adjusted_rate, 'crude rate': crude_rate,
                                              'race': race, 'sex': sex}

        # doing the same as the above if statement but in the mortality_data dictionary
        elif count_type == "Mortality":
            self.mortality_data[data_year] = {'count': count, 'population': population,
                                              'age adjusted rate': age_adjusted_rate, 'crude rate': crude_rate,
                                              'race': race, 'sex': sex}
        # if the count_type is not Incidence or Mortality, we want to raise a value error since those are the only types
        # of count_types we are taking into account for this type of disease
        else:
            raise ValueError("Unsupported count_type: must be either Incidence or Mortality")

    def __str__(self):
        """
        overloading the str function to output what I want it to.
        :return:
        """

        return "Disease: " + self.disease + '\tArea: ' + self.area + '\nIncidence data: ' + str(self.incidence_data) + \
               '\nMortality data: ' + str(self.mortality_data)

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
        >>> area.incidence_data
        {1999: {'count': 9299, 'population': 2293259, 'age adjusted rate': 367.2, 'crude rate': 405.5, 'race': 'All Races', 'sex': 'Female'}, 2000: {'count': 9299, 'population': 2293259, 'age adjusted rate': 367.2, 'crude rate': 405.5, 'race': 'All Races', 'sex': 'Female'}}

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
        if '-' in data:
            data = data.replace('-', '-1')

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
            raise TypeError("Incorrect data type: crude rate must be a float")

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

        # adding a year of data to the incidence dictionary or replacing the data year with the new input
        if count_type == "Incidence":
            self.incidence_data[data_year] = {'count': count, 'population': population,
                                              'age adjusted rate': age_adjusted_rate, 'crude rate': crude_rate,
                                              'race': race, 'sex': sex}

        # adding a year of data to the mortality dictionary or replacing the data year with the new input
        elif count_type == "Mortality":
            self.mortality_data[data_year] = {'count': count, 'population': population,
                                              'age adjusted rate': age_adjusted_rate, 'crude rate': crude_rate,
                                              'race': race, 'sex': sex}
        # if the count_type is not Incidence or Mortality, we want to raise a value error since those are the only types
        # of count_types we are taking into account for this type of disease
        else:
            raise ValueError("Unsupported count_type: must be either Incidence or Mortality")

    def get_incidence_count_by_year(self, year):
        """
        This instance method will get the incidence count for a given year. Will return a KeyError if there is no count
        for that year
        :param year: int
        :return: int - The incidence count of the disease type

        Examples:
        >>> area = DiseaseTypeArea('Alabama', 'All Cancer Sites Combined', 367.2, 9299, 'Incidence', 2293259,\
        "All Races", 'Female', 1999, 405.5)
        >>> area.get_incidence_count_by_year(1999)
        9299
        >>> area.get_incidence_count_by_year(1000)
        That year of data has not been added and cannot be accessed
        0
        """

        # trying to get the count of a given year. If not possible it's because that year has not been added yet
        if year in self.incidence_data:
            return self.incidence_data[year]['count']

        # the following only runs if the year has not been recorded. Print a statement explaining the situation
        # want to return 0 if there was no year
        print("That year of data has not been added and cannot be accessed")
        return 0

    def get_mortality_count_by_year(self, year):
        """
        This instance method will get the mortality count for a given year. Will return 0 if there is no
        count for that year
        :param year: int
        :return: int - mortality count for a given year

        Examples:
        >>> area = DiseaseTypeArea('Alabama', 'All Cancer Sites Combined', 367.2, 9299, 'Mortality', 2293259,\
        "All Races", 'Female', 1999, 405.5)
        >>> area.get_mortality_count_by_year(1999)
        9299
        """

        # trying to get the count of a given year. If not possible it's because that year has not been added yet
        if year in self.mortality_data:
            return self.mortality_data[year]['count']

        # the following only runs if the year has not been recorded. Print a statement explaining the situation
        # want to return 0 if there was no year
        print('That year has not been added to the data of mortality')
        return 0

    def get_incidence_crude_rate_by_year(self, year):
        """
        This method gets the incidence crude rate for a given input year. Will return 0 if that year does not exist
        :param year: int
        :return: incidence crude rate
         >>> area = DiseaseTypeArea('Alabama', 'All Cancer Sites Combined', 367.2, 9299, 'Incidence', 2293259,\
        "All Races", 'Female', 1999, 405.5)
        >>> area.get_incidence_crude_rate_by_year(1999)
        405.5
        """

        # trying to get the crude rate of a given year. If not possible it's because that year has not been added yet
        if year in self.incidence_data:
            return self.incidence_data[year]['crude rate']

        # the following only runs if the year has not been recorded for that count_type
        # Print a statement explaining the situation want to return 0 if there was no year
        print('That year has not been added to the data of incidence data')
        return 0.0

    def get_mortality_crude_rate_by_year(self, year):
        """
        This method gets the mortality crude rate for a given input year. Will return 0 if that year does not exist
        :param year: int
        :return: the crude mortality rate. 0 if there is none
        >>> area = DiseaseTypeArea('Alabama', 'All Cancer Sites Combined', 367.2, 9299, 'Mortality', 2293259,\
        "All Races", 'Female', 1999, 405.5)
        >>> area.get_mortality_crude_rate_by_year(1999)
        405.5
        """

        # trying to get the crude rate of a given year. If not possible it's because that year has not been added yet
        if year in self.mortality_data:
            return self.mortality_data[year]['crude rate']

        # the following only runs if the year has not been recorded for that count_type
        # Print a statement explaining the situation want to return 0 if there was no year
        return 0.0

    def get_incidence_data_between_years(self, data_type, lower_end, upper_end):
        """
        This function will get the total incidence numbers between the lower_end and upper_end years
        :param data_type: The data that the user wants to obtain. Could be 'count' or 'population', etc.
        :param lower_end: The year that the person wants to start getting the data from
        :param upper_end: The last year that data is to be obtained
        :return: int that represents the total number of incidences between the given years
        """

        # this int variable will hold the sum of all the incidence cases of all the years within the range
        incidence_counter = 0

        # looping through the years in the data and checking if they are within the range
        for year in self.incidence_data:

            if lower_end <= year <= upper_end:
                # if they are in the range, add the count of incidence to the incidence counter
                incidence_counter += self.incidence_data[year][data_type]

        # returning the incidence numbers in the age
        return incidence_counter

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
        if '-' in data:
            data = data.replace('-', '-1')

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
            raise TypeError("Incorrect data type: crude rate must be a float")

        count = data[4]

        if count == '.':
            count = (crude_rate*population)/100000
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

        new_line = line.split('|')

        area_name = new_line[0]

        if area_name == 'Female Breast, <i>in situ</i>':
            area_name = 'Female Breast, In Situ'

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


dict_of_areas = get_areas_from_file('BYAREA.TXT')
print(dict_of_areas)

if __name__ == '__main__':
    doctest.testmod()
