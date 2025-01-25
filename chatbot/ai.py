# Step 1: Import the libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Step 2: Load the dataset
# Replace 'data.csv' with your dataset file
data = pd.read_csv('data.csv')

# Step 3: Split the data into features (X) and target (y)
# Replace 'target_column' with the name of the column you want to predict
X = data.drop('target_column', axis=1)
y = data['target_column']

# Step 4: Split into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 6: Make predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
