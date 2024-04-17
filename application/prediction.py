from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def setup_prediction_model(target, non_target):
    # 70/30 train-test split
    X_train, X_test, y_train, y_test = train_test_split(target, non_target, test_size=0.3, random_state=42)

    # Create decision tree model
    dt = DecisionTreeClassifier()

    # fit model to training set
    dt.fit(X_train, y_train)

    return dt

# perform prediction given an input
def predictHeartRisk(input, dt):
    prediction = dt.predict(input)
    return prediction