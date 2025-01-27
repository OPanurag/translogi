import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def train_model():
    """
    Train a RandomForestRegressor model to predict delivery times based on store and drop location.
    """
    # Load data and select relevant columns for training
    df = pd.read_csv('data/amazon_delivery.csv')
    selected_columns = df[['Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude', 'Delivery_Time']]

    # Drop rows with missing values
    selected_columns = selected_columns.dropna()

    # Split features (X) and target variable (y)
    X = selected_columns[['Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude']]
    y = selected_columns['Delivery_Time']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestRegressor(random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'Mean Absolute Error (MAE) on Test Data: {mae}')

    # Save the model to a file using pickle
    with open('delivery_time_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    # Return the trained model
    return model

def predict_delivery_time(model, drop_points):
    """
    Predict the delivery time for a list of drop points using the trained model.
    
    drop_points: List of tuples containing (Drop_Latitude, Drop_Longitude, Store_Latitude, Store_Longitude)
    """
    # Prepare input features (Store and Drop Latitudes and Longitudes)
    predictions = {}
    for point in drop_points:
        store_lat, store_lon, drop_lat, drop_lon = point
        features = [[store_lat, store_lon, drop_lat, drop_lon]]
        predicted_time = model.predict(features)[0]
        predictions[point] = predicted_time

    return predictions

def load_model():
    """
    Load the trained model from the file.
    """
    with open('delivery_time_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def main():
    """
    Main function to train the model, save it, and make predictions.
    """
    # Train the model and save it
    model = train_model()

    # Example drop points to predict delivery time for (Store_Latitude, Store_Longitude, Drop_Latitude, Drop_Longitude)
    drop_points = [
        (37.7749, -122.4194, 37.8044, -122.2711),  # Example (Store and Drop points)
        (34.0522, -118.2437, 34.0522, -118.2437),
    ]
    
    # Predict delivery times for the drop points using the saved model
    predictions = predict_delivery_time(model, drop_points)
    
    print("Predicted Delivery Times for the Drop Points:")
    for point, time in predictions.items():
        print(f"Drop Point {point}: {time} minutes")

if __name__ == "__main__":
    main()
