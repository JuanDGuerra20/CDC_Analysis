"""
Author Juan David Guerra. First year student at McGill university. B.Sc Computer science minor in neuroscience
Start Date: December 28, 2020
Outline: This module will reformat the data from the CDC on the different types of cancer and make them useful for
correlation tests and other things yet to be found in the future
"""


def create_files(filename_in):
    """
    This function takes in the raw data from the cdc and creates a new file where only the type of cancer that
    we want to analyze is in
    :param filename_in: this will be the original CDC file containing all the raw data from all types of cancer. TXT
    :return: will return the amount of lines added to the output file. INT
    """

    # getting the file object
    fobj_in = open(filename_in, 'r', encoding='utf-8')

    # creating the line counter. this is what will be returned. Basically a check to make sure we went through all the
    # lines in the file and didn't miss any data by accident
    line_counter = 0
    # this is gonna be the check to see if we must add the data to a different file
    cancer_check = ''

    # looping through all the lines in the input file
    for line in fobj_in:

        # This caused a problem in the first iteration because the first line describes the format. Do not want to make
        # a file like this so we skip the first iteration of the loop
        # Also want to find at what spot the CDC is putting the type of cancer so we can use this code on all their data
        if line_counter == 0:

            # creating a file that will have the format of the rest of the files
            fobj_out = open('format.txt', 'w', encoding='utf-8')
            fobj_out.write(line)

            # splitting the line at the delimiter (always going to be |)
            line = line.split('|')

            # looping through all the data types in the first line (first line always tells us the data types)
            for i in range(len(line)):
                # SITE is the the type of cancer they have. Wherever this is located is where all cancers will be
                if line[i] == 'SITE':
                    # setting the cancer location to be the index
                    cancer_location = i
                    break  # stopping the loop to not take up more time than needed

            line_counter += 1
            continue

        # Getting the type of cancer by splitting the line by the delimiters (|) and accessing the index of the cancer
        # through the loop done in line 34
        cancer_type = line.split('|')
        cancer_type = cancer_type[cancer_location]

        # There was an issue with the first instance of this so I just made it work on the first. Unresolvable issue
        # First part of the statement is checking if the cancer is different from the previous iteration. If so, open
        # the appropriate file
        if cancer_check != cancer_type[:len(cancer_check)] or line_counter == 1:
            # creating the name of the file that must be opened by lower casing it and replacing spaces by _
            new_name = cancer_type.lower()
            new_name = new_name.replace(' ', '_')
            # opening the file and using 'a' because we don't want to reset the file everytime we open
            fobj_out = open(new_name + '_' + filename_in.lower(), 'a', encoding='utf-8')

            # setting the cancer_checker to be
            cancer_check = cancer_type

        # writing the line to the appropriate file
        fobj_out.write(line)

        # incrementing the line counter by one for each iteration
        line_counter += 1

    # closing the files
    fobj_in.close()
    fobj_out.close()
    return line_counter  # returning the number of lines iterated through
