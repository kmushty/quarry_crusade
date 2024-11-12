import streamlit as st
import folium
from streamlit_folium import st_folium
from app.database import create_route, get_active_routes
import json
from app.config import MAP_DEFAULT_CENTER, MAP_DEFAULT_ZOOM

def main():
    st.title("Quarry Crusade - Asset Manager")
    
    # Initialize the map using config values
    map = folium.Map(
        location=MAP_DEFAULT_CENTER, 
        zoom_start=MAP_DEFAULT_ZOOM
    )
    
    # Add drawing controls to the map
    draw = folium.plugins.Draw(
        export=True,
        position='topleft',
        draw_options={
            'polyline': True,
            'marker': True,
            'circle': True,
            'polygon': True,
            'rectangle': True,
            'circlemarker': True,
        }
    )
    draw.add_to(map)
    
    # Display map
    output = st_folium(map, width=1800, height=600)
    
    # use the last active drawing key in the st_folium dictionary to get drawn features
    if output['last_active_drawing']:
        drawn_features = output['last_active_drawing']
        st.write("New Route Created:")
        st.json(drawn_features)
        
        # Create route name input
        route_name = st.text_input("Route Name")
        
        if st.button("Save Route") and route_name:
            route_data = {
                "route_name": route_name,
                "geometry": drawn_features,
                "status": "active"
            }
            create_route(route_data)
            st.success(f"Route '{route_name}' saved successfully!")
    
    # Display existing routes
    st.subheader("Existing Routes")
    routes = get_active_routes()
    for route in routes:
        st.write(f"Route: {route['route_name']}")
        st.json(route['geometry'])

if __name__ == "__main__":
    main()