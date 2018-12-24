#!/usr/bin/env python3

# put your routing program here!
'''
(1)
We started with problem of representing this given txt files in terms of simple data structure.
We explored mediums like simple lists, adjacency matrix networkx package.
We decided upon implmenting dictionary of dictionaries as form of representation.
The first key had the source point and the nested dictionary had destination points as keys.
Speedlimits,distances and highway names were the values of nested dictionaries.
(2)
The statespace includes all the cities mentioned in the road-segments.txt file excluding ones with missing data
(3)
We implemented a fringe with contents listed as below:
    a: current_city
    b: cost required to get to this point in terms of distance,segments,time(g(s))
    c: list of cities travelled so far from source to current_city
    d: cost returned by the heuristic function(segments,distance,time) i.e h(s)(optional)

(4)
the edge weights or the values in nested dictionary were a collection of speeds distances and highway names
(5)
The goal state included the optimality of the algorithm, the start city and the end city including the path
We also printed a list of directions and the distance to be travelled before a change
(6)
For the A* search involved in part 2, there are 3 parameters to be optimized: time, distance and segments.
Distance Heuristic:  The minimum distance can be calculated from the GPS coordinates of the cities under consideration. 
Time Heuristic: For each of successor cities, average speed is calculated. Let City A be the successor city, then all speeds from and to this city are considered and averaged. The distance from distance heuristic is calculated and divided by this average speed for every successor. (Time = Distance/Speed)
Segment Heuristic: A city with many surrounding cities would take many segments to reach the destination. Therefore, in this heuristic we calculated the number of cities in a small radius of this successor city to city with lesser segments.
(7)
Based on input we decide upon an algorithm and the cost function to implement. 
The user can change the algorithm and compare between the time,distance and segment constraints
The output is a userfriendly one with list of directions and associated distances.
(8)
We used dictionaries of dictionaries for simplified search of nodes
Assumptions include
The noisy data or incomplete data was avoided.
We treated the incomplete gps coordinates with average coordinate via state it is in.
The radius to consider for points near a city for distance heuristics
A k value to normalize the combined heuristic of distance and segments
(9)
For time heuristics we first took an average of speeds and implemented the solution
We also went for the no of proximal nodes to current city
However we combined these 2 things to offer a better heuristic       
'''

# import statements to include argument vector
# import random to clean noisy data with fillers for latitude and longitude
# import math to calculate sin cosine tan cot etc
import sys
import random
import math

# get start city as input
start_city=str(sys.argv[1])
# get end_city as input
end_city=str(sys.argv[2])
# get algorithm to be used
algorithm=str(sys.argv[3])
# get cost to apply on algorithm
cost=str(sys.argv[4])


# function to check univisited states wrt cost and visited array
def not_visited(city,path_cost):
    # differentiate cost calculation based on algorithm used 
    global visited
    if(algorithm=='astar' or algorithm=='uniform'):
        if (city[0] in visited) and (path_cost>visited[city[0]]):
            return False
        else:
            return True
    else:
        if (city[0] in visited):
            return False
        else:
            return True

# calculate segment cost for segments as cost input
def segment_cost(cost,i,element):
    total_cost=element[1]+1
    return total_cost

# calculate distance between i and popped city with distance as input
def distance_cost(cost,i,element):
    total_cost=element[1]+int(map_dict[element[0]][i]['Distance'])
    return total_cost

# calculate segment cost for time to travel as cost input
def time_cost(cost,i,element):
    edge_distance=int(map_dict[element[0]][i]['Distance'])
    speed_limit=int(map_dict[element[0]][i]['SpeedLimit'])
    if(speed_limit!=0):
        time_taken=(edge_distance/speed_limit)
    else:
        time_taken=(edge_distance/45)
    total_time=element[1]+(time_taken)
    return total_time

