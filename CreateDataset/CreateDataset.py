from gensim.models.word2vec import Word2Vec

from Morphological.Morphological_analysis import Morphological_analysis

from googletrans import Translator
from time import sleep
import sys

import csv
import pandas as pd

class CreateDataset:
    def __init__(self):
        pass

    def createdataset(self, train_path, test_path):
        df_train = pd.read_csv(train_path, header=None, encoding="utf-8")
        df_test = pd.read_csv(test_path, header=None, encoding="utf-8")
        x_train_list, y_train_list = [], []
        x_test_list, y_test_list = [], []
        x_train, y_train = [], []
        x_test, y_test = [], []

        x_train_list = df_train.iloc[:,0].values.tolist()
        y_train_list = df_train.iloc[:,1].values.tolist()
        x_test_list = df_test.iloc[:,0].values.tolist()
        y_test_list = df_test.iloc[:,1].values.tolist()

        for x, y in zip(x_train_list, y_train_list):
            x_train.append(str(x))
            if "" in y:
                y_train.append(0)
            elif "" in y:
                y_train.append(1)
            else:
                print("Some data should not exist")
                exit(1)

        for x, y in zip(x_test_list, y_test_list):
            x_test.append(str(x))
            if "" in y:
                y_test.append(0)
            elif "" in y:
                y_test.append(1)
            else:
                print("Some data should not exist")
                exit(1)

        print("=======================Dataset Summury============================")
        print("x_train : ", len(x_train))
        print("x_train => ", x_train[0])
        print("x_test  : ", len(x_test))
        print("x_test  => ", x_test[0])
        print("==================================================================")

        return x_train, x_test, y_train, y_test

    def create_data(self, train_path):
        x_train_list, y_train_list = [], []
        x_train, y_train = [], []

        df_train = pd.read_csv(train_path, header=None, encoding="utf-8")
        
        x_train_list = df_train.iloc[:,0].values.tolist()
        y_train_list = df_train.iloc[:,1].values.tolist()

        for x, y in zip(x_train_list, y_train_list):
            x_train.append(str(x))
            if "" in y:
                y_train.append(0)
            elif "" in y:
                y_train.append(1)
            else:
                print("Some data should not exist")
                exit(1)
        return x_train, y_train

    def data_augment_use_word2vec(self, model, train_path, test_path):
        print("word2vec dataaugment...")

        x_train , y_train = [], []
        load_count = 0
        exception_vocab = 0
        morphological = Morphological_analysis()

        x_data, y_data = self.create_data(train_path)
        x_test, y_test = self.create_data(test_path)

        x_data = morphological.train_morphological(x_data)

        sys.stdout.flush()
        print("=======================Before  Dataset============================")
        print("x_train : ", len(x_data))
        print("x_train => ", x_data[0])
        print("x_test  : ", len(x_test))
        print("x_test  => ", x_test[0])
        print("==================================================================")

        """for x, y in zip(x_data, y_data):
            print("\r" + "load data :" + str(load_count), end="")
            sys.stdout.flush()
            x_train.append(morphological.basic_to_result(x))
            y_train.append(y)"""

        for x, y in zip(x_data, y_data):
            print(x)
            x_train.append(morphological.basic_to_result(x))
            y_train.append(y)
            buff = []
            for count, text in enumerate(x):
                try:
                    r = model.most_similar(positive=[text])
                    buff.append(r[0][0])
                except :
                    exception_vocab += 1
                    pass
            print(buff)
            x_train.append(buff)
            y_train.append(buff)

        print("\n")
        print("data augment complete!")
        print("=======================Dataset Summury============================")
        print("x_train : ", len(x_train))
        print("x_train => ", x_train[0])
        print("x_test  : ", len(x_test))
        print("x_test  => ", x_test[0])
        print("exception vocabrary :",exception_vocab)
        print("==================================================================")

        return x_train, x_test, y_train, y_test
        
    ###########################################
    #     stop working method... not using.   #
    ###########################################
    def data_augment_use_googletrans(self, x_data, y_data):
        translator = Translator()
        trans_eng = []
        csv_write = []

        print("data augment function start...")
        print("=======================Before Dataset===========================")
        print("training data : ", len(x_data))
        print("example  data : ", x_data[0])
        print("exsample label: ", y_data[0])
        print("================================================================")
        
        print("data translate.(augment executed)..")
        sleep(2)
        count = 0
        for text, label in zip(x_data, y_data):
            csv_write.append([text, label])
            try:
                trans_eng.append(translator.translate(text, src="ja", dest="en").text)
                if(count % 5 == 0):
                    print("English data sample :", trans_eng[count])
                sleep(2)
                count += 1
            except Exception as e:
                print(e)
                exit(1)

        sleep(1.5)
        print("translate japanese to english. retanslate...")

        count = len(csv_write) - 1
        for text, label in zip(trans_eng, y_data):
            try:
                csv_write.append([translator.translate(text, src="en", dest="ja").text, label])
                if(count % 5 == 0):
                    print("result data sample :", csv_write[count])
                sleep(2)
                count += 1
            except Exception as e:
                print(e)
                exit(1)
        
        print("=======================Befor Summury============================")
        print("training data : ", len(x_data))
        print("example  data : ", x_data[0])
        print("exsample label: ", y_data[0])
        print("================================================================")

        print("save sumury data...")

        with open('./train_augmentdata.csv', 'w',"utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_write)
