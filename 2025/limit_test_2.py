#attempted model inversion attack
import requests

CHALLENGE_URL="https://limittheory.aictf.sg:5000"

def order():
    response = requests.get(
        f"{CHALLENGE_URL}/order"
    )
    return response.json()
response=order()
print(response)

token=response['token']

ingredient_list_1=response['order']['ingredient-list-1']
ingredient_list_2=response['order']['ingredient-list-2']
ingredient_list_3=response['order']['ingredient-list-3']

import numpy as np
from sklearn.preprocessing import PolynomialFeatures

class PandanLeavesPredictor:
    def __init__(self):
        self.intercept = 607.959
        self.coefficients = np.array([
            -77.061, -170.430, -75.798,
            -1.676, 58.267, 205.814,
            7.641, 21.661, 1.740
        ])
        self.poly = PolynomialFeatures(degree=2, include_bias=False)

    def predict(self, X):
        # X should be a NumPy array of shape (n_samples, 3)
        X_poly = self.poly.fit_transform(X)
        return self.intercept + np.dot(X_poly, self.coefficients)

predictor = PandanLeavesPredictor()
X_new = np.array([
    ingredient_list_1,
    ingredient_list_2,
    ingredient_list_3
])
predictions = predictor.predict(X_new)

# Store predictions for the first three samples in a result list
result = list(predictions[:3])  # Store only the first three predictions
for i, pred in enumerate(predictions):
    print(f"Sample {i+1}: Predicted pandan_leaves = {pred:.2f}")

def test(token, result):
    response = requests.post(
        f"{CHALLENGE_URL}/taste-test",
        headers={"Content-Type": "application/json"},
        json={
            "token": token,
            "result": result
        },
    )
    return response.json()
print("TESTING...")
response=test(token,result)
print(response)
