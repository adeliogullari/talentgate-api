from enum import Enum


class GermanyStates(Enum):
    BADEN_WUERTTEMBERG = "Baden-Württemberg"
    BAVARIA = "Bavaria"
    BERLIN = "Berlin"
    BRANDENBURG = "Brandenburg"
    BREMEN = "Bremen"
    HAMBURG = "Hamburg"
    HESSEN = "Hessen"
    MECKLENBURG_VORPOMMERN = "Mecklenburg-Vorpommern"
    LOWER_SAXONY = "Lower Saxony"
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
    BIELEFELD = "Bielefeld"
    BERLIN = "Berlin"
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
    HALLE = "Halle"
    HAMBURG = "Hamburg"
    HANNOVER = "Hannover"
    HEIDELBERG = "Heidelberg"
    HILDESHEIM = "Hildesheim"
    KASSEL = "Kassel"
    KARLSRUHE = "Karlsruhe"
    KIEL = "Kiel"
    KREFELD = "Krefeld"
    LEIPZIG = "Leipzig"
    LEVERKUSEN = "Leverkusen"
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
    PADERBORN = "Paderborn"
    POTSDAM = "Potsdam"
    REGENSBURG = "Regensburg"
    REUTLINGEN = "Reutlingen"
    ROSTOCK = "Rostock"
    SAARBRUCKEN = "Saarbrücken"
    SCHWERIN = "Schwerin"
    STUTTGART = "Stuttgart"
    ULM = "Ulm"
    WOLFSBURG = "Wolfsburg"
    WIESBADEN = "Wiesbaden"
    WUPPERTAL = "Wuppertal"


class Germany:
    country = {
        GermanyStates.BADEN_WUERTTEMBERG: [
            GermanyCities.STUTTGART,
            GermanyCities.FREIBURG,
            GermanyCities.HEIDELBERG,
            GermanyCities.KARLSRUHE,
            GermanyCities.MANNHEIM,
            GermanyCities.REUTLINGEN,
            GermanyCities.ULM,
        ],
        GermanyStates.BAVARIA: [
            GermanyCities.MUNICH,
            GermanyCities.AUGSBURG,
            GermanyCities.NUREMBERG,
            GermanyCities.REGENSBURG,
        ],
        GermanyStates.BERLIN: [GermanyCities.BERLIN],
        GermanyStates.BRANDENBURG: [GermanyCities.POTSDAM],
        GermanyStates.BREMEN: [GermanyCities.BREMEN, GermanyCities.BREMERHAVEN],
        GermanyStates.HAMBURG: [GermanyCities.HAMBURG],
        GermanyStates.HESSEN: [
            GermanyCities.FRANKFURT,
            GermanyCities.DARMSTADT,
            GermanyCities.KASSEL,
            GermanyCities.WIESBADEN,
            GermanyCities.OFFENBACH,
        ],
        GermanyStates.LOWER_SAXONY: [
            GermanyCities.HANNOVER,
            GermanyCities.BRAUNSCHWEIG,
            GermanyCities.OSNABRUCK,
            GermanyCities.OLDENBURG,
            GermanyCities.WOLFSBURG,
        ],
        GermanyStates.MECKLENBURG_VORPOMMERN: [
            GermanyCities.ROSTOCK,
            GermanyCities.SCHWERIN,
        ],
        GermanyStates.NORTH_RHINE_WESTPHALIA: [
            GermanyCities.COLOGNE,
            GermanyCities.DUSSELDORF,
            GermanyCities.DORTMUND,
            GermanyCities.ESSEN,
            GermanyCities.BONN,
            GermanyCities.AACHEN,
            GermanyCities.BIELEFELD,
            GermanyCities.MUNSTER,
            GermanyCities.GELSENKIRCHEN,
            GermanyCities.KREFELD,
        ],
        GermanyStates.RHINELAND_PALATINATE: [
            GermanyCities.MAINZ,
            GermanyCities.LUDWIGSHAFEN,
        ],
        GermanyStates.SAARLAND: [GermanyCities.SAARBRUCKEN],
        GermanyStates.SAXONY: [
            GermanyCities.LEIPZIG,
            GermanyCities.DRESDEN,
            GermanyCities.CHEMNITZ,
        ],
        GermanyStates.SAXONY_ANHALT: [GermanyCities.MAGDEBURG, GermanyCities.HALLE],
        GermanyStates.SCHLESWIG_HOLSTEIN: [GermanyCities.KIEL, GermanyCities.LUEBECK],
        GermanyStates.THURINGIA: [GermanyCities.ERFURT, GermanyCities.GOTHA],
    }

    @classmethod
    def cities(cls) -> list:
        return list(set.union(*cls.country.values()))

    @classmethod
    def states(cls):
        return list(cls.country.keys())

    @classmethod
    def municipalities(cls, state: str):
        return cls.country.get(state, [])


class Countries(Enum):
    GERMANY = Germany
