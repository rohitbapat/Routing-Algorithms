# Implementation of search algorithms
My team and I implemented 5 search algorithms. These were:
a) Breadth First Search
b) Depth First Search
c) Best First Search
d) Iterative Deepening Search
e) A-Star search
The data consisted of 2 files mainly:
a) road-segments.txt
b) city-gps.txt

# Input Files
road-segments.txt file contains the route informations in terms of 5 attributes. These 5 attributes are:
a) Source city(with state initials)
b) Destination city(with state initials)
c) Distance
d) Speed limit
e) Highway Name

city-gps.txt contains the following attributes:
a) City name
b) Latitude
c) Longitude

# Optimization Parameters
The goal is to find most optimal path based on certain input parameters. The optimization can be in 3 ways:
a) Segments: Finding a route between source and destination with least number of stops thats is least number of middle cities.
b) Distance: Finding a route between source and destination with least distance.
c) Time:     Finding a route between source and destination which requires least time. This finds a route with least time required with                  distance and speed taken into consideration.

# Input Arguments
a) Source city
b) Destination city
c) Algorithm to use
d) Optimization to use

# Data Structure used
We explored mediums like simple lists, adjacency matrix networkx package.
We decided upon implmenting dictionary of dictionaries as form of representation.
The first key had the source point and the nested dictionary had destination points as keys.
Speedlimits,distances and highway names were the values of nested dictionaries.

# Fringe Structure
We implemented a fringe with contents listed as below:
a) current_city
b) cost required to get to this point in terms of distance,segments,time(g(s))
c) list of cities travelled so far from source to current_city
d) cost returned by the heuristic function(segments,distance,time) i.e h(s)(optional)

# Heuristics used for different optimization parameters
Distance Heuristic:  The minimum distance can be calculated from the GPS coordinates of the cities under consideration. 
Time Heuristic: For each of successor cities, average speed is calculated. Let City A be the successor city, then all speeds from and to this city are considered and averaged. The distance from distance heuristic is calculated and divided by this average speed for every successor. (Time = Distance/Speed)
Segment Heuristic: A city with many surrounding cities would take many segments to reach the destination. Therefore, in this heuristic we calculated the number of cities in a small radius of this successor city to city with lesser segments.

# Goal State
The goal state included the optimality of the algorithm, the start city and the end city including the path.
We also printed a list of directions and the distance to be travelled before a change.

