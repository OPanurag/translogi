# Route Optimization and Delivery Prediction System

This project helps in optimizing delivery routes, predicting travel times, and finding the best routes between multiple cities using real-time data from Google Maps and OpenWeatherMap.

## Features

- Optimizes the delivery route between multiple cities
- Fetches geographical coordinates using OpenWeatherMap API
- Calculates travel times and distances using Google Maps API
- Provides an optimized delivery route with total time and distance
- Displays the route visually on Google Maps

## Requirements

This project requires the following Python packages:

- `streamlit` - For building the front-end user interface
- `googlemaps` - For interacting with Google Maps API
- `geopy` - For calculating geographic distances
- `requests` - For making HTTP requests to APIs
- `scikit-learn` - For machine learning model (if applicable)
- `pickle` - For saving and loading the trained model

## Clone the Repository

1. Open your terminal (or command prompt).
2. Clone this repository using the following command:
    Bash
   ```
   git clone https://github.com/your-username/route-optimization.git
   ```
Navigate to the project directory:

bash
Copy
Edit
cd route-optimization
Set Up the Environment
To set up the required environment and dependencies, follow these steps:

Create a Virtual Environment:
bash
```
python -m venv venv
```

Activate the Virtual Environment:

On macOS/Linux:
bash
```
source venv/bin/activate
```

Install Required Dependencies:

bash
```
pip install -r requirements.txt
```

If requirements.txt is not available, you can manually install the necessary packages with:
bash
```
pip install streamlit googlemaps geopy requests scikit-learn pickle
```

Set Up API Keys
Google Maps API Key:

Sign up for the Google Maps API and obtain an API key.

Replace the placeholder key in src/app.py with your Google Maps API key:

```
gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')
```

OpenWeatherMap API Key:
Sign up for an OpenWeatherMap account and obtain an API key.
Replace the placeholder key in src/app.py with your OpenWeatherMap API key:
```
api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
```

Train the Model (Optional)
If you want to train the model on your own data:

Prepare a CSV file (amazon_delivery.csv) containing columns like:

Store_Latitude, Store_Longitude, Drop_Latitude, Drop_Longitude, Delivery_Time
The machine learning model will be trained to predict the delivery time based on these features.

Run the following script to train the model and save it using pickle:

bash
```
python model.py
```
This will create a delivery_model.pkl file that contains the trained model.

Run the Application
Start the Streamlit app by running the following command:

bash
```
streamlit run src/app.py
```
The application will open in your default browser, where you can:

Enter the origin city.
Enter drop points (separate multiple cities with commas).
Click the "Optimize Route" button to get the best route, including the travel time and distance.
The optimized route will be displayed, along with the total travel time and distance.

Usage
Once the application is running, the user will be prompted to:

Enter an origin city.
Enter drop points (separate multiple cities with commas).
View the optimized delivery route, including:
The best order of delivery points.
The travel time and distance for each leg of the journey.
The total travel time and distance for the entire route.
Example:

Origin City: Chicago
Drop Points: New York, Los Angeles, San Francisco
Output: Optimized route and total time/distance.
Contributing
Feel free to fork this repository, create a pull request, or open an issue if you find any bugs or would like to suggest new features.
