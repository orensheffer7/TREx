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
#df = df.dropna(axis = 1)
#print("After removing columns with NAN values: Your table has " + str(df.shape[0]) + " examples over " + str(df.shape[1]) + " features")
#df = df.dropna(axis = 0)
#print("After removing rows with NAN values: Your table has " + str(df.shape[0]) + " examples over " + str(df.shape[1]) + " features")


### Prepare data for learning - encode categoial features
df = pd.get_dummies(df, columns = categorial, drop_first=False, dummy_na=True)
df = df.fillna(df.mean())
print("After one hot encoding categorial features: Your table has " + str(df.shape[0]) + " examples over " + str(df.shape[1]) + " features")
target = df.pop(target[0]).values
X_train, X_test, y_train, y_test = train_test_split(df, target, test_size=0.2)

  
  
### Predict
print()
print() 
regr = linear_model.LinearRegression(normalize=True)
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)
print("Mean Squared Error:",  mean_squared_error(y_test, y_pred))
correct = 0
wrong = 0
for a,b in zip(y_test, [1 if x > 0.5 else 0 for x in y_pred]):
  if a == b:
    correct += 1
  else:
    wrong += 1
print("Prediction is done on 20% of the data which are {} examples:".format(len(y_test)))
a = list(zip(df.columns, regr.coef_))
a.sort(key=lambda x: abs(x[1]), reverse=True)
print(a)
print(regr.get_params)
print("Number of correct predictions: " + str(correct))
print("Number of wrong predictions: " + str(wrong))