# Calls to cost calculation functions   
def cost_function(cost,i,element,algorithm=None):
    if cost=='segments':
        return segment_cost(cost,i,element)
    elif cost=='distance':
        return distance_cost(cost,i,element)
    elif cost=='time':
        return time_cost(cost,i,element)

# function to calculate gps distances between 2 nodes      
def calculate_gps_distance(start,end):
    lat1 = float(gps_dict[start][0])
    lon1 = float(gps_dict[start][1])
    lat2 = float(gps_dict[end][0]) 
    lon2 = float(gps_dict[end][1])
    # [1] citation added to get distance 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    miles = 6371* c*0.6213
    return miles

# get estimate of time required to travel between current city and end city
def time_estimate(i,end_city):
    #Radius avg speed of other cities
    # Calculate speeds and counts to caculate average
    #Distance heuristic
    speeds=0
    count=1
    dest_dict=map_dict.get(i)
    for parameters in dest_dict.values():
        speeds+=int(parameters['SpeedLimit'])
        count+=1
               
    time_taken=round((calculate_gps_distance(i,end_city))/(speeds/count),2)
    # return time taken
    return time_taken

# define a scope of city for count of segments inside a particular area of GPS coordinates    
def city_scope(i):
    latitude=2
    longitude=15.5
    lat=gps_dict[i][0]
    lon=gps_dict[i][1]
    count=0
    #print(gps_dict.values)
    for scope in gps_dict.values():
        if((float(scope[0])<(float(lat)+latitude)) and float(scope[0])>(float(lat)-latitude)):
            if((float(scope[1])<(float(lon)+longitude)) and float(scope[1])>(float(lon)-longitude)):
                count+=1
                #print(count)
    return count

# calls to calculate heuristic function based on cost
def heuristic_function(cost,i,element,end_city):
    k=60 
    #As distance and segments have different magnitude of ranges.
    #This factor normalizes the heuristic to some extent
    # return h(s)+g(s)
    if(cost=='segments'):
        return math.ceil((city_scope(i))*(calculate_gps_distance(i,end_city)/k) + segment_cost(cost,i,element))
    elif(cost=='time'):
        return time_cost(cost,i,element)+time_estimate(i,end_city)
    elif(cost=='distance'):
        return calculate_gps_distance(i,end_city)+distance_cost(cost,i,element)

# whole map is in dictionary of dictionaries. The function finds sucessors                
def city_successors(element):
    list_dest=[] 
    for i in map_dict.get(element[0]).keys():
            total_cost=cost_function(cost,i,element)
            if(algorithm=='astar'):
                heuristic=heuristic_function(cost,i,element,end_city)
            else:
                heuristic=0
            list_dest.append([i,total_cost,element[2]+[i],heuristic])
    return list_dest

# Display results in required format
def display_result(element):
    total_dist=0
    total_time=0
    if(algorithm=='dfs' or algorithm=='bfs'):
        optimal='no'
    else:
        optimal='yes'
    print('Start From :',element[2][0])
    for i in range(0,len(element[2])-1):
        dist=float(map_dict[element[2][i]][element[2][i+1]]['Distance'])
        highway=map_dict[element[2][i]][element[2][i+1]]['Highway']
        if(float((map_dict[element[2][i]][element[2][i+1]]['SpeedLimit']))!=0):
            time=dist/float((map_dict[element[2][i]][element[2][i+1]]['SpeedLimit']))
        else:
            time=float(dist/45)
        print('Travel from ',element[2][i],' to ',element[2][i+1],' on ',highway,' for ',dist,' miles')
        total_dist+=dist
        total_time+=time
    print('Total Travel Time is : ',round(total_time,2))
    print('Total Distance is : ',total_dist)
    print('----------------------------------------------------------------')
    print(optimal,total_dist,round(total_time,2),element[2][0],' '.join(element[2][1:-2]),element[2][-1])   

