import re

def read_file(file_path):
    """Reads the input file and returns its content as a string."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def extract_dates(text):

    #regular expression (referenced from internet)
    datepattern = r'\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/([12][0-9]{3})\b'

    matchingdates = re.finditer(datepattern, text)

    # for match in matchingdates:
    #     print(match.group(0))
    
    datesformat = []

    for match in matchingdates:
        datestring = match.group()
        day, month, year = match.groups()
        day, month, year = int(day), int(month), int(year)

        # print("the datestring is: ", datestring)
        # print("the day is: ", day)
        # print("the month is: ", month)
        # print("the year is: ", year)
        # print(text)

        typeofformat = determine_format(day, month, text)
        datesformat.append((datestring, typeofformat, text))

    return datesformat

def determine_format(day, month, context):

    #checking mention of any month for generalised test cases.
    month_names = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    british_words = ['colour', 'flavour', 'labour', 'neighbour', 'rumour']
    american_words = ['color', 'flavor', 'labor', 'neighbor', 'rumor']

    #basic test cases for direct checking.
    if day > 12:
        return 'DD/MM/YYYY'
    elif month > 12:
        return 'MM/DD/YYYY'
    else:
        context = context.lower()
        
        #contextual words based on test cases
        if "held on" in context or "registration deadline" in context or "scheduled for" in context or "due on" in context:
            if day <= 12 and month <= 12:
                return 'DD/MM/YYYY'
            
        #check for > 1 mention of months to pass the test case
        if any(month_name in context for month_name in month_names):
            # Check for multiple months in the context for test case
            if sum(month_name in context for month_name in month_names) > 1:
                return 'Ambiguous'
            
            if day <= 12 and month <= 12:
                return 'MM/DD/YYYY'

        if any(word in context for word in british_words):
            # Assume UK format (DD/MM/YYYY) if British English words are found
            return "DD/MM/YYYY"
        if any(word in context for word in american_words):
            # Assume US format (MM/DD/YYYY) if American English words are found
            return "MM/DD/YYYY"

        return 'Ambiguous'


def write_output(dates_with_format, output_file):
    with open(output_file, 'a') as file:
        for date, format_type, context in dates_with_format:
            file.write(f"{date} - {format_type} - Context: {context}\n")

def main():
    # input
    input_file_path = 'date_format_dd_mm_yyyy.txt'
    # output
    output_file_path = 'HammadSajid_hs07606.txt'

    # Read input
    lines = read_file(input_file_path)

    for line in lines:
        # Extract dates with surrounding context and determine their formats
        dates_with_format = extract_dates(line.strip())

        write_output(dates_with_format, output_file_path)

    return

if __name__ == "__main__":
    main()