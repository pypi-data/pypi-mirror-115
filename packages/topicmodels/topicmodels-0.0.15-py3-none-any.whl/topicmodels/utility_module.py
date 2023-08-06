from topicmodels.topic_modelling_trans import topicmodelingtransformer
from topicmodels.topic_modelling_lstm import topicmodelinglstm
from topicmodels.topic_modelling_nn import topicmodelingnn
from transformers import TFAutoModelWithLMHead, AutoTokenizer
import keras
from tensorflow.keras.callbacks import LambdaCallback
import topicmodels.eval_measure
from topicmodels.corpus import DocData, DocDatalstm
import topicmodels.ldann
from topicmodels.ldann import Doc2Topic, Logger, data_feeder, Doc2Topiclstm
from topicmodels.eval_measure import custom_evaluator
import os
import collections
import numpy as np
import random
import json
import pandas as pd
import fasttext
from scipy import spatial
import traceback

# modelweights_path = "fasttext10.bin"
# wordmodel = fasttext.load_model(modelweights_path)
# fastdict = wordmodel.get_words()
# t5
model = TFAutoModelWithLMHead.from_pretrained("t5-base")
tokenizer = AutoTokenizer.from_pretrained("t5-base")


def topicmodelling(datafile, epochs=1, no_topic=10, topic_word=5, model_type='NN', column_name='clean_text'):
    try:
        if model_type == 'NN':
            print("topic modelling NN ")
            topics, score = topicmodelingnn(
                datafile, epochs, no_topic, topic_word, column_name=column_name)
        elif model_type == 'LSTM':
            print("topic modelling LSTM")
            topics, score = topicmodelinglstm(
                datafile, epochs, no_topic, topic_word, column_name=column_name)
        elif model_type == 'TRANS':
            print("topic modelling Transformer")
            topics, score = topicmodelingtransformer(
                datafile, no_topic=10, topic_word=5, column_name=column_name)
        topics.to_csv('predicted_topic.csv')
        for i in range(len(topics)):
            print(topics.iloc[i]['topic'])
        print("prediction score : ", score)
        return topics, score
    except:
        print("Exception occurred.")
        traceback.print_exc()
        print("please check the following")
        print('please enter valid column name ')

        print('please select \'NN\' for neural network model')
        print('please select \'LSTM\' for lstm model')
        print('please select \'TRANS\' for transformer model')
