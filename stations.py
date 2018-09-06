class Line:
    """A MARTA line of stations"""

    def __init__(self, name, stations, transfers=[], night=False):
        self.name = name
        self.stations = stations
        self.transfers = transfers
        self.night = night

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash((self.name))

    def __cmp__(self, other):
        if self.name < other.name:
            return -1
        elif self.name == other.name:
            return 0
        else:
            return 1

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

red = Line(
    "red",
    ["North Springs", "Sandy Springs", "Dunwoody", "Medical Center", "Buckhead", "Lindbergh Center", "Arts Center", "Midtown", "North Avenue", "Civic Center", "Peachtree Center", "Five Points", "Garnett", "West End", "Oakland City", "Lakewood/Ft. McPherson", "East Point", "College Park", "Airport"],
    {
        "gold": "Lindbergh Center",
        "green": "Five Points",
        "blue": "Five Points"
    }
)

red_night = Line(
    "red",
    ["North Springs", "Sandy Springs", "Dunwoody", "Medical Center", "Buckhead", "Lindbergh Center"],
    {
        "gold": "Lindbergh Center",
        "green": "Lindbergh Center",
        "blue": "Lindbergh Center"
    },
    night=True
)

gold = Line(
    "gold",
    ["Doraville", "Chamblee", "Brookhaven/Oglethorpe", "Lenox", "Lindbergh Center", "Arts Center", "Midtown", "North Avenue", "Civic Center", "Peachtree Center", "Five Points", "Garnett", "West End", "Oakland City", "Lakewood/Ft. McPherson", "East Point", "College Park", "Airport"],
    {
        "red": "Lindbergh Center",
        "green": "Five Points",
        "blue": "Five Points"
    }
)

blue = Line("blue",
    ["Hamilton E. Holmes", "West Lake", "Ashby", "Vine City", "Dome/GWCC/Philips Arena/CNN Center", "Five Points", "Georgia State", "King Memorial", "Inman Park/Reynoldstown", "Edgewood/Candler Park", "East Lake", "Decatur", "Avondale", "Kensington", "Indian Creek"],
    {
        "red": "Five Points",
        "gold": "Five Points",
        "green": "Ashby"
    }
 )

green = Line("green",
    ["Bankhead", "Ashby", "Vine City", "Dome/GWCC/Philips Arena/CNN Center", "Five Points", "Georgia State", "King Memorial", "Inman Park/Reynoldstown", "Edgewood/Candler Park"],
    {
        "red": "Five Points",
        "gold": "Five Points",
        "blue": "Ashby"
    }
)

green_night = Line("green",
    ["Bankhead", "Ashby", "Vine City"],
    {
        "red": "Vine City",
        "gold": "Vine City",
        "blue": "Vine City"
    },
    night=True
)

def getStationsDict():
    stations_dict = {}
    stations = []
    all_stations = red.stations + gold.stations + green.stations + blue.stations
    for sta in all_stations:
        if sta not in stations:
            stations.append(sta)
    for sta in stations:
        for word in sta.split("/"):
            stations_dict[word.lower()] = sta
    return stations_dict
