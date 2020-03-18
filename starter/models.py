class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.is_hazardous = kwargs.get('is_potentially_hazardous_asteroid')
        self.diameter = kwargs.get('estimated_diameter_max_kilometers')
        self.orbits = []

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?
        self.orbits.append(orbit)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.id == other.id

    def __repr__(self):
        result = f'ID: {self.id}\nName: {self.name}\nOrbits:\n'
        for orbit in self.orbits:
            result += f'- {orbit.name}\n'
            result += f'  - {orbit.miss_distance_kilometers}\n'
            result += f'  - {orbit.close_approach_date}\n'
        return result


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.close_approach_date = kwargs.get("close_approach_date")
        self.name = 'Around ' + kwargs.get('orbiting_body')
        self.miss_distance_kilometers = kwargs.get('miss_distance_kilometers') + ' km'
