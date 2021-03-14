'''
This is the last file for the cancer data project. This file will use the data from the other files in the
project and will do analytical tests between them
Author: Juan David Guerra First Year Computer Science and Neuroscience student at McGill University
Start data of this file: March 13, 2021
'''

import sort_data
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt


def linRegbyState(usgsyearlower,usgsyearupper,cdc_year_lower, cdc_year_upper, compound, crop, disease, usgsfile, cdcfile):
    """
    This function will create a linear regression checking the correlation between the two inputs
    Will erturn the value fo the linear regression
    :param usgsyear: the desired data year for the pesticide use
    :param cdcyear: the desired data year for the cdc cancer data
    :param compound: the compound that the user wants the data for
    :param crop: the crop type that the user would like to analyze
    :param disease: the disease that the user wants to analyze
    :return: the slope of the linear regression
    """

    pesticideArray = []
    cdcArray = []

    usgsData = sort_data.getUSGSDataFromFile(usgsfile)
    cdcData = sort_data.get_CDC_areas_from_file(cdcfile)

    for stateFIPS in usgsData[compound].compound:
        # going through all the states in the USA
        state = sort_data.PesticideData.stateMapping[stateFIPS]
        if state in cdcData:
            pesticideArray.append(usgsData[compound].getDataBetweenYear(str(stateFIPS), usgsyearlower, usgsyearupper,  crop))
            cdcArray.append(cdcData[state].get_data_between_years_by_disease_type(disease, 'Incidence', cdc_year_lower, cdc_year_upper, 'count'))

    x = np.array(pesticideArray).reshape((-1, 1))  # getting the transpose of the usgs data array to get lin regression
    y = np.array(cdcArray)

    regression = LinearRegression()
    regression.fit(x, y)

    print("R squared value: ", regression.score(x, y))
    print("Linear Regression (slope): ", regression.coef_)

    plt.title("Correlation Graph of Compound: " +compound+" used on crop type: "+ crop+ " and Cancer Type: "+disease)
    plt.xlabel("Amount (in kg) of " + compound + "used on crop type: " + crop + " in years " + str(usgsyearlower) + '-' + str(usgsyearupper))
    plt.ylabel("Incidence of " + disease+ "in years " + str(cdc_year_lower) + '-' + str(cdc_year_upper))
    plt.scatter(x, y)
    plt.show()
    return regression.coef_


linReg = linRegbyState(2006, 2007, 2016, 2017, 'GLYPHOSATE', "Total", 'Non-Hodgkin Lymphoma',
                       "HighEstimate_AgPestUsebyCropGroup92to17_v2.txt", "BYAREA.TXT")
