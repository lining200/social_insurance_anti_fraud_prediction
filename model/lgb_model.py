# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     lgb_model
   Description :
   Author :       Administrator
   date：          2018/7/12 0012
-------------------------------------------------
   Change Activity:
                   2018/7/12 0012:
-------------------------------------------------
"""
__author__ = 'Administrator'
import time
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import lightgbm as lgb
from sklearn import preprocessing
# from feature_integrate.feature_integrate import *
from feature_integrate.feature_integrate2 import *
# from feature_integrate.feature_integrate3 import *
import numpy as np

seed=1024
# np.random.seed(seed)
time_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))


#标准化
def normalization(df):
    X = df.values
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)
    print("preprocessing done!")
    df = pd.DataFrame(X, columns = df.columns)
    return df

# train = train()
# test = test()
train = pd.read_csv('../data/train_feature.csv')
test = pd.read_csv('../data/test_feature.csv')

train_path = '../data/feature/train/'
test_path = '../data/feature/test/'
# train = pd.read_csv(train_path + 'train_derive.csv')
# test = pd.read_csv(test_path + 'test_derive.csv')

train_id = pd.read_csv('../data/train_id.tsv', sep='\t')
train = train.merge(train_id, on='PERSONID', how='left')
train = train.fillna(0)
train_y = train.pop('LABEL')

feature_name = ['PERSONID', 'm_count3', 'm_count4', 'm_count5', 'm_count6', 'm_count7', 'm_count8', 'ftr51_mean', 'ftr51_median', 'ftr51_std', 'ftr51_max', 'ftr51_min', 'ftr51_sum', 'm_avg_n1', 'm_avg_n2', 'm_avg_n3', 'm_avg_n4', 'm_avg_n5', 'm_avg_n6', 'm_avg_n7', 'm_avg_n8', 'm_avg_n9', 'm_avg_n10', 'm_avg_n11', 'm_avg_n12', 'm_ev_mon_num1', 'm_ev_mon_num2', 'm_ev_mon_num3', 'm_ev_mon_num4', 'm_ev_mon_num5', 'm_ev_mon_num6', 'm_ev_mon_num7', 'm_ev_mon_num8', 'm_ev_mon_num9', 'm_ev_mon_num10', 'm_ev_mon_num11', 'm_ev_mon_num12', 'ev_day_avg1', 'ev_day_avg2', 'ev_day_avg3', 'ev_day_avg4', 'ev_day_avg5', 'ev_day_avg6', 'ev_day_avg7', 'ev_day_avg8', 'ev_day_avg9', 'ev_day_avg10', 'ev_day_avg11', 'ev_day_avg12', 'ev_day_avg13', 'ev_day_avg14', 'ev_day_avg15', 'ev_day_avg16', 'ev_day_avg17', 'ev_day_avg18', 'ev_day_avg19', 'ev_day_avg20', 'ev_day_avg21', 'ev_day_avg22', 'ev_day_avg23', 'ev_day_avg24', 'ev_day_avg30', 'ev_day_avg31', 'ftr_mean5', 'ftr_mean7', 'ftr_mean8', 'ftr_mean9', 'ftr_mean10', 'ftr_mean12', 'ftr_mean14', 'ftr_mean16', 'ftr_mean21', 'ftr_mean28', 'ftr_mean29', 'ftr_mean30', 'ftr_mean33', 'ftr_mean36', 'ftr_mean39', 'ftr_mean41', 'ftr_mean43', 'ftr_mean47', 'ftr_mean0', 'ftr_mean17', 'ftr_mean18', 'ftr_mean23', 'ftr_mean32', 'ftr_mean34', 'ftr_mean35', 'ftr_mean42', 'ftr_mean44', 'ftr_mean48', 'ftr_std5', 'ftr_std7', 'ftr_std8', 'ftr_std9', 'ftr_std10', 'ftr_std12', 'ftr_std14', 'ftr_std16', 'ftr_std21', 'ftr_std28', 'ftr_std29', 'ftr_std30', 'ftr_std33', 'ftr_std36', 'ftr_std39', 'ftr_std41', 'ftr_std43', 'ftr_std47', 'ftr_std0', 'ftr_std17', 'ftr_std18', 'ftr_std23', 'ftr_std32', 'ftr_std34', 'ftr_std35', 'ftr_std42', 'ftr_std44', 'ftr_std48', 'ftr_max5', 'ftr_max7', 'ftr_max8', 'ftr_max9', 'ftr_max10', 'ftr_max12', 'ftr_max14', 'ftr_max16', 'ftr_max21', 'ftr_max28', 'ftr_max29', 'ftr_max30', 'ftr_max33', 'ftr_max36', 'ftr_max39', 'ftr_max41', 'ftr_max43', 'ftr_max47', 'ftr_max0', 'ftr_max17', 'ftr_max18', 'ftr_max23', 'ftr_max32', 'ftr_max34', 'ftr_max35', 'ftr_max42', 'ftr_max44', 'ftr_max48', 'ftr_skew5', 'ftr_skew7', 'ftr_skew8', 'ftr_skew9', 'ftr_skew10', 'ftr_skew12', 'ftr_skew14', 'ftr_skew16', 'ftr_skew21', 'ftr_skew28', 'ftr_skew29', 'ftr_skew30', 'ftr_skew33', 'ftr_skew36', 'ftr_skew39', 'ftr_skew41', 'ftr_skew43', 'ftr_skew47', 'ftr_skew0', 'ftr_skew17', 'ftr_skew18', 'ftr_skew23', 'ftr_skew32', 'ftr_skew34', 'ftr_skew35', 'ftr_skew42', 'ftr_skew44', 'ftr_skew48', 'ftr_sum5', 'ftr_sum7', 'ftr_sum8', 'ftr_sum9', 'ftr_sum10', 'ftr_sum12', 'ftr_sum14', 'ftr_sum16', 'ftr_sum21', 'ftr_sum28', 'ftr_sum29', 'ftr_sum30', 'ftr_sum33', 'ftr_sum36', 'ftr_sum39', 'ftr_sum41', 'ftr_sum43', 'd_count1', 'd_count2', 'd_count3', 'd_count4', 'd_count5', 'd_count6', 'd_count7', 'd_count8', 'd_count9', 'd_count10', 'd_count11', 'd_count12', 'd_count13', 'd_count14', 'd_count15', 'd_count16', 'd_count17', 'd_count18', 'd_count19', 'd_count20', 'd_count21', 'd_count22', 'd_count23', 'd_count24', 'd_count30', 'd_count31', 'diff_day_mean', 'diff_day_std', 'diff_day_min', 'diff_day_max', 'diff_day_sum', 'ftr_nunique0', 'ftr_nunique5', 'ftr_nunique7', 'ftr_nunique8', 'ftr_nunique9', 'ftr_nunique10', 'ftr_nunique12', 'ftr_nunique14', 'ftr_nunique16', 'ftr_nunique21', 'ftr_nunique28', 'ftr_nunique29', 'ftr_nunique47', 'ftr_nunique51', 'ftr_rate0', 'ftr_rate5', 'ftr_rate7', 'ftr_rate8', 'ftr_rate9', 'ftr_rate10', 'ftr_rate12', 'ftr_rate14', 'ftr_rate16', 'ftr_rate21', 'ftr_rate28', 'ftr_rate29', 'ftr_rate47', 'ftr_rate51', 'm_unique1', 'm_unique2', 'm_unique3', 'm_unique4', 'm_unique5', 'm_unique6', 'm_unique7',
                'm_unique8', 'm_unique9', 'm_unique10', 'm_unique11', 'm_unique12', 'ftr_sum_c1', 'ftr_count_c1',
                'm_count1_c1', 'm_count1_c2']

features = [x for x in train.columns if  x in feature_name]
train = train[features]
test = test[features]

print('the feature name is: ' + str(test.columns))
print('the number of feature: ' + str(train.shape))
print('the number of feature: ' + str(test.shape))

train_userid = train.pop('PERSONID')
col = train.columns
train = normalization(train[col])
train_x = train.values
test_userid = test.pop('PERSONID')
test = normalization(test.fillna(0))



# params = {
#     'boosting_type': 'gbdt',
#     'objective': 'binary',
#     'metric': {'auc'},
#     'num_leaves': 32,
#     'learning_rate': 0.02,
#     'feature_fraction': 0.65,
#     'bagging_fraction': 0.8,
#     'bagging_freq': 5,
#     'verbose': 0,
#     'min_split_gain': 0.1,
#     'reg_alpha': 10,
#     'nthread': 10,
#     'scale_pos_weight': 2
# }

params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': {'auc'},
    'num_leaves': 32,
    'learning_rate': 0.2,
    'feature_fraction': 65,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0,
    'min_split_gain': 0.1,
    # 'reg_alpha': 10,
    'nthread': 10,
    'scale_pos_weight': 2
}



kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=2017)
n = 0
cv = []
for index_train, index_eval in kf.split(train,train_y):

    x_train, x_eval = train.iloc[index_train], train.iloc[index_eval]
    y_train, y_eval = train_y[index_train], train_y[index_eval]

    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_eval = lgb.Dataset(x_eval, y_eval, reference=lgb_train)

    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=50000,
                    valid_sets=[lgb_eval],
                    verbose_eval=100,
                    early_stopping_rounds=200)
    # gbm = lgb.train(params,
    #                 lgb_train, # 训练集
    #                 valid_sets=lgb_eval,  # 验证集
    #                 num_boost_round=40000, # 迭代次数 40000 -> 10000
    #                 verbose_eval=250, # 每隔250次，打印日志
    #                 early_stopping_rounds=500)
    print('Start predicting...')
    y_pred = gbm.predict(x_eval, num_iteration=gbm.best_iteration)
    cv.append(roc_auc_score(y_eval, y_pred))

    print('start predicting on test...')
    # testpreds = gbm.predict(test.values, num_iteration=gbm.best_iteration)
    testpreds = gbm.predict(test.values)

    if n > 0:
        totalpreds = totalpreds + testpreds
    else:
        totalpreds = testpreds
    # gbm.save_model('lgb_model_fold_{}.txt'.format(n), num_iteration=gbm.best_iteration)
    n += 1

totalpreds = totalpreds / n
print('lgb best score', np.mean(cv))

# submit result
res = pd.DataFrame()
res['PERSONID'] = list(test_userid.values)
res['Pre'] = totalpreds
res.to_csv('../data/submit/lgb_%s.csv'%str(time_date), index=False, sep='\t')
# print('use time: '+ str(time_date - time.time()))

feature_names = [x for x in train.columns if x not in ['PERSONID','LABEL']]

# importance = pd.DataFrame({
#         'column': feature_names,
#         'importance': gbm.feature_importance(),
#     }).sort_values(by='importance')
# importance['importance'] = importance['importance'] / importance['importance'].sum()
#
# importance.to_csv( '../data/feature_importance/fi3.csv', index=False)
