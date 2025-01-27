import streamlit as st
import googlemaps
import folium
from geopy.distance import geodesic
import requests

# Set up Google Maps API client
gmaps = googlemaps.Client(key='')  # Replace with your Google Maps API key

# Function to get latitude and longitude from OpenWeatherMap API
def get_lat_long(city_name):
    api_key = ''  # Replace with your OpenWeatherMap API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            lat = data['coord']['lat']
            lon = data['coord']['lon']
            return lat, lon
        else:
            print(f"Error fetching data for {city_name}: {data.get('message')}")
            return None, None
    except Exception as e:
        print(f"Error fetching data for {city_name}: {str(e)}")
        return None, None

# Function to get the driving time and distance between origin and destination
def get_driving_time_and_distance(origin, destination):
    try:
        directions_result = gmaps.directions(origin, destination, mode="driving")
        if directions_result:
            travel_time = directions_result[0]['legs'][0]['duration']['text']
            distance = directions_result[0]['legs'][0]['distance']['text']
            return travel_time, distance
        else:
            return "No route found", "N/A"
    except Exception as e:
        return f"Error: {str(e)}", "N/A"

# Function to calculate the distance between two cities using geopy
def calculate_distance(city1, city2):
    lat1, lon1 = get_lat_long(city1)
    lat2, lon2 = get_lat_long(city2)
    if lat1 and lon1 and lat2 and lon2:
        return geodesic((lat1, lon1), (lat2, lon2)).km
    return float('inf')  # If coordinates are not found, return a very large number

# Function to convert time to minutes
def convert_time_to_minutes(time):
    time_parts = time.split()
    total_minutes = 0

    if 'hour' in time_parts:
        hours = int(time_parts[0])
        total_minutes += hours * 60

    if 'min' in time_parts:
        minutes = int(time_parts[-2])
        total_minutes += minutes

    return total_minutes

# Function to optimize the route using a Greedy approach
def optimize_route(drop_points):
    # Initialize the route with the origin city
    visited = [drop_points[0]]
    remaining = drop_points[1:]
    total_time = 0
    total_distance = 0
    route_summary = f"Optimized Route: {drop_points[0]}"

    while remaining:
        # Find the nearest city to the current city
        last_visited = visited[-1]
        nearest_city = min(remaining, key=lambda city: calculate_distance(last_visited, city))
        distance, time = get_driving_time_and_distance(last_visited, nearest_city)

        # Add to the total time and distance
        travel_time = convert_time_to_minutes(time)  # Convert time to minutes
        total_time += travel_time
        total_distance += float(distance.split()[0].replace(',', '').replace('km', '').replace('mi', ''))

        # Update the route summary
        route_summary += f" -> {nearest_city} - Distance: {distance}, Travel Time: {time}"

        # Move the nearest city from remaining to visited
        visited.append(nearest_city)
        remaining.remove(nearest_city)

    route_summary += f"\nTotal Distance: {total_distance} km\nTotal Time: {total_time} minutes"
    
    # Generate map with route
    route_coordinates = []
    for city in visited:
        lat, lon = get_lat_long(city)
        if lat and lon:
            route_coordinates.append([lat, lon])

    # Plot the route on the map using folium
    if route_coordinates:
        map_center = route_coordinates[0]
        delivery_map = folium.Map(location=map_center, zoom_start=6)

        # Plot markers for the origin and each drop point
        for city in visited:
            lat, lon = get_lat_long(city)
            if lat and lon:
                folium.Marker([lat, lon], popup=city).add_to(delivery_map)

        # Plot the route line
        folium.PolyLine(route_coordinates, color='blue', weight=5, opacity=0.7).add_to(delivery_map)

        # Display map in Streamlit
        map_html = delivery_map._repr_html_()
        st.components.v1.html(map_html, height=500)

    return route_summary

# Streamlit user input section
st.title("Route Optimization for Delivery")

origin_city = st.text_input("Enter the Origin City:")
drop_points_input = st.text_input("Enter the Drop Points (separate cities with commas):")
drop_points = [origin_city] + [city.strip() for city in drop_points_input.split(",")]

if st.button("Optimize Route"):
    if origin_city and drop_points_input:
        # Get optimized route and travel time details
        optimized_route = optimize_route(drop_points)

        # Display the optimized route details
        st.write(optimized_route)
    else:
        st.write("Please enter both origin city and drop points.")