# function to solve the problem by iterative deepening
def solve_IDS(init_city,end_city,cost):
    k=2
    # define initial depth k and iteratively increase
    while(k>0):
        global visited
        visited.clear
        path_list=[]
        path_list.append(init_city)
        fringe=[[init_city,0,path_list,0]]
        while(len(fringe)>0):
            element=fringe.pop()
            next_city=element[0]
            if(next_city==end_city):
                display_result(element)
                return
            if(len(element[2])<k):
                for city in city_successors(element):
                    path_cost=cost_function(cost,city[0],element)
                    if not_visited(city,path_cost):
                        fringe.append(city)
                        visited.update({city[0]:path_cost})
            k+=1    

# function to solve the problem by dfs
def solve_dfs(init_city,end_city,cost):
    path_list=[]
    path_list.append(init_city)
    fringe=[[init_city,0,path_list,0]]
    while(len(fringe)>0):
        #pop last element from fringe
        element=fringe.pop()
        next_city=element[0]
        if(next_city==end_city):
            display_result(element)
            return
        for city in city_successors(element):
            path_cost=cost_function(cost,city[0],element)
            if not_visited(city,path_cost):
                fringe.append(city)
                global visited
                visited.update({city[0]:path_cost})
        

# function to solve problem by bfs
def solve_bfs(init_city,end_city,cost):
    #print("End city: "+ str(end_city))
    path_list=[]
    path_list.append(init_city)
    fringe=[[init_city,0,path_list,0]]
    while(len(fringe)>0):
        # pop the first element in fringe
        element=fringe.pop(0)
        next_city=element[0]
        if(next_city==end_city):
            display_result(element)
            return
        
        for city in city_successors(element):
            path_cost=cost_function(cost,city[0],element)
            if not_visited(city,path_cost):
                fringe.append(city)
                global visited
                visited.update({city[0]:path_cost})
                
# function to calculate uniform function   
def solve_uniform(init_city,end_city,cost):
    path_list=[]
    path_list.append(init_city)
    #fringe=Q.PriorityQueue
    fringe=[[init_city,0,path_list,0]]
    while(len(fringe)>0):
        #print(fringe)
        #max(fringe,key=lambda x: x[1])
        #print(ind)
        i=fringe.index(min(fringe,key=lambda x: x[1]))
        #print(element)
        element=fringe.pop(i)
        next_city=element[0]
        
        if(next_city==end_city):
            display_result(element)
            return
        
        for city in city_successors(element):
            path_cost=cost_function(cost,city[0],element)
            if not_visited(city,path_cost):
                fringe.append(city)
                global visited
                visited.update({city[0]:path_cost})

# function to calculate astar approach                              
def solve_astar(init_city,end_city,cost,algorithm):
    path_list=[]
    path_list.append(init_city)
    fringe=[[init_city,0,path_list,0]]
    while(len(fringe)>0):
        # pop the least element from fringe based on last calculated cost element
        i=fringe.index(min(fringe,key=lambda x: x[3]))
        element=fringe.pop(i)
        next_city=element[0]
        # calculate if state is goal state
        if(next_city==end_city):
            display_result(element)
            return
        # calculate successors
        for city in city_successors(element):
            path_cost=cost_function(cost,city[0],element,algorithm)
            if not_visited(city,path_cost):
                fringe.append(city)
                global visited
                visited.update({city[0]:path_cost})
                              

# initialize route,line array to append routes visited dictionary to keep record 
visited={}
route=[]
lines=[]

# read file road-segments.txt
with open('road-segments.txt') as csv_file:
    for line in csv_file:
        lines.append(line.split())

#create a map dictionary to store source
map_dict={}

