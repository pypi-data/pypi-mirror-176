import pandas as pd
import numpy as np
import random
import itertools
import copy
import lightgbm as lgb
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import multiprocessing as mp
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_X_y
from sklearn.utils.multiclass import unique_labels
import copyreg
import types
import warnings
warnings.filterwarnings("ignore")


def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    cls_name = ''
    if func_name.startswith('__') and not func_name.endswith('__'):
        cls_name = cls.__name__.lstrip('_')
    if cls_name:
        func_name = '_' + cls_name + func_name
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


copyreg.pickle(types.MethodType, _pickle_method, _unpickle_method)



class Operator():
    """
    define all the operator of dfs
    """
    
    def __init__(self, data1, data2, f1, f2):
        self.data1 = data1
        self.data2 = data2
        self.f1 = f1
        self.f2 = f2
        

    def add(self):
        return self.data1[self.f1].fillna(0)+self.data2[self.f2].fillna(0)
    
    def minus(self):
        return self.data1[self.f1].fillna(0)-self.data2[self.f2].fillna(0)
    
    def multiply(self):
        return self.data1[self.f1] * self.data2[self.f2]
    
    def divide(self):
        return (self.data1[self.f1]+1) / (self.data2[self.f2]+1)

    def run(self):
        add = self.add()
        minus = self.minus()
        multiply = self.multiply()
        divide = self.divide()
        newf = pd.DataFrame({f'({self.f1}+{self.f2})':add, f'({self.f1}-{self.f2})':minus, f'({self.f1}*{self.f2})':multiply, f'({self.f1}/{self.f2})':divide})
        return newf


