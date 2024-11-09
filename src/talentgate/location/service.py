from .enums import World


def retrieve_countries():
    return list(World.keys())


def retrieve_states_by_country(country: str):
    return list(World[country].keys())


def retrieve_cities_by_state(country: str, state: str):
    return World[country][state]

    # return GermanyStates.THURINGIA #Germany.get(country)


#
#     @classmethod
#     def cities(cls):
#         return list(map(str, GermanyCities))
#
#     @classmethod
#     def states(cls):
#         return list(map(str, GermanyStates))
#
#     @classmethod
#     def cities_by_state(cls, state):
#         """Returns the cities associated with a given state."""
#         return cls.state_city_mapping.get(state, [])
