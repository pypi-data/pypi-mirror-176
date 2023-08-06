from autofe import autofe
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
 
def load_data():
    breast_cancer_bunch = load_breast_cancer()

    breast_cancer_data = pd.DataFrame(breast_cancer_bunch.data,columns=breast_cancer_bunch.feature_names)
    breast_cancer_target = pd.DataFrame(breast_cancer_bunch.target,columns=['target'])
    feature_cols = breast_cancer_bunch.feature_names.tolist()
    breast_cancer_data['id'] = [i for i in range(len(breast_cancer_data))]
    x_train, x_test, y_train, y_test = train_test_split(breast_cancer_data, breast_cancer_target, test_size=0.3, random_state=0)
    return x_train, x_test, y_train, y_test, feature_cols


if __name__=='__main__':

    x_train, x_test, y_train, y_test, feature_cols = load_data()

    afe = autofe.AutoFE('id', feature_cols, k1=5, k2=5)

    afe.fit(x_train, y_train)

    x_train = afe.transform(x_train)
    x_test = afe.transform(x_test)

    finaldf = afe.generator(x_train, x_test, y_train, y_test)
    print(finaldf.shape)
    print(finaldf.columns)
