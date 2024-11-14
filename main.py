import streamlit as st
import folium
from streamlit_folium import st_folium
from app.database import create_route, get_active_routes
import json
import base64
from pathlib import Path
from app.config import MAP_DEFAULT_CENTER, MAP_DEFAULT_ZOOM


def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    # Set page to wide mode
    st.set_page_config(
        page_title="Quarry Crusade",
        layout="wide",
        initial_sidebar_state="expanded"
    )    
    # Initialize the map using config values
    map = folium.Map(
        location=MAP_DEFAULT_CENTER, 
        zoom_start=MAP_DEFAULT_ZOOM
    )
    
     # Add a static vehicle position (TODO: replace with actual coordinates later)
    vehicle_position = [40.604455, -89.487935]
    vehicle_heading = 0
    # Get base64 string of the image
    img_path = Path("assets/minres_truck.png")
    img_base64 = img_to_base64(img_path)
    
    vehicle_icon = folium.DivIcon(
        html=f"""
            <div style='position: relative;'>
                <img src='data:image/png;base64,{img_base64}' 
                     style='width: 30px; 
                            height: 70px; 
                            position: absolute; 
                            left: -15px;
                            top: -25px;
                            transform: rotate({vehicle_heading}deg);
                            transition: transform 0.3s ease;'>
                </img>
            </div>
        """
    )
    folium.Marker(
        vehicle_position,
        popup='Vehicle 1',
        icon=vehicle_icon,
    ).add_to(map)

    # Add drawing controls to the map
    draw = folium.plugins.Draw(
        export=True,
        position='topleft',
        draw_options={
            'polyline': {
                'shapeOptions': {
                    'color': '#ff3700',
                    'weight': 8
                },
                'allowIntersection': True,
                'showLength': True,
                'metric': True,
                'feet': False,
                'repeatMode': False,
                'guideLayers': []
            },
            'polygon': False,
            'rectangle': False,
            'circle': False,
            'marker': False,
            'circlemarker': False
        },
        edit_options={
            'poly': {
                'allowIntersection': True
            },
            'featureGroup': None
        }
    )
    map.add_child(draw)
    
    # Display map
    output = st_folium(map, width="100%", height=800)
    
    # Check if there's a drawing and it's not None
    if output and 'last_active_drawing' in output and output['last_active_drawing']:
        drawn_features = output['last_active_drawing']
        st.write("New Route Created:")
        st.json(drawn_features)
        
        # Create route name input
        route_name = st.text_input("Route Name")
        
        if st.button("Save Route") and route_name:
            try:
                route_data = {
                    "route_name": route_name,
                    "geometry": drawn_features,
                    "status": "active"
                }
                create_route(route_data)
                st.success(f"Route '{route_name}' saved successfully!")
            except Exception as e:
                st.error(f"Error saving route: {str(e)}")
    
    # Display existing routes
    st.subheader("Existing Routes")
    routes = get_active_routes()
    for route in routes:
        st.write(f"Route: {route['route_name']}")
        st.json(route['geometry'])

if __name__ == "__main__":
    main()