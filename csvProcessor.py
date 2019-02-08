import csv
import pycountry


class Processor:

    def __init__(self, path):
        self.path = path

    def csv_prcessr(self, input_file_path, output_file_path):

        with open(input_file_path, 'r', newline='') as inputFile:
            fieldnames = ['date', 'state name', 'impressions', 'CTR']
            input_reader = csv.DictReader(inputFile, fieldnames=fieldnames)
            input_data = list(input_reader)

            new_data_format = self.convert_date(input_data)
            country_alpha3_code = self.country_decoder(input_data)

    @staticmethod
    def convert_date(input_data):

        new_date_list = []
        new_date_format = []

        for i in range(len(input_data)):
            date = input_data[i][0]
            splited_date = date.split("/")
            new_date_list.append(splited_date[2])
            new_date_list.append(splited_date[0])
            new_date_list.append(splited_date[1])
            separator = "-"
            new_date_format.append(separator.join(new_date_list))
            new_date_list = []

        return new_date_format

    @staticmethod
    def country_decoder(input_data):
        country_alpha3_code = []
        for i in range(len(input_data)):

            try:
                subdivision = pycountry.subdivisions.lookup(input_data[i][1])
                country = pycountry.countries.get(alpha_2=subdivision.country_code)
                country_alpha3_code.append(country.alpha_3)
            except LookupError:
                country_alpha3_code.append("XXX")
        return country_alpha3_code
