from datetime import datetime
from pytz import timezone
from stations import *
from enum import Enum

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

def findRoute(origin, dest):
    return findRouteHelper(origin, dest, [])

def findRouteHelper(origin, dest, route):
    origin_lines = findLinesWithStation(origin)
    dest_lines = findLinesWithStation(dest)
    intersects = origin_lines.intersection(dest_lines)
    if len(intersects) >= 1:
        route.append({
            "lines": intersects,
            "direction": findDirection(origin, dest, min(intersects)),
            "destination": dest
        })
        return route
    elif len(intersects) == 0:
        dest_line_name = min(dest_lines).name
        transfer = min(origin_lines).transfers[dest_line_name]
        route.append({
            "lines": origin_lines,
            "direction": findDirection(origin, transfer, min(origin_lines)),
            "destination": transfer
        })
        return findRouteHelper(transfer, dest, route)

def findLinesWithStation(station):
    lines = set()
    now_utc = datetime.now(timezone('UTC'))
    now_eastern = now_utc.astimezone(timezone('US/Eastern'))
    if now_eastern.hour <= 5 and now_eastern.hour >= 1 and now_eastern.minute >= 30:
        return lines
    if station in red.stations:
        if now_eastern.hour >= 21 and now_eastern.hour <= 2:
            lines.add(red_night)
        else:
            lines.add(red)
    if station in gold.stations:
        lines.add(gold)
    if station in green.stations:
        if now_eastern.hour >= 21 and now_eastern.hour <= 2:
            lines.add(green_night)
        else:
            lines.add(green)
    if station in blue.stations:
        lines.add(blue)
    return lines

def findDirection(origin, dest, line):
    if line.name is 'red' or line.name is 'gold':
        if line.stations.index(origin) < line.stations.index(dest):
            return Direction.SOUTH
        else:
            return Direction.NORTH
    else:
        if line.stations.index(origin) < line.stations.index(dest):
            return Direction.EAST
        else:
            return Direction.WEST
