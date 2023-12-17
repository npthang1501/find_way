import folium
from dijkstra import find_way
from Utils.utils import read_data, str2point, distance, make_vector, angle_between, S

def directions(way):
    direct = ''
    dis = 0
    for i in range(len(way)):
        if i > 0:
            dis += distance(way[i-1],way[i])
            if i != len(way)-1:
                angle = angle_between(make_vector(way[i],way[i-1]),make_vector(way[i],way[i+1]))
                if angle > 70 and angle < 120:
                    if S(way[i-1],way[i],way[i+1]) >= 0:
                        direct += "Đi thẳng " + str(round(dis)) + "m rồi rẽ phải\n"
                    else:
                        direct += "Đi thẳng " + str(round(dis)) + "m rồi rẽ trái\n"
                    dis = 0
    direct += "Đi thẳng " + str(round(dis)) + "m"
    return direct


def make_map(s = '',t = ''):
    map = folium.Map(location=[21.034878, 105.810350],zoom_start=16)
    dis = 0
    direct_way = ''
    coords = read_data("./Dataset/data_node.txt")

    # for node in coords:
    #     folium.Marker(node).add_to(map)

    if s != '':
        folium.Marker(str2point(s)).add_to(map)
    if t != '':
        folium.Marker(str2point(t)).add_to(map)

    if s != '' and t != '':
        list_way,dis = find_way(str2point(s),str2point(t))
        my_PolyLine=folium.PolyLine(locations=list_way,weight=4)
        map.add_child(my_PolyLine)
        direct_way = directions(list_way)

    return map,dis,direct_way
    # map.save('line_example_newer.html')
    # webbrowser.open("line_example_newer.html")
