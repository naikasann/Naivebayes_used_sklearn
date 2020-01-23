from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB 

from sklearn.metrics import classification_report
from gensim.models.word2vec import Word2Vec

from Morphological.Morphological_analysis import Morphological_analysis
from CreateDataset.CreateDataset import CreateDataset
from MakeLog.MakeLog import MakeLog

import pandas as pd
import numpy as np

###################################################
#                 setiing tool                    #
###################################################
print("=========================================")
print("#           naivebayse execute          #")
print("=========================================")

train_path = "./dataset/train/train.csv"
test_path  = "./dataset/test/test.csv"

dataaugment = True
model_path = "./word2vec_model/word2vec.gensim.model"
model = Word2Vec.load(model_path)

#method type
# 0:tfidf
# 1:Bag of Word
# 2: tfidf vector
method = 0

#Evaluation type
# 0:default
# 1:Evaluation method considering similarity
evaluation = 1

alpha = 0.1

label = [
        "test", "test2"]

###################################################
#                Create_dataset                   #
###################################################
print("dataset loading...")
print("dataset augment :", dataaugment)
dataset = CreateDataset()
morphological = Morphological_analysis()

if dataaugment:
    x_train, xtest, y_train, y_test = dataset.data_augment_use_word2vec(model, train_path, test_path)
else:
    x_data, x_test_data, y_train, y_test = dataset.createdataset(train_path, test_path)
    x_train, xtest = morphological.data_morphological(x_data, x_test_data)
print("dataset load complete.")
###################################################
#               Evaluation type                   #
###################################################
if evaluation == 1:
    print("Use a special evaluation method.")
    xx_test, yy_test = [], []
    test_size = len(xtest)
    index = -1

    for count in range(0, test_size):
        if xtest[count] in xx_test:
            yy_test[index].append(y_test[count])
        else:
            index += 1
            yy_test.append([])
            yy_test[index].append(y_test[count])
            xx_test.append(xtest[count])
    xtest = xx_test
    y_test = yy_test
else:
    print("Use the usual evaluation method.")

###################################################
#       vector method    &   Naivebayse           #
###################################################
corpus = x_train + xtest
train_size = len(x_train)

cv = CountVectorizer()
wc = cv.fit_transform(corpus)
ttf = TfidfTransformer(use_idf = False, sublinear_tf = True)
tfidf = ttf.fit_transform(wc)

if method == 0:
    print("tfidf method...")
    x_train = tfidf[:train_size,:]
    x_test = tfidf[train_size:,:]
elif method == 1:
    print("Countvector(Bag of word) method...")
    x_train = wc[:train_size, :]
    x_test = wc[train_size:, :]
elif method == 2:
    print("tfidf vector method...")
    tfidf_vect = TfidfVectorizer()
    X_tfidf = tfidf_vect.fit_transform(corpus)
    x_train = X_tfidf[:train_size, :]
    x_test = X_tfidf[train_size:, :]

print("Multinomial Naivebayse use...")
clf = MultinomialNB(alpha=alpha, class_prior=None, fit_prior=True)
clf.fit(x_train, y_train)
predict = clf.predict(x_test)
###################################################
#                  result report                  #
###################################################
log = MakeLog(label)
if evaluation == 1:
    ans_df, data_count, correct = log.evaluation_to_pd(xtest, y_test, predict)
    set_df = log.setdata_evaluation_to_pd(train_path, test_path, data_count, correct, evaluation, method, alpha, dataaugment)
else:
    train_acc = clf.score(x_train, y_train)
    test_acc = clf.score(x_test, y_test)
    print("==================== summury =====================")
    print("train accracy : ", train_acc)
    print("test  accracy : ", test_acc)
    print("===================================================")
    ans_df = log.history_to_pd(xtest, y_test, predict)
    set_df = log.setting_to_pd(train_path, test_path, train_acc, test_acc, evaluation, method, alpha, dataaugment)
log.log_write("result/result_report.xlsx", ans_df, set_df)