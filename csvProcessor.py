import csv
import pycountry


class Processor:
    """
    Processor class which accepts two parameters:
    :param input_file_path: path to csv file you wont to convert like path/to/file/fileName.csv
    :param output_file_path: record path and proccesed data file name like record/path/fileName.csv
    """

    def csv_processor(self, input_file_path, output_file_path):
        """
            This function onverts the csv file in the following way:

                input file format:
                mm/dd/yyyy, state name, impressions, CTR

        """
        with open(input_file_path, 'r', newline='') as inputFile:
            fieldnames = ['date', 'state name', 'impressions', 'CTR']
            input_reader = csv.DictReader(inputFile, fieldnames=fieldnames)
            input_data = list(input_reader)

            new_data_format = self._convert_date(input_data)
            country_alpha3_code = self._country_decoder(new_data_format)
            click_amount = self._click_amount(country_alpha3_code)
            sorted_data = self._sorting(click_amount)

        with open(output_file_path, "w", newline="") as outputFile:
            fieldnames = ['date', 'country', 'impressions', 'number of clicks']
            output_writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
            output_writer.writeheader()
            for row in sorted_data:
                output_writer.writerow(row)

    @staticmethod
    def _convert_date(input_data):
        for row in input_data:
            try:
                splitted_date = row['date'].split('/')
                row['date'] = '-'.join([splitted_date[2], splitted_date[0], splitted_date[1]])
            except IndexError:
                return "Wrong date format. Should be dd/mm/yyyy"

        return input_data

    @staticmethod
    def _country_decoder(input_data):
        """

        :param input_data:
        :return:
        """
        for row in input_data:
            try:
                subdivision = pycountry.subdivisions.lookup(row['state name'])
                country = pycountry.countries.get(alpha_2=subdivision.country_code)
                row['country'] = country.alpha_3
                del row['state name']
            except LookupError:
                row['country'] = 'XXX'
                del row['state name']

        return input_data

    @staticmethod
    def _click_amount(input_data):
        for i in range(len(input_data)):

            try:
                cliks = round(int(input_data[i]['impressions']) * (float(input_data[i]['CTR'].rstrip("%")) / 100))
                input_data[i]['number of clicks'] = cliks
                del input_data[i]['CTR']
            except KeyError:
                pass

        return input_data

    @staticmethod
    def _sorting(input_data):

        sorted_data = sorted(input_data, key=lambda i: (i['date'], i['country']))

        for i in range(len(sorted_data) + 1):
            try:
                if sorted_data[i]['date'] == sorted_data[i + 1]['date'] and \
                        sorted_data[i]['country'] == sorted_data[i + 1]['country']:
                    a = int(sorted_data[i]['impressions'])
                    b = int(sorted_data[i + 1]['impressions'])
                    c = int(sorted_data[i]['number of clicks'])
                    d = int(sorted_data[i + 1]['number of clicks'])

                    sorted_data[i]['impressions'] = a + b
                    sorted_data[i]['number of clicks'] = c + d
                    del sorted_data[i + 1]

            except IndexError:
                pass

        return sorted_data


Processor().csv_processor('example.csv', 'output.csv')
