from sklearn import metrics
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pandas as pd

# Load dataset
df = pd.read_csv('iris.csv', names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'Class'])
X = df.drop('Class', axis=1)
y = df['Class'].astype('category').cat.codes.astype(int)

# Split dataset: training and testing group
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=101)

# Set Feature columns
sepal_length = tf.feature_column.numeric_column('sepal_length')
sepal_width = tf.feature_column.numeric_column('sepal_width')
petal_length = tf.feature_column.numeric_column('petal_length')
petal_width = tf.feature_column.numeric_column('petal_width')

feature_cols = [sepal_length, sepal_width, petal_length, petal_width]

# Create input functions for training and testing
train_input_function = tf.estimator.inputs.pandas_input_fn(x=X_train, y=y_train,
                                                           batch_size=10, num_epochs=1000,
                                                           shuffle=True)
test_input_function = tf.estimator.inputs.pandas_input_fn(x=X_test, y=y_test,
                                                          batch_size=10, num_epochs=1,
                                                          shuffle=False)

# Create a model
model = tf.estimator.DNNClassifier(feature_columns=feature_cols, hidden_units=[10, 20, 20, 10],  n_classes=3)

# Train model
model.train(input_fn=train_input_function, steps=1000)

# Evaluate the model
results = model.evaluate(test_input_function)
print(results)
