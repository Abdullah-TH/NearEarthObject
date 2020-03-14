from models import OrbitPath, NearEarthObject
import csv


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        self.filename = filename
        self.orbit_date_to_neos = {}
        self.neos = {}

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                neo_attributes_list = list(row.items())[:14]
                neo_attributes_dict = dict(neo_attributes_list)
                orbit_attributes_list = list(row.items())[14:]
                orbit_attributes_dict = dict(orbit_attributes_list)
                neo = NearEarthObject(**neo_attributes_dict)
                orbit = OrbitPath(**orbit_attributes_dict)

                orbit_date_key = orbit.close_approach_date
                if self.orbit_date_to_neos.get(orbit_date_key) is None:
                    self.orbit_date_to_neos[orbit_date_key] = [neo]
                else:
                    self.orbit_date_to_neos[orbit_date_key].append(neo)

                self.neos[neo.name] = neo

        return None
