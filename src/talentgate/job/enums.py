from enum import Enum
from typing import Dict, List


class GermanyStates(Enum):
    BADEN_WUERTTEMBERG = "Baden-Württemberg"
    BAVARIA = "Bavaria"
    BERLIN = "Berlin"
    BRANDENBURG = "Brandenburg"
    BREMEN = "Bremen"
    HAMBURG = "Hamburg"
    HESSEN = "Hessen"
    LOWER_SAXONY = "Lower Saxony"
    MECKLENBURG_VORPOMMERN = "Mecklenburg-Vorpommern"
    NORTH_RHINE_WESTPHALIA = "North Rhine-Westphalia"
    RHINELAND_PALATINATE = "Rhineland-Palatinate"
    SAARLAND = "Saarland"
    SAXONY = "Saxony"
    SAXONY_ANHALT = "Saxony-Anhalt"
    SCHLESWIG_HOLSTEIN = "Schleswig-Holstein"
    THURINGIA = "Thuringia"


class GermanyCities(Enum):
    AACHEN = "Aachen"
    AUGSBURG = "Augsburg"
    BERLIN = "Berlin"
    BIELEFELD = "Bielefeld"
    BONN = "Bonn"
    BRAUNSCHWEIG = "Braunschweig"
    BREMEN = "Bremen"
    BREMERHAVEN = "Bremerhaven"
    CHEMNITZ = "Chemnitz"
    COLOGNE = "Cologne"
    DARMSTADT = "Darmstadt"
    DORTMUND = "Dortmund"
    DRESDEN = "Dresden"
    DUSSELDORF = "Düsseldorf"
    ERFURT = "Erfurt"
    ESSEN = "Essen"
    FREIBURG = "Freiburg"
    FRANKFURT = "Frankfurt"
    GELSENKIRCHEN = "Gelsenkirchen"
    GOTHA = "Gotha"
    HAMBURG = "Hamburg"
    HALLE = "Halle"
    HANNOVER = "Hannover"
    HEIDELBERG = "Heidelberg"
    KARLSRUHE = "Karlsruhe"
    KASSEL = "Kassel"
    KIEL = "Kiel"
    KREFELD = "Krefeld"
    LEIPZIG = "Leipzig"
    LUDWIGSHAFEN = "Ludwigshafen"
    LUEBECK = "Lübeck"
    MAGDEBURG = "Magdeburg"
    MAINZ = "Mainz"
    MANNHEIM = "Mannheim"
    MUNICH = "Munich"
    MUNSTER = "Münster"
    NUREMBERG = "Nuremberg"
    OFFENBACH = "Offenbach"
    OLDENBURG = "Oldenburg"
    OSNABRUCK = "Osnabrück"
    POTSDAM = "Potsdam"
    REGENSBURG = "Regensburg"
    REUTLINGEN = "Reutlingen"
    ROSTOCK = "Rostock"
    SAARBRUCKEN = "Saarbrücken"
    SCHWERIN = "Schwerin"
    STUTTGART = "Stuttgart"
    ULM = "Ulm"
    WIESBADEN = "Wiesbaden"
    WOLFSBURG = "Wolfsburg"


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

Germany: Dict[GermanyStates, List[GermanyCities]] = dict()

Germany[GermanyStates.BADEN_WUERTTEMBERG] = [
    GermanyCities.FREIBURG,
    GermanyCities.HEIDELBERG,
    GermanyCities.KARLSRUHE,
    GermanyCities.MANNHEIM,
    GermanyCities.REUTLINGEN,
    GermanyCities.STUTTGART,
    GermanyCities.ULM,
]
Germany[GermanyStates.BAVARIA] = [
    GermanyCities.AUGSBURG,
    GermanyCities.MUNICH,
    GermanyCities.NUREMBERG,
    GermanyCities.REGENSBURG,
]
Germany[GermanyStates.BERLIN] = [GermanyCities.BERLIN]
Germany[GermanyStates.BRANDENBURG] = [GermanyCities.POTSDAM]
Germany[GermanyStates.BREMEN] = [GermanyCities.BREMEN, GermanyCities.BREMERHAVEN]
Germany[GermanyStates.HAMBURG] = [GermanyCities.HAMBURG]
Germany[GermanyStates.HESSEN] = [
    GermanyCities.DARMSTADT,
    GermanyCities.FRANKFURT,
    GermanyCities.KASSEL,
    GermanyCities.OFFENBACH,
    GermanyCities.WIESBADEN,
]
Germany[GermanyStates.LOWER_SAXONY] = [
    GermanyCities.BRAUNSCHWEIG,
    GermanyCities.HANNOVER,
    GermanyCities.OLDENBURG,
    GermanyCities.OSNABRUCK,
    GermanyCities.WOLFSBURG,
]
Germany[GermanyStates.MECKLENBURG_VORPOMMERN] = [
    GermanyCities.ROSTOCK,
    GermanyCities.SCHWERIN,
]
Germany[GermanyStates.NORTH_RHINE_WESTPHALIA] = [
    GermanyCities.AACHEN,
    GermanyCities.BIELEFELD,
    GermanyCities.BONN,
    GermanyCities.COLOGNE,
    GermanyCities.DORTMUND,
    GermanyCities.DUSSELDORF,
    GermanyCities.ESSEN,
    GermanyCities.GELSENKIRCHEN,
    GermanyCities.KREFELD,
    GermanyCities.MUNSTER,
]
Germany[GermanyStates.RHINELAND_PALATINATE] = [
    GermanyCities.LUDWIGSHAFEN,
    GermanyCities.MAINZ,
]
Germany[GermanyStates.SAARLAND] = [GermanyCities.SAARBRUCKEN]
Germany[GermanyStates.SAXONY] = [
    GermanyCities.CHEMNITZ,
    GermanyCities.DRESDEN,
    GermanyCities.LEIPZIG,
]
Germany[GermanyStates.SAXONY_ANHALT] = [
    GermanyCities.HALLE,
    GermanyCities.MAGDEBURG,
]
Germany[GermanyStates.SCHLESWIG_HOLSTEIN] = [GermanyCities.KIEL, GermanyCities.LUEBECK]
Germany[GermanyStates.THURINGIA] = [GermanyCities.ERFURT, GermanyCities.GOTHA]
