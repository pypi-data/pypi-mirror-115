import pickle
from typing import Any, List

import codefast as cf
import jieba
import numpy as np
from numpy.lib.arraypad import pad


class Pickle:
    def read(self, pickle_file: str):
        return pickle.load(open(pickle_file, 'rb'))

    def write(self, contents, pickle_file: str):
        with open(pickle_file, 'wb') as f:
            pickle.dump(contents, f)


def jb_cut(X) -> List[Any]:
    if isinstance(X, str):
        return ' '.join(jieba.lcut(X))
    return [' '.join(jieba.lcut(_)) for _ in X]


def any_cn(X) -> bool:
    '''Decides any Chinese char was contained'''
    if isinstance(X, str):
        X = [X]
    return any(cf.nstr(s).is_cn() for s in X)


def datainfo(sequences: list) -> None:
    len_list = list(map(len, sequences))

    def percentile(n: int):
        return int(np.percentile(len_list, n))

    print('{:<30} {}'.format('Size of sequence:', len(sequences)))
    print('{:<30} {}'.format('Maximum length:', max(len_list)))
    print('{:<30} {}'.format('Minimum length:', min(len_list)))
    print('{:<30} {}'.format('Percentile 90 :', percentile(90)))
    print('{:<30} {}'.format('Percentile 80 :', percentile(80)))
    print('{:<30} {}'.format('Percentile 20 :', percentile(20)))
    print('{:<30} {}'.format('Percentile 10 :', percentile(10)))

    if any_cn(sequences):
        import jieba
        sequences = [jieba.lcut(s) for s in sequences]
    _, tokenizer = tokenize(sequences)
    print('unique words count {}'.format(len(tokenizer.word_index)))


def gpu_check():
    import tensorflow as tf
    tf.Session(config=tf.ConfigProto(
        log_device_placement=True)).run(tf.constant(1) + tf.constant(1))


def tokenize(X: list, max_feature: int = 10000) -> list:
    cf.info(f'Tokenizing texts')
    from tensorflow.keras.preprocessing.text import Tokenizer
    tok = Tokenizer(num_words=max_feature)
    tok.fit_on_texts(X)
    ans = tok.texts_to_sequences(X)
    return ans, tok


def label_encode(y: list, return_processor: bool = False) -> np.ndarray:
    '''Encode labels into 0, 1, 2...'''
    cf.info(
        f'Getting binary labels. Return encoder is set to {return_processor}')
    from sklearn.preprocessing import LabelEncoder
    enc = LabelEncoder()
    y_categories = enc.fit_transform(y)
    return (y_categories, enc) if return_processor else y_categories


def onehot_encode(y: list, return_processor: bool = False) -> np.ndarray:
    '''input format: y =[['red'], ['green'], ['blue']]
    '''
    cf.info(
        f'Getting one hot encode labels. Return encoder is set to {return_processor}'
    )
    assert isinstance(y[0], list) or isinstance(y[0], np.ndarray)
    from sklearn.preprocessing import OneHotEncoder
    enc = OneHotEncoder()
    y_categories = enc.fit_transform(y)
    return (y_categories, enc) if return_processor else y_categories


def pad_sequences(sequences, **kwargs):
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    seq = pad_sequences(sequences, **kwargs)
    return seq


pkl = Pickle()
