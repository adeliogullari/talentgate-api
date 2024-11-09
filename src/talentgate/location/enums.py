from enum import StrEnum
from typing import List, Dict


class GermanyCities(StrEnum):
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


class NetherlandsCities(StrEnum):
    ALKMAAR = "Alkmaar"
    ALMERE = "Almere"
    ALPHEN_AAN_DEN_RIJN = "Alphen aan den Rijn"
    AMERSFOORT = "Amersfoort"
    AMSTELVEEN = "Amstelveen"
    AMSTERDAM = "Amsterdam"
    APELDOORN = "Apeldoorn"
    ARNHEM = "Arnhem"
    ASSEN = "Assen"
    BERGEN_OP_ZOOM = "Bergen op Zoom"
    BREDA = "Breda"
    CAPELLE_AAN_DEN_IJSSEL = "Capelle aan den IJssel"
    DELFT = "Delft"
    S_HERTOGENBOSCH = "s-Hertogenbosch"
    DEVENTER = "Deventer"
    DORDRECHT = "Dordrecht"
    EDE = "Ede"
    EINDHOVEN = "Eindhoven"
    EMMEN = "Emmen"
    ENSCHEDE = "Enschede"
    GELEEN = "Geleen"
    GOUDA = "Gouda"
    GRONINGEN = "Groningen"
    HAARLEM = "Haarlem"
    HAGUE = "The Hague"
    HELMOND = "Helmond"
    HENGELO = "Hengelo"
    HILVERSUM = "Hilversum"
    HOORN = "Hoorn"
    LEEUWARDEN = "Leeuwarden"
    LEIDEN = "Leiden"
    LEIDSCHENDAM = "Leidschendam"
    MAASTRICHT = "Maastricht"
    NIEUWEGEIN = "Nieuwegein"
    NIJMEGEN = "Nijmegen"
    PURMEREND = "Purmerend"
    RIDDERKERK = "Ridderkerk"
    ROTTERDAM = "Rotterdam"
    SCHIEDAM = "Schiedam"
    SITTARD = "Sittard"
    SPAKENBURG = "Spakenburg"
    TILBURG = "Tilburg"
    UTRECHT = "Utrecht"
    VEENENDAAL = "Veenendaal"
    VENLO = "Venlo"
    VLISSINGEN = "Vlissingen"
    VOORBURG = "Voorburg"
    ZAANDAM = "Zaandam"
    ZOETERMEER = "Zoetermeer"
    ZUTPHEN = "Zutphen"
    ZWIJNDRECHT = "Zwijndrecht"


class GermanyStates(StrEnum):
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


class NetherlandsStates(StrEnum):
    DRENTHE = "Drenthe"
    FLEVOLAND = "Flevoland"
    FRIESLAND = "Friesland"
    GELDERLAND = "Gelderland"
    GRONINGEN = "Groningen"
    LIMBURG = "Limburg"
    NORTH_BRABANT = "North Brabant"
    NORTH_HOLLAND = "North Holland"
    OVERIJSSEL = "Overijssel"
    SOUTH_HOLLAND = "South Holland"
    UTRECHT = "Utrecht"
    ZEELAND = "Zeeland"


class Countries(StrEnum):
    GERMANY = "Germany"
    NETHERLANDS = "Netherlands"


Germany: Dict[str, List[str]] = dict()
Netherlands: Dict[str, List[str]] = dict()

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

Netherlands[NetherlandsStates.DRENTHE] = [
    NetherlandsCities.ASSEN,
    NetherlandsCities.EMMEN,
]
Netherlands[NetherlandsStates.FLEVOLAND] = [
    NetherlandsCities.ALMERE,
]
Netherlands[NetherlandsStates.FRIESLAND] = [
    NetherlandsCities.LEEUWARDEN,
]
Netherlands[NetherlandsStates.GELDERLAND] = [
    NetherlandsCities.APELDOORN,
    NetherlandsCities.ARNHEM,
    NetherlandsCities.EDE,
    NetherlandsCities.NIJMEGEN,
]
Netherlands[NetherlandsStates.GRONINGEN] = [
    NetherlandsCities.GRONINGEN,
]
Netherlands[NetherlandsStates.LIMBURG] = [
    NetherlandsCities.GELEEN,
    NetherlandsCities.MAASTRICHT,
    NetherlandsCities.SITTARD,
    NetherlandsCities.VENLO,
]
Netherlands[NetherlandsStates.NORTH_BRABANT] = [
    NetherlandsCities.BERGEN_OP_ZOOM,
    NetherlandsCities.BREDA,
    NetherlandsCities.EINDHOVEN,
    NetherlandsCities.HELMOND,
    NetherlandsCities.S_HERTOGENBOSCH,
    NetherlandsCities.TILBURG,
]
Netherlands[NetherlandsStates.NORTH_HOLLAND] = [
    NetherlandsCities.ALKMAAR,
    NetherlandsCities.AMSTELVEEN,
    NetherlandsCities.AMSTERDAM,
    NetherlandsCities.HAARLEM,
    NetherlandsCities.HILVERSUM,
    NetherlandsCities.HOORN,
    NetherlandsCities.PURMEREND,
    NetherlandsCities.ZAANDAM,
]
Netherlands[NetherlandsStates.OVERIJSSEL] = [
    NetherlandsCities.DEVENTER,
    NetherlandsCities.ENSCHEDE,
    NetherlandsCities.HENGELO,
    NetherlandsCities.ZUTPHEN,
]
Netherlands[NetherlandsStates.SOUTH_HOLLAND] = [
    NetherlandsCities.CAPELLE_AAN_DEN_IJSSEL,
    NetherlandsCities.DELFT,
    NetherlandsCities.DORDRECHT,
    NetherlandsCities.GOUDA,
    NetherlandsCities.HAGUE,
    NetherlandsCities.LEIDEN,
    NetherlandsCities.LEIDSCHENDAM,
    NetherlandsCities.RIDDERKERK,
    NetherlandsCities.ROTTERDAM,
    NetherlandsCities.SCHIEDAM,
    NetherlandsCities.VOORBURG,
    NetherlandsCities.ZOETERMEER,
    NetherlandsCities.ZWIJNDRECHT,
]
Netherlands[NetherlandsStates.UTRECHT] = [
    NetherlandsCities.AMERSFOORT,
    NetherlandsCities.NIEUWEGEIN,
    NetherlandsCities.UTRECHT,
    NetherlandsCities.VEENENDAAL,
]
Netherlands[NetherlandsStates.ZEELAND] = [
    NetherlandsCities.VLISSINGEN,
]

World: Dict[str, Dict[str, List[str]]] = dict()

World[Countries.GERMANY] = Germany
World[Countries.NETHERLANDS] = Netherlands
