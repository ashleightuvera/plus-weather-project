import csv
from datetime import datetime

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    # """Takes a temperature and returns it in string format with the degrees
    #     and celcius symbols.

    # Args:
    #     temp: A string representing a temperature.
    # Returns:
    #     A string contain the temperature and "degrees celcius."
    # """

    return f"{temp}{DEGREE_SYBMOL}"


def convert_date(iso_string):
    # """Converts and ISO formatted date into a human readable format.

    # Args:
    #     iso_string: An ISO date string..
    # Returns:
    #     A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    # """
    if not isinstance(iso_string, str):
        raise ValueError("Input must be a string")

    # Convert the input date string to a datetime object
    input_datetime = datetime.fromisoformat(iso_string)

    # Leap year
    is_leap_year = (input_datetime.year % 4 == 0 and input_datetime.year % 100 != 0) or (input_datetime.year % 400 == 0)

    # First day of the month
    is_first_day = input_datetime.day == 1

    # Last day of the month
    year = input_datetime.year
    month = input_datetime.month

    # List of days in each month, considering a non-leap year
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Adjust for a leap year
    if is_leap_year:
        days_in_month[1] = 29  # February has 29 days in a leap year

    last_day = days_in_month[month - 1]
    is_last_day = input_datetime.day == last_day

    # Format the date according to the specified conditions
    formatted_date = input_datetime.strftime("%A %d %B %Y")

    return formatted_date

pass


def convert_f_to_c(temp_in_farenheit):
    # """Converts an temperature from farenheit to celcius.

    # Args:
    #     temp_in_farenheit: float representing a temperature.
    # Returns:
    #     A float representing at emperature in degrees celcius, rounded to 1dp.
    # """
    try:
        # Convert the input to a float if it's a string
        temp_in_farenheit = float(temp_in_farenheit)
                # previous temp_in_farenheit = float(temp_in_farenheit)

        # Check if it's a valid temperature value
        if isinstance(temp_in_farenheit, (int, float)):
            # Perform the conversion
            temp_in_celsius = (temp_in_farenheit - 32) * 5/9
            return round(temp_in_celsius, 1)  # Round to one decimal place

        else:
            raise ValueError("Invalid temperature value")

    except ValueError as e:
        print(f"Error: {e}")
        return None
pass


def calculate_mean(weather_data):
    # """Calculates the mean value from a list of numbers.

    # Args:
    #     weather_data: a list of numbers.
    # Returns:
    #     A float representing the mean value.
    # """
    if not weather_data:
        raise ValueError("Input list is empty")

    # converting items to floats
    try:
        temperatures = [float(value) for value in weather_data]
    except ValueError as e:
        raise ValueError("Input list contains non-numeric values") from e

    # Calculate mean
    mean_value = sum(temperatures) / len(temperatures)
    return mean_value
pass


def load_data_from_csv(csv_file):
    # """Reads a csv file and stores the data in a list.

    # Args:
    #     csv_file: a string representing the file path to a csv file.
    # Returns:
    #     A list of lists, where each sublist is a (non-empty) line in the csv file.
    # """
    data = []

    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        
        # Skip the header row
        next(csv_reader, None)
        
        for row in csv_reader:
            # Check if the row has at least three elements before attempting conversion
            if len(row) >= 3:
                try:
                    # Convert the second and third elements to integers
                    row[1] = int(row[1])
                    row[2] = int(row[2])
                    data.append(row)
                except ValueError:
                    pass  # Ignore rows with non-numeric values
            else:
                pass  # Ignore incomplete rows

    return data
pass


def find_min(weather_data):
    # """Calculates the minimum value in a list of numbers.

    # Args:
    #     weather_data: A list of numbers.
    # Returns:
    #     The minium value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    # """

    if not weather_data or not all(isinstance(value, (int, float, str)) for value in weather_data):
        return ()

    try:
        # Convert strings to float if necessary
        weather_data = [float(value) for value in weather_data]
    except ValueError:
        return ()

    min_value = weather_data[0]
    min_index = 0

    for i, value in enumerate(weather_data):
        if value <= min_value:
            min_value = value
            min_index = i
            # min_entry = weather_data[min_index][1]

    return min_value, min_index

pass


def find_max(weather_data):
    # """Calculates the maximum value in a list of numbers.

    # Args:
    #     weather_data: A list of numbers.
    # Returns:
    #     The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    # """

    if not weather_data or not all(isinstance(value, (int, float, str)) for value in weather_data):
        return ()

    try:
        # Convert strings to float if necessary
        weather_data = [float(value) for value in weather_data]
    except ValueError:
        return ()

    max_value = weather_data[0]
    max_index = 0

    for i, value in enumerate(weather_data):
        if value >= max_value:
            max_value = value
            max_index = i

    return max_value, max_index

pass


def generate_summary(weather_data):
    # """Outputs a summary for the given weather data.

    # Args:
    #     weather_data: A list of lists, where each sublist represents a day of weather data.
    # Returns:
    #     A string containing the summary information.
    # """
    for entry in weather_data:
        entry[1] = convert_f_to_c(entry[1])
        entry[2] = convert_f_to_c(entry[2])

    # Find min, max, average
    min_temp, min_temp_index = find_min([item[1] for item in weather_data])
    max_temp, max_temp_index = find_max([item[2] for item in weather_data])
    average_low = calculate_mean([entry[1] for entry in weather_data])
    average_high = calculate_mean([entry[2] for entry in weather_data])

    # Format dates
    min_temp_date = convert_date(weather_data[min_temp_index][0])
    max_temp_date = convert_date(weather_data[max_temp_index][0])

    # Generate summary
    summary = f"{len(weather_data)} Day Overview\n"
    summary += ( 
                 f"  The lowest temperature will be {min_temp:.1f}°C, and will occur on {min_temp_date}.\n"
                 f"  The highest temperature will be {max_temp:.1f}°C, and will occur on {max_temp_date}.\n"
                 f"  The average low this week is {average_low:.1f}°C.\n"
                 f"  The average high this week is {average_high:.1f}°C.\n"
                )       

    return summary

    pass

def generate_daily_summary(weather_data):
    # """Outputs a daily summary for the given weather data.

    # Args:
    #     weather_data: A list of lists, where each sublist represents a day of weather data.
    # Returns:
    #     A string containing the summary information.

    # """
    summary = ""

    for entry in weather_data:
        iso_date, min_temp, max_temp = entry
        formatted_date = convert_date(iso_date)
        min_temp_celsius = convert_f_to_c(min_temp)
        max_temp_celsius = convert_f_to_c(max_temp)

        summary += (
                                f"---- {formatted_date} ----\n"
                                f"  Minimum Temperature: {min_temp_celsius}°C\n"
                                f"  Maximum Temperature: {max_temp_celsius}°C\n\n"
                              )

    return summary

    pass
