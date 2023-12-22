import streamlit as st
from streamlit_folium import st_folium
from create_map import create_map
from Global.constants import speed, vehicle_list

# Page title
st.set_page_config(page_title='Find path between two location')
st.title('Find path between two location')

def choose_veh():
    vehicle = st.selectbox('Phương tiện', vehicle_list, 0)
    return vehicle

def main():
    with st.sidebar:
        start_point = st.text_input('First location')
        end_point = st.text_input('Second location')
        vehicle = choose_veh()

    map,dis,direc_way = create_map(start_point, end_point)
    st_map = st_folium(map, width=800,height=600)

    # data = ''
    # if st_map['last_clicked'] is not None: 
    #     data = str(st_map['last_clicked']['lat'])+" "+str(st_map['last_clicked']['lng'])
    #     st.write(data)
    #     if st.button("Set to first location"):
    #         start_point = data
    #     if st.button("Set to second location"):
    #         end_point = data

    col1, col2 = st.columns(2)
    with col1:
        st.metric('Khoảng cách', str(round(dis)) + ' m')
    with col2:
        st.metric('Thời gian đi', str(round(dis/speed[vehicle])) + 'P')

    st.write('Đường đi')
    st.text(direc_way)

if __name__ == "__main__":
    main()

#streamlit run streamlit_app.py