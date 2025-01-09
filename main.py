import streamlit as st
import folium
from streamlit_folium import st_folium
from app.database import create_route, get_active_routes
from app.dds.base import get_qos_settings
from app.dds.base.handler import DdsHandler
from app.dds.subscribers.hxgn_event import HxgnEventSubscriber, HxgnEvent
import json
import base64
from pathlib import Path
from app.config import MAP_DEFAULT_CENTER, MAP_DEFAULT_ZOOM
import numpy as np
from scipy.special import comb


def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def bernstein_poly(i, n, t):
    """
    Bernstein polynomial for Bézier curves
    Implemented from: https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
    """
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_curve(points, num_points=100):
    """
    Generate points along a Bézier curve
    
    Args:
        points: List of control points [(lat1,lon1), (lat2,lon2), ...]
        num_points: Number of points to generate along the curve
    
    Returns:
        List of (lat,lon) points along the curve
    """
    n = len(points) - 1
    t = np.linspace(0, 1, num_points)
    
    curve_points = []
    for t_i in t:
        point = [0.0, 0.0]
        for i in range(n + 1):
            coef = bernstein_poly(i, n, t_i)
            point[0] += coef * points[i][0]  # latitude
            point[1] += coef * points[i][1]  # longitude
        curve_points.append(tuple(point))
    
    return curve_points

def create_route_with_bezier(start_point, end_point, control_point):
    """
    Create a route with a Bézier curve
    
    Args:
        start_point: (lat, lon) of start
        end_point: (lat, lon) of end
        control_point: (lat, lon) of control point for curve shape
    """
    # Create control points for a quadratic Bezier curve
    control_points = [
        start_point,
        control_point,
        end_point
    ]
    
    # Generate curve points
    curve_points = bezier_curve(control_points, num_points=50)
    
    return curve_points

def handle_hxgn_event(event: HxgnEvent) -> None:
    """Callback for handling events"""
    # Receive Event data (print for now, TODO: update UI)
    print("equipment_id:", event['equipment_id'])

def init_dds():
    """Initialize DDS handler and subscribers"""
     # Get absolute path to QOS file
    xml_path = str(Path(__file__).parent.absolute() / "app" / "dds" / "USER_QOS_PROFILES.xml")
    
    # Verify file exists
    if not Path(xml_path).exists():
        raise FileNotFoundError(f"QOS file not found at: {xml_path}")

    handler = DdsHandler(
        xml_path=xml_path,
        config_name="QuarryCrusadeParticipants::HxgnEventParticipant",
    )
    
    try:
        handler.init_connector()
        
        # Initialize subscribers
        hxgn_event_subscriber = HxgnEventSubscriber(
            handler=handler,
            callback=handle_hxgn_event
        )
        hxgn_event_subscriber.start()
        
        return handler, hxgn_event_subscriber
        
    except Exception as e:
        st.error(f"Failed to initialize DDS: {str(e)}")
        raise

def main():
    # Set page to wide mode
    st.set_page_config(
        page_title="Quarry Crusade",
        layout="wide",
        initial_sidebar_state="expanded"
    )    

    if 'dds_handler' not in st.session_state:
        try:
            handler, hxgn_event_subscriber = init_dds()
            # Store in session state to persist across page reruns
            st.session_state.dds_handler = handler
            st.session_state.hxgn_event_subscriber = hxgn_event_subscriber
            
            def cleanup():
                st.session_state.event_subscriber.stop()
                st.session_state.dds_handler.cleanup()
                del st.session_state.event_subscriber
                del st.session_state.dds_handler

            # Register cleanup
            if st.runtime.exists():
                st.runtime.add_cleanup(cleanup)
                
        except Exception:
            st.error("Failed to start DDS communication")
            return
    
    # Initialize the map using config values
    map = folium.Map(
        location=MAP_DEFAULT_CENTER, 
        zoom_start=MAP_DEFAULT_ZOOM,
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite'
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
                # If it's a polyline, create a smooth Bézier curve
                if drawn_features['geometry']['type'] == 'LineString':
                    coordinates = drawn_features['geometry']['coordinates']
                    
                    # Need at least 3 points for a quadratic Bézier curve
                    if len(coordinates) >= 3:
                        smooth_points = []
                        # Create Bézier curves between each set of 3 points
                        for i in range(len(coordinates) - 2):
                            start = coordinates[i]
                            control = coordinates[i + 1]
                            end = coordinates[i + 2]
                            
                            curve_points = create_route_with_bezier(
                                start_point=start,
                                control_point=control,
                                end_point=end
                            )
                            smooth_points.extend(curve_points)
                        
                        # Update the geometry with smoothed points
                        drawn_features['geometry']['coordinates'] = smooth_points
                
                route_data = {
                    "route_name": route_name,
                    "geometry": drawn_features,
                    "status": "active"
                }
                create_route(route_data)
                st.success(f"Route '{route_name}' saved successfully!")
                
                # Add the smoothed curve to the map
                print("updated smooth points:", smooth_points)
                folium.PolyLine(
                    smooth_points,
                    weight=8,
                    color='#ff3700',
                    opacity=0.8
                ).add_to(map)
                
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