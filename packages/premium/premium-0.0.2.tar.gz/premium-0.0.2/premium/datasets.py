#!/usr/bin/env python

import os

import codefast as cf
import numpy as np

stopwords = {
    'en':
    cf.file.read(
        os.path.join(cf.file.dirname() + '/localdata/en_stopwords.txt'))
}


class Urls:
    prefix = 'https://filedn.com/lCdtpv3siVybVynPcgXgnPm/corpus'


def _load(fpath: str) -> None:
    cf.info(f'Downloading {fpath}')
    online_url = os.path.join(Urls.prefix, fpath)
    dest = f'/tmp/{io.basename(fpath)}'
    if io.exists(dest):
        if input('File already existed, press [y] to overwrite: ') != 'y':
            return
    cf.net.download(online_url, dest)


class Glove:
    dim2file = {
        50: 'glove.6B.50d.txt',
        100: 'glove.6B.100d.txt',
        200: 'glove.6B.200d.txt',
        300: 'glove.6B.300d.txt',
    }

    @classmethod
    def load(cls, dimention: int = 50):
        _file = cls.dim2file[dimention]
        _file = f'/tmp/{_file}'
        embeddings_dict = {}
        if not io.exists(_file):
            cf.info(f'{_file} not exist')
        else:
            for line in io.iter(_file):
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], "float32")
                embeddings_dict[word] = vector
        return embeddings_dict


class Downloader:
    def douban_movie_review(self):
        '''Kaggle dataset https://www.kaggle.com/liujt14/dou-ban-movie-short-comments-10377movies'''
        cf.info(
            'Downloading douban movie review data: https://www.kaggle.com/liujt14/dou-ban-movie-short-comments-10377movies',
        )
        _load('douban_movie_review.zip')

    def douban_movie_review_2(self):
        _load('douban_movie_review2.csv.zip')

    def chinese_mnist(self):
        '''https://www.kaggle.com/fedesoriano/chinese-mnist-digit-recognizer'''
        _load('Chinese_MNIST.csv.zip')

    def toxic_comments(self):
        _load('toxic_comments.csv')

    def glove_50d(self):
        _load('pretrained/glove.6B.50d.txt')

    def glove_100d(self):
        _load('pretrained/glove.6B.100d.txt')

    def glove_200d(self):
        _load('pretrained/glove.6B.200d.txt')

    def glove_300d(self):
        _load('pretrained/glove.6B.300d.txt')


def load_icwb():
    '''Data source: http://sighan.cs.uchicago.edu/bakeoff2005/
    '''
    _load('icwb2-data.zip')


def load_news2016():
    ''' 中文新闻 3.6 GB 2016年语料 
    '''
    _load('news2016.zip')


def load_msr_training():
    _load('msr_training.utf8')


def load_realty():
    import getpass
    cf.info("Download real estate dataset realty.csv")
    _load('realty.zip')
    passphrase = getpass.getpass('Type in your password: ').rstrip()
    cf.utils.shell(f'unzip -o -P {passphrase} /tmp/realty.zip -d /tmp/')


def load_spam(path: str = '/tmp/'):
    cf.info(f'Downloading English spam ham dataset to {path}')
    online_url = os.path.join(Urls.prefix, 'spam-ham.txt')
    local_path = path + 'spam-ham.txt'
    cf.net.download(online_url, local_path)


def load_spam_cn(path: str = '/tmp/'):
    cf.info(f'Downloading Chinese spam ham dataset to {path}')
    zipped_data = os.path.join(Urls.prefix, 'spam_cn.zip')
    label_file = os.path.join(Urls.prefix, 'spam_cn.json')
    cf.net.download(zipped_data, '/tmp/tmp_spam.zip')
    cf.utils.shell('unzip -o /tmp/tmp_spam.zip -d /tmp/')
    cf.net.download(label_file, '/tmp/spam_cn.json')
