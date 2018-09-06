from routing import findRoute
from stations import getStationsDict
from difflib import get_close_matches

keys = getStationsDict().keys()
print(get_close_matches("east lake", keys, 10))

# print(findRoute("Airport", "Indian Creek"))
