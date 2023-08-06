#!/usr/bin/env python
import abc
from abc import abstractmethod
from operator import methodcaller

import codefast as cf
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

import premium as pm
from premium.measure import metrics
from premium.preprocess import any_cn, jb_cut


class BaseModel(metaclass=abc.ABCMeta):
    def __init__(self, X, y, test_size: float = 0.2):
        self.X = jb_cut(X) if any_cn(X) else X
        self.y = y
        self.test_size = test_size

    @abc.abstractmethod
    def preprocess(self):
        ...


class SVM(BaseModel):
    def __init__(self, X, y, test_size: float = 0.2):
        super(SVM, self).__init__(X, y, test_size)

    def preprocess(self):
        cv = CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b')
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, random_state=63, test_size=self.test_size)

        X_train = cv.fit_transform(X_train)
        X_test = cv.transform(X_test)
        cf.js.write(cv.vocabulary_, cf.io.tmpfile('cv', 'json'))
        return X_train, X_test, y_train, y_test

    def run(self):
        X_train, X_test, y_train, y_test = self.preprocess()
        clf = SVC(kernel='rbf', C=10, gamma='auto', random_state=63)
        clf.fit(X_train, y_train)
        cf.info('Train completes.')

        y_pred = clf.predict(X_test)
        metrics(y_test, y_pred)

        model_name = cf.io.tmpfile('svm', 'joblib')
        cf.info('saving model to {}'.format(model_name))
        joblib.dump(clf, model_name)
        cf.info('SVM.run() completes.')


def bayes(X: list, y: list, is_cn: bool = False):
    if is_cn:
        import jieba
        X = [' '.join(jieba.lcut(e)) for e in X]

    cv = CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b')
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        random_state=42,
                                                        test_size=0.2)
    X_train = cv.fit_transform(X_train)
    X_test = cv.transform(X_test)
    nb = MultinomialNB()
    nb.fit(X_train, y_train)
    y_pred = nb.predict(X_test)

    metrics(y_test, y_pred)
