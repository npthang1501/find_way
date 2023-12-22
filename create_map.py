import folium
from dijkstra import find_way
from Utils.utils import read_data, str2point, distance, make_vector, angle_between, S
import requests
import string
from Global.constants import direct_angle

def directions(way):
    direct = ''
    dis = 0
    for i in range(len(way)):
        if i > 0:
            dis += distance(way[i-1],way[i])
            if i != len(way)-1:
                angle = angle_between(make_vector(way[i],way[i-1]),make_vector(way[i],way[i+1]))
                if angle > direct_angle[0] and angle < direct_angle[1]:
                    if S(way[i-1],way[i],way[i+1]) >= 0:
                        direct += "Đi thẳng " + str(round(dis)) + "m rồi rẽ phải\n"
                    else:
                        direct += "Đi thẳng " + str(round(dis)) + "m rồi rẽ trái\n"
                    dis = 0
    direct += "Đi thẳng " + str(round(dis)) + "m"
    return direct

# take lat, long from address
def find_location(address):
    url = "https://nominatim.openstreetmap.org/?addressdetails=1&q=" +address +"&format=json&limit=1"

    response = requests.get(url).json()
    return [response[0]["lat"],response[0]["lon"]]

# change text to lat, long
def change_to_latlong(s=''):
    s = s.replace('Latitude: ','')
    s = s.replace('Longitude: ','')
    check = False
    for c in (string.ascii_lowercase+string.ascii_uppercase):
        if c in s:
            check = True
    if s != '':
        if check == True:
            s = find_location(s)
        else:
            s = str2point(s)
    return s

# create map from data
def create_map(s = '',t = ''):
    s = change_to_latlong(s)
    t = change_to_latlong(t)

    map = folium.Map(location=[21.034878, 105.810350],zoom_start=16)
    map.add_child(folium.LatLngPopup())
    dis = 0
    direct_way = ''
    coords = read_data("./Dataset/data_node_2.txt")

    # for i in range(len(coords)):
    #     node = coords[i]
    #     folium.Marker(node,popup=str(i)+": "+str(node[0])+ " " +str(node[1])).add_to(map)

    # E = read_data("./Dataset/data_distance_2.txt")

    # for u in E:
    #     my_PolyLine=folium.PolyLine(locations=[coords[u[0]],coords[u[1]]],popup=str(u[0])+ " " +str(u[1]),weight=6)
    #     map.add_child(my_PolyLine)

    if s != '':
        folium.Marker(s).add_to(map)
    if t != '':
        folium.Marker(t).add_to(map)

    if s != '' and t != '':
        list_way,dis = find_way(s,t)
        my_PolyLine=folium.PolyLine(locations=list_way,weight=4)
        map.add_child(my_PolyLine)
        direct_way = directions(list_way)

    return map,dis,direct_way
    # map.save('line_example_newer.html')
    # webbrowser.open("line_example_newer.html")