class AutoFE(BaseEstimator, TransformerMixin):

    def __init__(self, primary_key, feature_cols, k1=10, k2=8, batch_size=30000, random_seed=2022, is_autoterminate=True):
        """
        primary_key: string, the primary key for identify one data sample
        feature_cols: list, for all the features that involved in feature engineering
        k1: int, the number of features that choose from aggregation
        k2: int, the number of features that choose from crossing
        batch_size: int, the number of features that involved in crossing at the first time
        random_seed: int, the number for setting the random state
        is_autoterminate: bool, if automatically terminate the feature engineering process
        """
        self.random_seed = random_seed
        self.primary_key = primary_key
        self.feature_cols = feature_cols
        self.k1 = k1 
        self.k2 = k2
        self.batch_size = batch_size
        self.random_seed = random_seed
        self.is_autoterminate=is_autoterminate


    def fit(self, X, y):

        # Check that X and y have correct shape
        check_X_y(X, y)
        # Store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.X_ = X[self.feature_cols+[self.primary_key]].dropna(thresh=int(0.7*X[self.feature_cols].shape[0]),axis=1)
        self.y_ = y

        self.highest_non_inf = X[self.feature_cols].max().loc[lambda v: v<np.inf].max()
        self.lowest_non_inf = X[self.feature_cols].min().loc[lambda v: v>-np.inf].min()

        self.median_ = X[self.feature_cols].median()

        # Return the classifier

        return self

    def transform(self, X):
        X = X.copy()
        X = X[self.X_.columns]
        
        X = X.replace(np.Inf, self.highest_non_inf)
        X = X.replace(-np.inf, self.lowest_non_inf)
        X = X.fillna(self.median_)

        return X

    def aggregation(self, data, cols):
        tmp = data[cols].pct_change()
        tmp.columns = [i+"_pct" for i in cols]
        f = pd.concat([data,tmp],axis=1)

        t = f[[self.primary_key]+cols+tmp.columns.tolist()].groupby([self.primary_key]).agg([np.sum, np.mean, np.std,np.min,np.max])
        t.columns = t.columns.map('_'.join)
        t.reset_index(inplace=True)
        return t

    def fcross(self, l1, l2):
        new = []
        for i in l1:
            for j in l2:
                x = (i, j)
                new.append(x)
        new = list(set(new))
        return new

    def selector(self, X, y, k):
        model = LGBMClassifier(random_state=self.random_seed, n_jobs=1)
        
        newcol = [f"f{x}" for x in range(X.shape[1])]
        cols = X.columns.tolist()
        cols.sort()
        X = X[cols]
        colname = dict(zip(newcol, cols))
        X.columns = colname
        model.fit(X, y)
        feature_importance = pd.DataFrame({
                'feature': model.booster_.feature_name(),
                'gain': model.booster_.feature_importance('gain'),
                'split': model.booster_.feature_importance('split')
            }).sort_values('split',ascending=False)
        selectCol = [colname[x] for x in feature_importance['feature'][:k]]
        
        return selectCol
    
    def order_iter(self, order):
        random.seed(self.random_seed)
        random.shuffle(order)
        for i in range(0, len(order), self.batch_size):
            mini_batch = order[i: min(i + self.batch_size, len(order))]
            yield mini_batch

    def ifContinue(self, X, y):
        x_train, x_test, y_train, y_test = train_test_split(X.drop([self.primary_key,'flag','label'],axis=1), y, test_size=0.3, random_state=self.random_seed)
        lgb_train =  lgb.Dataset(x_train, label=y_train)
        lgb_eval = lgb.Dataset(x_test, label=y_test, reference=lgb_train) 
        
        parameters = {
                'task': 'train',
                'max_depth': 5,
                'boosting_type': 'gbdt',
                'objective': 'binary',
                'metric': 'auc',
                'is_unbalance': True, 
                'verbose': -1,
                'random_state': self.random_seed,
                'n_jobs': 1
                }
        
        evals_result = {}
        gbm_model = lgb.train(parameters,
                        lgb_train,
                        valid_sets=[lgb_train,lgb_eval],
                        num_boost_round=50,
                        early_stopping_rounds=500,
                        evals_result=evals_result,
                        verbose_eval=False
                        )

        prediction = gbm_model.predict(x_test,num_iteration=gbm_model.best_iteration)
        score = roc_auc_score(y_test, prediction)
        return score

    def rowToCol(self, df):
        if df[self.primary_key].nunique() == df.shape[0]:
            return df
        else:
            n = df.shape[0]/df[self.primary_key].nunique()
            multi = [str(i+1) for i in range(int(n))]
            df['entry_num'] = multi*(df[self.primary_key].nunique())
            tmp = df.drop_duplicates(subset=[self.primary_key,'flag','label'],keep='first')[[self.primary_key,'flag','label']]
            cols = [col for col in df.columns if col not in [self.primary_key,'flag','label']]

            for col in cols:
                two_level = df.set_index([self.primary_key, "entry_num"])[col]
                two_level_unstack = two_level.unstack().rename_axis(columns=None).reset_index()
                two_level_unstack.columns = [self.primary_key] + [f'{col}_{i}' for i in multi]
                tmp = pd.merge(tmp, two_level_unstack, how='left',on=self.primary_key)
            return tmp

    def init(self, l):
        global lock
        lock = l

    def calOp_multi(self, f, df, testSample, minitestdfCol, minitestdata):
        f1,f2 = f
        op = Operator(df, testSample, f1, f2)
        minitestdf = op.run()
        minitestdfCol.extend(minitestdf.columns.tolist())    
        minitestdata = pd.concat([minitestdata, minitestdf], axis=1)
        return minitestdfCol, minitestdata



    def calOp(self, mini_order, df, testSample, firstround=True):
        minitestdfCol = []
        if firstround:
            minitestdata = df[[self.primary_key]]
        else:
            minitestdata = df
        lock = mp.Lock()
        pool = mp.Pool(initializer=self.init, initargs=(lock,))
        res =[]
        for f in mini_order:
            a = pool.apply_async(self.calOp_multi, (f, df, testSample, minitestdfCol, minitestdata,))
            res.append(a)
        pool.close()
        pool.join()
        
        minitestdfCol = []
        minitestdata = []
        tmp = [i.get() for i in res]

        for i in tmp:
            x,y = i
            minitestdfCol.extend(x)
            minitestdata.append(y)

        minitestdata = pd.concat(minitestdata,axis=1)
        minitestdata = pd.concat([y[self.primary_key],minitestdata[minitestdfCol]],axis=1)     
        miniy = pd.merge(testSample[[self.primary_key,'flag','label']], minitestdata, how='inner', on=self.primary_key)
        minibestcols = self.selector(miniy[miniy['label']=='x_train'].drop([self.primary_key,'flag','label'],axis=1),miniy[miniy['label']=='x_train']['flag'], self.k2) # just use train
        minitestdata = minitestdata[[self.primary_key]+minibestcols] 

        return minibestcols, minitestdata


    def generator(self, x_train, x_test, y_train, y_test):
        
        x_train['label'] = 'x_train'
        x_train['flag'] = y_train
        x_test['label'] = 'x_test'
        x_test['flag'] = y_test
        
        df = pd.concat([x_train,x_test], axis=0, ignore_index=True)

        data = self.rowToCol(df)
        cols = [col for col in data.columns if col not in [self.primary_key,'flag','label']]
        cols_ = self.feature_cols
        testSample = data[cols+[self.primary_key,'flag','label']]

        originalset = cols

        i = 0
        order=[]
        sequeece = []

        bestcols=[]

        testdata = testSample[[self.primary_key]]
        finaldf = copy.deepcopy(testSample[[self.primary_key,'flag','label']])

        auc_value_0 = 0

        for i in range(len(cols)-2):
            if i > 0 :
                order = self.fcross(bestcols, originalset)
                bestcols, testdata = self.calOp(order, testdata, testSample, firstround=False)
                finaldf = pd.concat([finaldf, testdata[bestcols]], axis=1)
                sequeece+=bestcols
                i+=1    

                if self.is_autoterminate == True:
                    # autotermination condition: if the new derived feature cannot improve the auc then stop deriving
                    auc_value_1 = copy.deepcopy(auc_value_0)

                    auc_value_0 = self.ifContinue(finaldf[finaldf['label']=='x_train'], finaldf[finaldf['label']=='x_train']['flag'])
                    if auc_value_0 <= auc_value_1:
                        break

            else:
                for j in itertools.combinations(originalset, 2):
                    order.append(j) 

                bestminidf = testSample[[self.primary_key,'flag','label']]
                
                for mini_order in self.order_iter(order):
                    minibestcols, minitestdata = self.calOp(mini_order, testSample, testSample)
                    bestminidf =  pd.concat([bestminidf, minitestdata[minibestcols]], axis=1)
                bestcols = self.selector(bestminidf[bestminidf['label']=='x_train'].drop([self.primary_key,'flag','label'],axis=1),bestminidf[bestminidf['label']=='x_train']['flag'], self.k2)
                finaldf = pd.concat([finaldf, bestminidf[bestcols]], axis=1)

                testdata = bestminidf[[self.primary_key]+bestcols]
                sequeece+=bestcols

                i+=1

        # add aggregation calculation
        df_agg = self.aggregation(df, cols_)
        df_agg = pd.merge(data[[self.primary_key,'flag','label']],df_agg, how='inner', on=self.primary_key)

        agg_bestcols = self.selector(df_agg[df_agg['label']=='x_train'].drop([self.primary_key,'flag','label'],axis=1),df_agg[df_agg['label']=='x_train']['flag'], self.k1)

        final_agg = df_agg[[self.primary_key]+agg_bestcols]

        finaldf = pd.merge(finaldf, final_agg, how='inner', on=self.primary_key)

        return finaldf
