# -------------------------------------
#   Author: Sotirios Kougiouris
#   Date: 9 / 3 / 2024
#   Description: A script to parse configuration files in order to see what settings/configs are missing from which files. Gig done for Lenny Giuliano.
#   Usage: python config_parser.py input-directory outputfile
# -------------------------------------

import os
import sys

def parse_file(path, excluded):
    settings = set()
    with open(path, 'r') as file:
        for line in file:
            # adding all the config settings to a set to cross reference with other files
            if line.startswith('set'):
                only_settings = ""
                for word in line.split():
                    # excluding the values
                    if(any(i.isdigit() for i in word) or (word in excluded)):
                        break
                    only_settings += word + ' '
                
                # adding the config to the file's list of settings
                config = ' '.join(only_settings.strip().split())
                settings.add(config)
    return settings

def compare_files(files, excluded):
    general_settings = set()
    counts = {}
    individual_file_settings = {}

    for file in files:
        # get settings of current file
        settings = parse_file(file, excluded)
        # getting how many times each setting appeared in the directory
        for setting in settings:
            counts[setting] = counts.get(setting, 0) + 1
        individual_file_settings[file] = settings
        general_settings.update(settings)
    
    diffs = {}
    # checking if anything is missing
    for file, settings in individual_file_settings.items():
        # using the set minus (-) in order to get settings that aren't overlapping
        missing = general_settings - settings
        if missing:
            diffs[file] = sorted(missing)
    
    return diffs, counts, len(files)

def main(input_dir, output_file):
    # getting any settings to exclude
    print('Please enter the settings/word that you want ignored and press ENTER:\n  (i.e. everything after this word will not be considered)\n  (numbers are already excluded)\n  (for multiple, enter them with A SPACE in between)\n  (simply press ENTER to skip)')
    # checking the Python version because raw_input() and input() have changed from Python 2 -> 3
    if(sys.version_info[0] < 3):
        excluded = raw_input().split()
    else:
        excluded = input().split()
    
    # getting the minimum percentage threshold to display
    print('\nPlease enter the minimum percentage threshold to display a missing setting and press ENTER:\n  (i.e. if any setting appears in less than this percentage of files, it will not be listed as a missing setting)\n  (ONLY enter integers, nothing else)\n  (simply press ENTER to skip and see all percentages)')
    # checking the Python version because raw_input() and input() have changed from Python 2 -> 3
    if(sys.version_info[0] < 3):
        threshold = raw_input()
    else:
        threshold = input()
    # ensuring the user entered an integer
    if(threshold):
        threshold = int(threshold)

    # excluding any Python files from the files to read
    config_files = [(input_dir + '/' + i) for i in os.listdir(input_dir) if (not i.endswith('.py'))]
    if not config_files:
        print("No files found in the current directory")
        return
    
    differences, counts, file_count = compare_files(config_files, excluded)

    # writing the missing config settings
    with open(output_file, "w") as f:
        if differences:
            f.write("Here are some discrepancies between the files:\n")
            for file, missing in differences.items():
                f.write(file + " is missing:\n")
                sorted_by_percentage = {}
                for setting in missing:
                    # getting the percentage of files this setting/config appears in, if selected
                    percentage = (counts[setting] / float(file_count)) * 100
                    # ensuring each setting is sorted by percentage
                    sorted_by_percentage[setting] = sorted_by_percentage.get(setting, percentage)
                
                for setting in sorted(sorted_by_percentage, key=sorted_by_percentage.get, reverse=True):
                    if threshold:
                        if(sorted_by_percentage[setting] >= threshold):
                            f.write("  - " + setting + " (appeared in " + '{0:.0f}'.format(sorted_by_percentage[setting]) + "% of files in the directory)\n")
                    else:
                        f.write("  - " + setting + " (appeared in " + '{0:.0f}'.format(sorted_by_percentage[setting]) + "% of files in the directory)\n")
        else:
            f.write("No discrepancies found!\n")

if __name__ == "__main__":
    try:
        # getting command line options
        input_dir = sys.argv[1]
        output_file = sys.argv[2]
        main(input_dir, output_file)
    except Exception as e:
        print("\n\nSomething went wrong:\n" + str(e))
        print("\nUsage:\n    python config_parser.py input-directory outputfile\n\n")

