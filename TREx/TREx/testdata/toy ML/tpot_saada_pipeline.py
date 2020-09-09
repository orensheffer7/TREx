import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import train_test_split

path = "./La_liga.csv" # path to csv (delimiter is ',')
categorial = ['City', 'Team', 'Country'] # Categorial features from finite set (color, country, day of week)
# numerical = ['Year', 'Rank'] # Numerical features - all non categorial should be numerical
toRemove = ['League'] # Remove all infinite set features (name, address)
target = ['target'] # Value/Feature to predict (Binary in this case)


# NOTE: Make sure that the outcome column is labeled 'target' in the data file
df = pd.read_csv("./La_liga.csv", sep=',')

### Prepare data for learning - Drop missing data
df = df.drop(toRemove, axis=1)

### Prepare data for learning - encode categoial features
df = pd.get_dummies(df, columns = categorial, drop_first=False, dummy_na=True)
df = df.fillna(df.mean())
print("After one hot encoding categorial features: Your table has " + str(df.shape[0]) + " examples over " + str(df.shape[1]) + " features")
target = df.pop(target[0]).values
X_train, X_test, y_train, y_test = train_test_split(df, target, random_state=42)


# Average CV score on the training set was: 0.0
exported_pipeline = AdaBoostRegressor(learning_rate=0.01, loss="exponential", n_estimators=100)
# Fix random state in exported estimator
if hasattr(exported_pipeline, 'random_state'):
    setattr(exported_pipeline, 'random_state', 42)

exported_pipeline.fit(X_train, y_train)
results = exported_pipeline.predict(X_test)
print(results)
print(y_test)
