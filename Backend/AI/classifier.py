import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import SimpleRNN, Embedding, Dense
from tensorflow.keras.models import Sequential
import pickle
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def createModel():
    data = pd.read_csv(basedir + '/data.csv',encoding='utf-8')

    print('총 샘플의 수 :',len(data))
    data.info()

    # null값이 들어있는지 확인
    print(data.isnull().values.any())

    # content 열에서 중복인 내용이 있다면 중복 제거
    data.drop_duplicates(subset=['content'], inplace=True) 

    print('총 샘플의 수 :',len(data))

    # 홍보글과 일반글 비율 시각화
    print(data.groupby('label').size().reset_index(name='count'))

    # 데이터를 x와y로 분리
    X_data = data['content']
    y_data = data['label']

    print('판매 글의 개수: {}'.format(len(X_data)))
    print('레이블의 개수: {}'.format(len(y_data)))

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_data) # 5169개의 행을 가진 X의 각 행에 토큰화를 수행
    sequences = tokenizer.texts_to_sequences(X_data) # 단어를 숫자값, 인덱스로 변환하여 저장

    # print(sequences[:5])

    word_to_index = tokenizer.word_index
    # print(word_to_index)


    # tokenizer 저장
    with open(basedir + '/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)


    threshold = 2
    total_cnt = len(word_to_index) # 단어의 수
    rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

    # # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    # for key, value in tokenizer.word_counts.items():
    #     total_freq = total_freq + value

    #     # 단어의 등장 빈도수가 threshold보다 작으면
    #     if(value < threshold):
    #         rare_cnt = rare_cnt + 1
    #         rare_freq = rare_freq + value

    # print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
    # print("단어 집합(vocabulary)에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
    # print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)


    vocab_size = len(word_to_index) + 1
    # print('단어 집합의 크기: {}'.format((vocab_size)))

    X_data = sequences

    # print('메일의 최대 길이 : %d' % max(len(l) for l in X_data))
    # print('메일의 평균 길이 : %f' % (sum(map(len, X_data))/len(X_data)))
    # plt.hist([len(s) for s in X_data], bins=50)
    # plt.xlabel('length of samples')
    # plt.ylabel('number of samples')
    # plt.show()

    max_len = 16899
    # 전체 데이터셋의 길이는 max_len으로 맞춤
    data = pad_sequences(X_data, maxlen = max_len)
    print("훈련 데이터의 크기(shape): ", data.shape)

    # 데이터 분할
    n_of_train = int(len(sequences) * 0.8)
    n_of_test = int(len(sequences) - n_of_train)
    # print('훈련 데이터의 개수 :',n_of_train)
    # print('테스트 데이터의 개수:',n_of_test)

    X_test = data[n_of_train:] 
    y_test = np.array(y_data[n_of_train:]) 
    X_train = data[:n_of_train]
    y_train = np.array(y_data[:n_of_train])

    # checkpoint_path = "./checkpoints/train"
    # ckpt = tf.train.Checkpoint(encoder=encoder,
    #                            decoder=decoder,
    #                            optimizer = optimizer)
    # ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)

    # start_epoch = 0
    # if ckpt_manager.latest_checkpoint:
    #   start_epoch = int(ckpt_manager.latest_checkpoint.split('-')[-1])
    #   # restoring the latest checkpoint in checkpoint_path
    #   ckpt.restore(ckpt_manager.latest_checkpoint)


    # 모델 생성
    model = Sequential()
    model.add(Embedding(vocab_size, 32)) # 임베딩 벡터의 차원은 32
    model.add(SimpleRNN(32)) # RNN 셀의 hidden_size는 32
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=3, batch_size=64, validation_split=0.2)

    print("\n 테스트 정확도: %.4f" % (model.evaluate(X_test, y_test)[1]))

    model.save(basedir + '/my_model.h5')

    # epochs = range(1, len(history.history['acc']) + 1)
    # plt.plot(epochs, history.history['loss'])
    # plt.plot(epochs, history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'val'], loc='upper left')
    # plt.show()
