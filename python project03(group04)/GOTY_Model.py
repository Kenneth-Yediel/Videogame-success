# Declare all necessary libraries
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
# Declare the strategy pattern for the models
class MLStrategy(ABC):
# Make the abstract functions for the class
    @abstractmethod
    def predict(self, features):
        pass

    @abstractmethod
    def train(self, X, Y):
        pass

    @abstractmethod
    def get_model(self):
        pass
# RandomF Strategy
class RandomForestStrategy(MLStrategy):
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
        self.scaler = StandardScaler()

    def train(self, X, Y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, Y)
        return self.model

    def predict(self, features):
        features_scaled = self.scaler.transform([features])
        return self.model.predict(features_scaled)[0]

    def get_model(self):
        return self.model

    def get_scaler(self):
        return self.scaler
# Logistic Strategy
class LogisticRegressionStrategy(MLStrategy):
    def __init__(self):
        self.model = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced')
        self.scaler = StandardScaler()

    def train(self, X, Y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, Y)
        return self.model

    def predict(self, features):
        features_scaled = self.scaler.transform([features])
        return self.model.predict(features_scaled)[0]

    def get_model(self):
        return self.model

    def get_scaler(self):
        return self.scaler
# Load and read Dataset
dataframe = pd.read_csv('GOTY(2005-2023).csv')
# Print the head of the DataFrame to display the data
print("--- Head of the DataFrame ---")
print(dataframe.head())
# Take the dataset information for predictions
def takeData(data):
    dataframe1 = data.copy()
    # Clean the data
    dataframe1['Copies_sold'] = dataframe1['Copies sold'].astype(str).str.replace(',', '').astype(float)
    dataframe1['Revenue_clean'] = dataframe1['Revenue'].astype(str).str.replace('$', '').str.replace(',', '').astype(
        float)
# Add Revenue per copy (proxy for pricing/premium quality)
    dataframe1['Revenue_per_copy'] = dataframe1['Revenue_clean'] / dataframe1['Copies_sold']
# Log transformations for skewed features
    dataframe1['Log_Copies'] = np.log1p(dataframe1['Copies_sold'])
    dataframe1['Log_Revenue'] = np.log1p(dataframe1['Revenue_clean'])
# One-hot encode Genre column
    genres_encoded = pd.get_dummies(dataframe1['Genre'], prefix='Genre')
    features = ['Ratings', 'Revenue_per_copy', 'Log_Copies', 'Log_Revenue',
                'Narrative_Quality', 'Art_Direction', 'Innovation']
# Select numerical features and combine with encoded genres
    X_numeric = dataframe1[features]
    X = pd.concat([X_numeric, genres_encoded], axis=1)
# Create target variable (2 for Winner, 1 for Nominee, 0 for Non-Nominee)
    def map_status(status):
        if status == 'Winner':
            return 2
        elif status == 'Nominee':
            return 1
        else:  # Non-Nominee or empty
            return 0
    Y = dataframe1['GOTY_Status'].apply(map_status)
    return X.values, Y.values
# Redefine the values
X, Y = takeData(dataframe)
# Prepare the Kfold procedure
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
# K-fold model
def crossValidation(reg_model, X_prepared, Y_prepared, cv_splitter):
    scores = cross_val_score(reg_model, X_prepared, Y_prepared, cv=cv_splitter, scoring="accuracy", n_jobs=-1)
    print(f"\n=== CROSS-VALIDATION RESULTS ===")
    print("Accuracy scores for each fold:", np.round(scores, 3))
    print("Mean Accuracy:", np.round(scores.mean(), 3))
    print("Standard Deviation:", np.round(scores.std(), 3))
    return scores.mean(), scores.std()
# Multiple train-test model
def multipleTrainTestValidation(reg_model, X_prepared, Y_prepared, n_runs=10, test_size=0.1):
    accuracies = []
    print(f"\n=== MULTIPLE TRAIN-TEST SPLITS ({n_runs} runs) ===")
    for i in range(n_runs):
        # Split the data with different random state each time
        X_train, X_test, Y_train, Y_test = train_test_split(
            X_prepared, Y_prepared,
            test_size=test_size,
            random_state=42 + i,  # Different seed each run
            stratify=Y_prepared
        )
        # Train the model
        reg_model.fit(X_train, Y_train)
        # Make predictions
        Y_pred = reg_model.predict(X_test)
        # Calculate accuracy
        accuracy = accuracy_score(Y_test, Y_pred)
        accuracies.append(accuracy)
    print("All accuracies:", np.round(accuracies, 3))
    print("Mean Accuracy:", np.round(np.mean(accuracies), 3))
    print("Standard Deviation:", np.round(np.std(accuracies), 3))
    print("Accuracy Range:", f"{np.min(accuracies):.3f} - {np.max(accuracies):.3f}")
    return np.mean(accuracies), np.std(accuracies)
# Create train model using Strategy Pattern
randomF_Strat = RandomForestStrategy()
logistic_Strat = LogisticRegressionStrategy()
# Train both strategies
print("\n" + "=" * 60)
print("Training Strategies...")
print("=" * 60)
randomF_Strat.train(X, Y)
logistic_Strat.train(X, Y)
# Get scaled data for evaluation
X_scaled_randomF = randomF_Strat.get_scaler().transform(X)
X_scaled_logistic = logistic_Strat.get_scaler().transform(X)
