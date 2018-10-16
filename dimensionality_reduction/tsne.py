import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE


if __name__ == '__main__':
    os.system('clear')
    sns.set_style("darkgrid")

    # Load dataset
    data = sns.load_dataset('iris')
    print(data.describe())
    
    # Print scatter plot of features
    sns.lmplot( x='sepal_length', 
                y='sepal_width', 
                data=data, 
                hue='species', 
                palette='Set1', 
                fit_reg=False)
    plt.title('2-Feature space')

    # Create feature data: X
    X = data.drop('species', axis=1).values
    
    # Transform using TSNE
    model = TSNE(learning_rate=100, random_state=42)
    X_proj = model.fit_transform(X)

    cols = ['Component %d' % (i + 1) for i in range(X_proj.shape[1])]
    X_low_dim = pd.DataFrame(data=X_proj, columns=cols)
    X_low_dim['species'] = data['species']
    
    # Plot reduced space
    sns.lmplot( x=cols[0],
                y=cols[1],
                data=X_low_dim,
                hue='species',
                fit_reg=False,
                palette='Set1')
    plt.title('Low dimmension - TSNE')
    plt.show()