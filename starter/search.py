import operator

from collections import namedtuple, defaultdict
from enum import Enum
from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath
from datetime import datetime


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?
        self.__parameters = kwargs

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        date_search = self.__build_date_search()
        return_object = self.ReturnObjects[self.__parameters["return_object"]]
        selectors = self.Selectors(date_search, self.__parameters["number"], None, return_object)
        return selectors

    def __build_date_search(self):
        date = self.__parameters.get("date")
        start_date = self.__parameters.get("start_date")
        end_date = self.__parameters.get("end_date")
        if date is not None:
            return self.DateSearch(DateSearch("equals"), [date])
        elif start_date is not None or end_date is not None:
            return self.DateSearch(DateSearch("between"), [start_date, end_date])
        else:
            return None


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        'is_hazardous': 'is_potentially_hazardous_asteroid',
        'diameter': 'estimated_diameter_max_kilometers',
        'distance': 'miss_distance_kilometers'
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
        '=': operator.eq,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param object:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param filter_options: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and
        #  value of empty list or list of Filters
        # NOTE: I'm returning a list instead of defaultdict
        result = []
        for filter_option in filter_options:
            items = filter_option.split(':')
            option = items[0].lower()
            operation = items[1]
            value = items[2]
            object = None
            if option == 'diameter':
                object = 'Orbit'
            else:
                object = 'NEO'
            filter_object = Filter(option, object, operation, value)
            result.append(filter_object)
        return result

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results




class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
        result = None
        if query.date_search.type.value == "equals":
            result = self.__get_objects_on_date(query.date_search.values[0])
        else:
            result = self.__get_objects_between_dates(query.date_search.values[0], query.date_search.values[1])

        result = result[:query.number]
        return result

    def __get_objects_on_date(self, date):
        result = set()
        for key in self.db.orbit_date_to_neos.keys():
            if key == date:
                neos = self.db.orbit_date_to_neos[key]
                result.update(neos)
        return list(result)

    def __get_objects_between_dates(self, start_date_str, end_date_str):
        result = []
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        for key in self.db.orbit_date_to_neos.keys():
            date = datetime.strptime(key, "%Y-%m-%d")
            if start_date <= date <= end_date:
                neos = self.db.orbit_date_to_neos[key]
                result.extend(neos)
        return result
