from google.colab import drive
drive.mount('/content/drive')

from warnings import filterwarnings
filterwarnings('ignore')

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

## Loading dataset
data1 = pd.read_csv('/content/drive/MyDrive/AML/heart.csv',skipinitialspace=True)
data1.head()

## Checking missing entries in the dataset columnwise
data1.isna().sum()

#Ensemble Methods
#Bagging and Random Forest
from sklearn import model_selection
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

x=pd.DataFrame(data1.iloc[:,:-1]) 
y=pd.DataFrame(data1["target"])

#seed = 8
kfold = model_selection.KFold(n_splits = 3, random_state = None)
  
# initialize the base classifier
base_cls = DecisionTreeClassifier()
  
# no. of base classifier
num_trees = 500
  
# bagging classifier
model = BaggingClassifier(base_estimator = base_cls,
                          n_estimators = num_trees,
                          random_state = None)
  
results = model_selection.cross_val_score(model, x, y, cv = kfold)
print("accuracy :")
print(results.mean())

#Random Forest

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score
#seed = 10
x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.8,
                                               random_state=0) 
print(x_train.shape) 
print(x_test.shape) 
print(y_train.shape) 
print(y_test.shape) 
RFCModel=RandomForestClassifier(n_estimators=100) 
RFCModel.fit(x_train,y_train) 
y_pred2=RFCModel.predict(x_test) 
print(accuracy_score(y_test,y_pred2))

from scipy.stats import randint
from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import HalvingRandomSearchCV
from sklearn.datasets import make_classification

#rng = np.random.RandomState(0)
#X, y = make_classification(n_samples=700, random_state=rng)

RFCModel2 = RandomForestClassifier(n_estimators=100, random_state=0)

param_dist = {
    "max_depth": [3, None],
    "max_features": randint(1, 13),
    "min_samples_split": randint(2, 13),
    "bootstrap": [True, False],
    "criterion": ["gini", "entropy"],
}

rsh = HalvingRandomSearchCV(estimator=RFCModel2, param_distributions=param_dist, 
                            factor=2, random_state=0)
rsh.fit(x, y)
rsh.best_params_

#BootStrap Method, Bootstrap Aggregation, Variable Importance

plt.figure(figsize=(18,12))
plt.subplot(221)
data1["sex"].value_counts().plot.pie(autopct = "%1.0f%%",
                colors = sns.color_palette("prism",5),
                startangle = 60,labels=["Male","Female"],
wedgeprops={"linewidth":2,"edgecolor":"k"},explode=[.1,.1],shadow =True)
plt.title("Distribution of Gender")
plt.subplot(222)
ax= sns.distplot(data1['age'], rug=True)
plt.title("Age wise distribution")
plt.show()

# filtering numeric features as age , resting bp, cholestrol and max heart rate achieved has outliers as per EDA
#resting_blood_pressure = trestbps
#cholesterol = chol
#max_heart_rate_achieved=thalach
dt_numeric = data1[['age','trestbps','chol','thalach']]

dt_numeric.head()

# calculating zscore of numeric columns in the dataset
from scipy import stats
z = np.abs(stats.zscore(dt_numeric))
print(z)

# Defining threshold for filtering outliers 
threshold = 3
print(np.where(z > 3))

#filtering outliers retaining only those data points which are below threshhold
data2 = data1[(z < 3).all(axis=1)]

data2.shape

## encoding categorical variables
data2 = pd.get_dummies(data2, drop_first=True)

data2.head()

data2.shape

# segregating dataset into features i.e., X and target variables i.e., y
X = data2.drop(['target'],axis=1)
y = data2['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2,shuffle=True, random_state=5)

print('------------Training Set------------------')
print(X_train.shape)
print(y_train.shape)

print('------------Test Set------------------')
print(X_test.shape)
print(y_test.shape)

#feature normalization
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train[['age','trestbps','chol','thalach','slope']] = scaler.fit_transform(X_train[['age','trestbps','chol','thalach','slope']])
X_train.head()

X_test[['age','trestbps','chol','thalach','slope']] = scaler.transform(X_test[['age','trestbps','chol','thalach','slope']])
X_test.head()

from sklearn import model_selection
from sklearn.model_selection import cross_val_score
import xgboost as xgb
# function initializing baseline machine learning models
def GetBasedModel():
    basedModels = []
    #basedModels.append(('LR_L2'   , LogisticRegression(penalty='l2')))
    basedModels.append(('LDA'  , LinearDiscriminantAnalysis()))
    basedModels.append(('KNN7'  , KNeighborsClassifier(7)))
    basedModels.append(('KNN5'  , KNeighborsClassifier(5)))
    basedModels.append(('KNN9'  , KNeighborsClassifier(9)))
    basedModels.append(('KNN11'  , KNeighborsClassifier(11)))
    basedModels.append(('CART' , DecisionTreeClassifier()))
    basedModels.append(('NB'   , GaussianNB()))
    basedModels.append(('SVM Linear'  , SVC(kernel='linear',gamma='auto',probability=True)))
    basedModels.append(('SVM RBF'  , SVC(kernel='rbf',gamma='auto',probability=True)))
    basedModels.append(('AB'   , AdaBoostClassifier()))
    basedModels.append(('GBM'  , GradientBoostingClassifier(n_estimators=100,max_features='sqrt')))
    basedModels.append(('RF_Ent100'   , RandomForestClassifier(criterion='entropy',n_estimators=100)))
    basedModels.append(('RF_Gini100'   , RandomForestClassifier(criterion='gini',n_estimators=100)))
    basedModels.append(('ET100'   , ExtraTreesClassifier(n_estimators= 100)))
    basedModels.append(('ET500'   , ExtraTreesClassifier(n_estimators= 500)))
    basedModels.append(('MLP', MLPClassifier()))
    basedModels.append(('SGD3000', SGDClassifier(max_iter=1000, tol=1e-4)))
    basedModels.append(('XGB_2000', xgb.XGBClassifier(n_estimators= 2000)))
    basedModels.append(('XGB_500', xgb.XGBClassifier(n_estimators= 500)))
    basedModels.append(('XGB_100', xgb.XGBClassifier(n_estimators= 100)))
    basedModels.append(('XGB_1000', xgb.XGBClassifier(n_estimators= 1000)))
    basedModels.append(('ET1000'   , ExtraTreesClassifier(n_estimators= 1000)))
    
    return basedModels

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
from sklearn.metrics import log_loss,roc_auc_score,precision_score,f1_score,recall_score,roc_curve,auc
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score,fbeta_score,matthews_corrcoef
from sklearn import metrics
from sklearn.metrics import log_loss
from imblearn.metrics import geometric_mean_score
import warnings
import re
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC 
import xgboost as xgb
#from vecstack import stacking
from scipy import stats
import os

# function for performing 10-fold cross validation of all the baseline models
def BasedLine2(X_train, y_train,models):
    # Test options and evaluation metric
    num_folds = 10
    scoring = 'accuracy'
    seed = 7
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)                 
    return results,msg

#models = GetBasedModel()
#names,results = BasedLine2(X_train, y_train,models)
results