# parse each line and check for empty values
# assumptions
# if speedlimit=0 take it as 45
# leave out empty or incomplete rows
for line in lines:
    if(len(line)==5):
        source_pt=line[0]
        dest_pt=line[1]
        distance_pt=line[2]
        if(line[3]==0):
            speedlimit_pt=45
        else:
            speedlimit_pt=line[3]
        highway_pt=line[4]
        dest_dict={}
        if(source_pt not in map_dict.keys()):
            dest_dict={dest_pt:{'Distance':distance_pt,'SpeedLimit':speedlimit_pt,'Highway':highway_pt}}
            map_dict[source_pt]=dest_dict
        else:
            map_dict[source_pt][dest_pt]={'Distance':distance_pt,'SpeedLimit':speedlimit_pt,'Highway':highway_pt}
        if(dest_pt not in map_dict.keys()):
            dest_dict={source_pt:{'Distance':distance_pt,'SpeedLimit':speedlimit_pt,'Highway':highway_pt}}
            map_dict[dest_pt]=dest_dict
        else:
            map_dict[dest_pt][source_pt]={'Distance':distance_pt,'SpeedLimit':speedlimit_pt,'Highway':highway_pt}

# open and read gps file
with open('city-gps.txt') as csv_file:
    for line in csv_file:
        lines.append(line.split())

#initialise dictionary for place and gps coordinates       
gps_dict={}
for line in lines:
    if(len(line)==3):
        city=line[0]
        gps1=line[1]
        gps2=line[2]
        gps_dict[line[0]]=[line[1],line[2]]

# compare map nodes and gps nodes for missing elements
map_keys=list(map_dict.keys())
gps_keys=list(gps_dict.keys())
state_list=[]

# Assumptions
# for missing gps nodes we check for states of the these nodes
# we check for latitudes and longitudes of same state nodes in map dictionary
# we randomly generate gps coordinates in the specified range for that missing node
for i in gps_keys:
    state_list.append(i.split(",_",1)[1])

average_gps={}   
for i in set(state_list):
    by_state=[value for key, value in gps_dict.items() if ('_'+i) in key]
    sum_lat=0
    sum_long=0
    for coordinate in by_state:
        sum_lat+=float(coordinate[0])
        sum_long+=float(coordinate[1])
    average_lat=sum_lat/len(by_state)
    average_long=sum_long/len(by_state)
    average_gps[i]=[average_lat,average_long]

gps_miss=list(set(map_keys).difference(gps_keys))

for i in gps_miss:
    if i.split(",_",1)[1] in average_gps:      
        gps_dict[i]=average_gps[i.split(",_",1)[1]]
    else:
        gps_dict[i]=[round(random.uniform(30,40),3),round(random.uniform(-70,-105),3)]
    


# calls to function to calculate the distance,cost,segments and print a routing table accordingly
if(algorithm=='bfs'):
    solve_bfs(start_city,end_city,cost)
elif(algorithm=='dfs'):
    solve_dfs(start_city,end_city,cost)
elif(algorithm=='uniform'):
    solve_uniform(start_city,end_city,cost)
elif(algorithm=='ids'):
    solve_IDS(start_city,end_city,cost)
elif(algorithm=='astar'):
    solve_astar(start_city,end_city,cost,algorithm)

    
'''
[1] :   https://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
        Code to calculate gps distance between 2 coordinates
[2]            
'''

#print(lines)


#print(map_dict)

#        if(line.split()[2]):
#            distance_pt=line.split()[2]
#        else:
#            distance_pt="NA"
#        if(line.split()[3]):
#            speedlimit_pt=line.split()[3]
#        else:
#            speedlimit_pt="NA"
#        if(line.split()[4]):
#            highway_pt=line.split()[4]
#        else:
#            highway_pt="NA"
#    dest_dict={}
#    if(source_pt not in map_dict.keys()):
#        dest_dict={dest_pt:{'Distance':distance_pt,'SpeedLimit':speedlimit_pt,'Highway':highway_pt}}
#        map_dict={source_pt:dest_dict}
#        print(map_dict)
#    else:
#        map_dict[source_pt][dest_pt]={'Distance':distance_pt,'SpeedLimit':speedlimit_pt,'Highway':highway_pt}
#        print(map_dict)      