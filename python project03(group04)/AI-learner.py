# Declare all necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
# Load and read Dataset
dataframe = pd.read_csv('GOTY(2005-2023).csv')
# Print the head of the DataFrame to display the data
print("--- Head of the DataFrame ---" )
print(dataframe.head())
# Take the dataset information for predictions
def takeData(data):
    dataframe1 = data.copy()
# Clean the data
    dataframe1['Copies_sold'] = dataframe1['Copies sold'].astype(str).str.replace(',', '').astype(float)
    dataframe1['Revenue_clean'] = dataframe1['Revenue'].astype(str).str.replace('$', '').str.replace(',', '').astype(float)
    features = ['Ratings', 'Copies_sold', 'Revenue_clean']
    X = dataframe1[features]
# Create target variable (1 for Winner, 0 for Nominee)
    Y = dataframe1['GOTY_Status'].apply(lambda x: 1 if x == 'Winner' else 0)
    return X.values, Y.values
# Redefine the values
X, Y = takeData(dataframe)
# Scaling the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Prepare the Kfold procedure
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
def crossValidation(reg_model, X_prepared, Y_prepared, cv_splitter):
    scores = cross_val_score(reg_model, X_prepared, Y_prepared, cv=cv_splitter, scoring="accuracy", n_jobs=-1)
    print(f"\n=== CROSS-VALIDATION RESULTS ===")
    print("Accuracy scores for each fold:", np.round(scores, 3))
    print("Mean Accuracy:", np.round(scores.mean(), 3))
    print("Standard Deviation:", np.round(scores.std(), 3))
    return scores.mean(), scores.std()
# Multiple train-test
def multipleTrainTestValidation(reg_model, X_prepared, Y_prepared, n_runs=10, test_size=0.2):
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
# Create train model
logistic_reg = LogisticRegression(random_state=42, max_iter=1000)
randomF_class = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
# Run cross-validation on loaded data
print("\n" + "="*60)
print("With Random Forest:")
print("="*60)
crossValidation(randomF_class, X_scaled, Y, kfold)
# Run train-test validation
multipleTrainTestValidation(randomF_class, X_scaled, Y)
print("\n" + "="*60)
print("With Logistic Regression:")
print("="*60)
crossValidation(logistic_reg, X_scaled, Y, kfold)
multipleTrainTestValidation(logistic_reg, X_scaled, Y)

