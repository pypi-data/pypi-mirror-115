#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Author  : youshu.Ji
import codecs
import os
import json
import pickle
import time
from functools import wraps
# other ----------------------------------------------------------------------
# 统计词频
def calc_word_count(list_word, mode, path='tempcount.txt', sort_id=1, is_reverse=True):
    word_count = {}
    for key in list_word:
        if key not in word_count:
            word_count[key] = 1
        else:
            word_count[key] += 1
    word_dict_sort = sorted(word_count.items(), key=lambda x: x[sort_id], reverse=is_reverse)
    if mode == 'w':
        for key in word_dict_sort:
            writetxt_a(str(key[0]) + '\t' + str(key[1]) + '\n', path)
    elif mode == 'p':
        for key in word_dict_sort:
            print(str(key[0]) + '\t' + str(key[1]))
    elif mode == 'u':
        return word_dict_sort


def dupl_dict(dict_list, key):
    new_dict_list, value_set = [], []
    print('去重中...')
    for i in tqdm(dict_list):
        if i[key] not in value_set:
            new_dict_list.append(i)
            value_set.append(i[key])
    return new_dict_list

CHINESE_PUNCTUATION = list('，。；：‘’“”！？《》「」【】<>（）、')
ENGLISH_PUNCTUATION = list(',.;:\'"!?<>()')


def del_special_char(sentence):
    special_chars = ['\ufeff', '\xa0', '\u3000', '\xa0', '\ue627']
    for i in special_chars:
        sentence = sentence.replace(i, '')
    return sentence


def en_pun_2_zh_pun(sentence):
    # TODO 因为引号的问题，所以我没有写
    for i in ENGLISH_PUNCTUATION:
        pass


# 定义装饰器
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[finished {func_name} in {time:.2f}s]'.format(func_name=function.__name__, time=t1 - t0))
        return result

    return function_timer


def split_sentences(sentences, mode='chinese'):
    # sentences->Str
    # example '12“345。”“6789”'
    if mode == 'chinese':
        split_signs = list('。！？…')
        other_sign = "”"
    elif mode == 'english':
        split_signs = list('.!?')
        other_sign = '"'
    else:
        print('暂时还没有')
        split_signs = list('.!?')
        other_sign = '"'
    splited_sentences = []
    start_idx = 0
    for idx, char in enumerate(sentences):
        if idx == len(sentences) - 1:
            if char in split_signs:
                splited_sentences.append(sentences[start_idx:idx + 1].strip())
                start_idx = idx + 1
            else:
                splited_sentences.append(sentences[start_idx:].strip())
        else:
            if char in split_signs:
                if sentences[idx + 1] == other_sign:
                    if idx < len(sentences) - 2:
                        # 处理。”。
                        if sentences[idx + 2] not in split_signs:
                            splited_sentences.append(sentences[start_idx:idx + 2].strip())
                            start_idx = idx + 2
                elif sentences[idx + 1] not in split_signs:
                    splited_sentences.append(sentences[start_idx:idx + 1].strip())
                    start_idx = idx + 1
    return splited_sentences


def get_substring_loc(text, subtext):
    import re
    res = re.finditer(
        subtext.replace('\\', '\\\\').replace('?', '\?').replace('(', '\(').replace(')', '\)').replace(']',
                                                                                                       '\]').replace(
            '[', '\[').replace('+', '\+'), text)
    l, r = [i for i in res][0].regs[0]
    return l, r


def tf_idf(corpus, save_path):
    from sklearn import feature_extraction
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    import string
    tfidfdict = {}
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        for j in range(len(word)):
            getword = word[j]
            getvalue = weight[i][j]
            if getvalue != 0:  # 去掉值为0的项
                if getword in tfidfdict:  # 更新全局TFIDF值
                    tfidfdict[getword] += float(getvalue)
                else:
                    tfidfdict.update({getword: getvalue})
    sorted_tfidf = sorted(tfidfdict.items(), key=lambda d: d[1], reverse=True)
    to_write = ['{} {}'.format(i[0], i[1]) for i in sorted_tfidf]
    writetxt_w_list(to_write, save_path, num_lf=1)

# 常用函数参考
# import tensorflow as tf
#
# gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)
# sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
# for gpu in tf.config.experimental.list_physical_devices('GPU'):
#     tf.config.experimental.set_memory_growth()
