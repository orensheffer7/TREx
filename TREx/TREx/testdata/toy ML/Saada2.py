from tpot import TPOTRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

#########

## Change params here

path = "./La_liga.csv" # path to csv (delimiter is ',')
categorial = ['City', 'Team', 'Country'] # Categorial features from finite set (color, country, day of week)
# numerical = ['Year', 'Rank'] # Numerical features - all non categorial should be numerical
toRemove = ['League'] # Remove all infinite set features (name, address)
target = ['Target'] # Value/Feature to predict (Binary in this case)

#########


### Open csv
df = pd.read_csv(path, delimiter=',')
print("Initially your table has " + str(df.shape[0]) + " examples over " + str(df.shape[1]) + " features")


### Prepare data for learning - Drop missing data
df = df.drop(toRemove, axis=1)

### Prepare data for learning - encode categoial features
df = pd.get_dummies(df, columns = categorial, drop_first=False, dummy_na=True)
df = df.fillna(df.mean())
print("After one hot encoding categorial features: Your table has " + str(df.shape[0]) + " examples over " + str(df.shape[1]) + " features")
target = df.pop(target[0]).values

X_train, X_test, y_train, y_test = train_test_split(df, target,
                                                    train_size=0.8, test_size=0.2, random_state=42)

tpot = TPOTRegressor(generations=5, population_size=100, verbosity=2, random_state=42)
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))
tpot.export('tpot_saada_pipeline.py')