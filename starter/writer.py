from enum import Enum


class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object used to write the results from supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        pass

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # TODO: Using the OutputFormat, how can we organize our 'write' logic for output to stdout vs to csvfile
        # TODO: into instance methods for NEOWriter? Write instance methods that write() can call to do the necessary
        # TODO: output format.
        if format == OutputFormat.display.value:
            return self.display(data)
        else:
            self.write_to_csv_file()

    def display(self, data):
        print(data)
        return True

    def write_to_csv_file(self):
        pass
