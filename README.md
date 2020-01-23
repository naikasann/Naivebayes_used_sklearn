# ---naivebayes program---

ナイーブベイズ分類器の学習のために作成したプログラム。

## システム概要

ナイーブベイズ分類器をpythonのパッケージskleanを利用して作成する。

## ファイル構成

* /CreateDataset --- 作成したcsvファイルを読み取りデータセットを作成するclass。
* /dataset(ignore) --- 学習用のデータセットと、テストのデータセットを入れておく。
* /Morphological --- データを読み取り形態素解析を行うclass。
* /result(ignore) --- classification_reportなどの実行結果ログを保存する場所
* /setting --- pipのrequire.txtを入れてある。バージョン管理用テキストファイル
* /word2vec_model(ignore) --- word2vecの学習済みモデルが格納されている
* .gitignore     --- gitignoreファイル
* *data_augment.py(現在動きません)* --- googletransのデータ拡張用のファイル。
* *naivebayse.py* --- 実行のメインファイル。これを実行することでナイーブベイズが行われる。
* README.mb     --- readmeファイル

---------------------------------------------------
* **gitignoreしたもの**
 * /detaset

train用とtest用のcsvファイルとtrainを拡張したときに生成されるcsvファイル。
これは
` 文章　| 分類 `
が連続してなるcsvで文章をデータ、分類を答えとして学習を行うようになっている。

 * result/result_report.xlsx

testdataをpredictしてどれだけの精度なのか確かめるためのエクセルファイル。

* /word2vec_model

word2vecのモデルが格納されているフォルダ
モデルは　[東北大学のモデル](http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/)を利用させていただいています。

---------------------------------------------------
## 実行方法

Pythonファイルのnaivebayse.pyがあるディレクトリで

`python naivebayse,py`

を実行することでプログラムが動作する。

---------------------------------------------------
## 処理の手順

1. まずデータセットを呼び出す。
2. 形態素解析を行う。(mecab-ipadic-NEologdを利用した)
3. tfidf, Bag Of word, tfidfvectorの中から選択したもので数値に変換する。
4. skleanのMultinomialNBにかける。
5. predictを行って、結果からログをエクセル形式で作成する

---------------------------------------------------
## データ拡張について

### `googleの翻訳機能を利用したデータ拡張(不要と言われたので現在使用不可)`

ナイーブベイズ分類器に対してデータがあまりに少ないため。(項目による偏りもあるが今回は考慮しない。)
データ拡張を行う必要があると判断した。
データの拡張方法は

1. train用のデータに対してGoogletranseを用いて英語に変換を行う。
2. 英語に訳した文章に対して日本語に再翻訳をかける。
3. そのデータをtrainのデータに連結し、学習を行う。

この拡張方法は単純な文章には重複する分が生成される恐れがあるため、有用ではないが複雑な文章に対しては再翻訳をかけることで似たような文章だが違った単語などが出現し、汎化性が高まるのではないのかと考えられる。

しかし、GoogleTransはHTTP POSTでデータのやり取りを行うため、大量なデータを行う際にはディレイをかけて通信を連続的に行わないように気をつける必要がある。

※　この拡張方法は有用であると考えたが不要と言われたので現在使用することができない。気が向けば復活し、作成するかもしれないがおそらくデータセットが今年度でなくなるので作成することはおそらくない。

### `word2vecを利用したデータ拡張`

上気した通りデータ数が少ないため、データ拡張を行う。
こっちの方法はword2vecを利用して

1. 一つの文章を形態素解析する。
2. 形態素解析した結果の品詞一つをword2vecにかけ類似した単語(文や人の場合もある)を出力する。
3. 類似した単語を連結し、データ拡張に追加。
4. 学習を行う。

---------------------------------------------------
## Mecabの辞書について

Mecabの単語辞書は初期に格納されているものでは形態素解析すると正しくできないものがある。
それは、芸能人などの固有名詞である。
これを形態素解析すると、臨んだような形態素解析にならない。

そこで、Mecabの辞書データを変更することにした。
芸能人もある程度抑えることができる、[mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)を利用する。
これでMecabで対応できない形態素解析がある程度減少するはず

---------------------------------------------------
## 評価方法について

ナイーブベイズ分類器にかけた際に、accuracyがあまり上がらないという現象が発生した。
これはカテゴリーを分ける際に複数のカテゴリーをまたいでいるデータが多数あったため起きた問題だということがわかった。
そこで複数のカテゴリーにまたいだものはその中からどれか一つでも判別することができていた場合、accuracyに数値を与えることにする。

ただこの評価法は適切ではない部分があるため選択肢として与えることとした。実行するときに選択できるものとする。

(まあ数値が低かったので救済的な部分が大きい。カテゴリーのつけ方を変えたほうがいいとは思う…時間ないからできない…)

---------------------------------------------------
## 開発環境
* Python --- ver3.7.3
* MeCab --- ver0.996
    * mecab-ipadic-NEologd --- 2019/12/17に辞書データをダウンロード
* windows10
* Windows Subsystem for Linux(Ubuntu)
    * DISTRIB_ID=Ubuntu
    * DISTRIB_RELEASE=18.04
    * DISTRIB_CODENAME=bionic
    * DISTRIB_DESCRIPTION="Ubuntu 18.04.1 LTS"

## 検討すべき点
* 評価方法の計算方法をどうするのか。
* カテゴリー間どうする。(カテゴリーをまたいだデータについて)

---------------------------------------------------

### 参考文献
1. [【Python】自然言語処理で使われるTF-IDFと単純ベイズ分類器(Naive Bayes)について使いながら解説する - Qiita](https://qiita.com/tomone_hata/items/67e7f9415dbf5c8ff8ba)
2. [sklearn.metrics.classification_report — scikit-learn 0.21.3 documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)
3. [pythonによる日本語前処理備忘録 | ブログ一覧 | DATUM STUDIO株式会社](https://datumstudio.jp/blog/python%E3%81%AB%E3%82%88%E3%82%8B%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%89%8D%E5%87%A6%E7%90%86%E5%82%99%E5%BF%98%E9%8C%B2)
4. [機械学習の勉強歴が半年の初心者が、 Kaggle で銅メダルを取得した話 | 株式会社トップゲート](https://www.topgate.co.jp/kaggle-bronze-report-jigsaw)
5. [Python – googletransを試してみました。 ｜ Developers.IO](https://dev.classmethod.jp/beginners/python-py-googletrans/)
6. [MeCab: Yet Another Part-of-Speech and Morphological Analyzer](https://taku910.github.io/mecab/)
7. [Word2Vec学習済モデルとgensimで「世界」－「知性」＝を計算したら「日本」になった（笑） - "BOKU"のITな日常](https://arakan-pgm-ai.hatenablog.com/entry/2019/02/08/090000)
8. [neologd/mecab-ipadic-neologd: Neologism dictionary based on the language resources on the Web for mecab-ipadic](https://github.com/neologd/mecab-ipadic-neologd)
9. [mecab-ipadic-NEologdをWindowsで使ってみる。 - どん底から這い上がるまでの記録](https://www.pytry3g.com/entry/MeCab-NEologd-Windows)
10. [日本語 Wikipedia エンティティベクトル](http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/)