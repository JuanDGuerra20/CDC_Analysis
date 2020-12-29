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
        Constructor making the class
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
        >>> area.incidence_data
        {1999: {'count': 9299, 'population': 2293259, 'age adjusted rate': 367.2, 'crude rate': 405.5, 'race': 'All Races', 'sex': 'Female'}, 2000: {'count': 9299, 'population': 2293259, 'age adjusted rate': 367.2, 'crude rate': 405.5, 'race': 'All Races', 'sex': 'Female'}}

        """

        # splitting the input data at the delimiter (|)
        data = data.split('|')

        # assigning the desired data types to the proper variables and making sure they are the correct type
        age_adjusted_rate = data[3]
        try:
            age_adjusted_rate = float(age_adjusted_rate)

        except:
            raise TypeError("Incorrect data type: age adjusted rate must be a float")

        count = data[4]
        try:
            count = int(count)
        except:
            raise TypeError("Incorrect data type: count must be an int")

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


if __name__ == '__main__':
    doctest.testmod()
