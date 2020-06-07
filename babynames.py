#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

import sys
import re
import glob


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """

    # Extracting the year
    year_match = re.search(r'\d\d\d\d', filename)
    if not year_match:
        sys.stderr.write('Could not find a year!\n')
        sys.exit()
    year = year_match.group()

    # Opening the file
    try:
        with open(filename) as file:
            data = file.read()
    except FileNotFoundError:
        sys.stderr.write('There is no such file in the directory!\n')
        sys.exit()

    # Finding patterns
    regex = re.compile(r'<td>\w+')
    names = regex.findall(data)
    for i in range(len(names)):
        names[i] = names[i].replace('<td>', '')

    # Creating a dictionary with names data
    names_dict = {}
    for i in range(0, len(names) - 2, 3):
        key = names[i]
        names_dict[key] = [names[i + 1], names[i + 2]]

    # Creating a list with result
    boy_names = []
    girl_names = []
    result = [year]
    for key, value in names_dict.items():
        if value[0] not in boy_names:
            result.append(value[0] + ' ' + key)
            boy_names.append(value[0])
        if value[1] not in girl_names:
            result.append(value[1] + ' ' + key)
            girl_names.append(value[1])

    result.sort()
    # result.insert(0, year)

    return result


def main():
    # TThis is for windows command line to take argument like: 'baby*.html'.
    # Otherwise the program doesn't work with this argument.
    if '*' in sys.argv[-1]:
        sys.argv[-1:] = glob.glob(sys.argv[-1])

    # Only necessary arguments
    args = sys.argv[1:]

    # If a user doesn't give any arguments, he receive this line with explanation how to use the program.
    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    if summary:
        for file in args:
            result = extract_names(file)
            file_name = 'baby' + str(result[0]) + '.summary'
            string = '\n'.join(result) + '\n'
            with open(file_name, 'w') as f:
                f.write(string)
    else:
        for file in args:
            result = extract_names(file)
            print('\n'.join(result) + '\n')
    print('The process is finished successfully.')


if __name__ == '__main__':
    main()
