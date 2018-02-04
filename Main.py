# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import random
import tqdm
from RL_brain import DuelingDQN
from Env import Env

FLAGS = tf.app.flags.FLAGS
# tf.app.flags.DEFINE_string("param_name", "default_val", "description")
tf.app.flags.DEFINE_bool("pre",True, "use the pre_train model")
tf.app.flags.DEFINE_integer("pre_epoch", 100000, "the epoch of pre_train model")

def pre_train(pre_epoch):
    '''
    由于真实环境游戏太慢样本太少，这里使用模拟游戏环境的方法来进行模型的预训练。
    '''
    #初始化第一个状态值
    print('====================Pre_Train_Start====================')
    state = env.generate_reset_state()
    for i in tqdm.tqdm(range(pre_epoch)):
        action = RL.choose_action(state)
        action_ = (action) * 50 + 300
        state_, reward, done = env.generate_state(action_, state)
        #print(action, state, state_, reward)
        RL.store_transition(state, action, np.float64(reward), state_)

        # 判断是否跳崩了
        if done == True:
            # print(state, reward, done)
            RL.learn()
            state = env.generate_reset_state()
        else:
            state = state_
    print('====================Pre_Train_End====================')
def main(_):
    if FLAGS.pre:
        print('预训练的迭代次数为' + str(FLAGS.pre_epoch))
        pre_train(FLAGS.pre_epoch)
    max_ = 0
    while True:
        state = env.reset()
        tmp = 0
        while True:
            action = RL.choose_action(state)
            # print(action)
            action_ = (action) * 50 + 300
            # action = state * press_coefficient
            state_, reward, done = env.step(action_)
            if not done:
                reward += 0.05 * (tmp + 1)
            RL.store_transition(state, action, np.float64(reward), state_)

            if done == True:
                print('...End...')
                RL.learn()
                env.touch_the_restart()
                break
            tmp +=1
            max_ = max(max_, tmp)
            state = state_
        print('TopJump:', max_, '')

env = Env()
if __name__ == '__main__':
    with tf.Session() as sess:
        with tf.variable_scope('dueling'):
            RL = DuelingDQN(
                n_actions=14, n_features=1, memory_size=5000000,
                e_greedy_increment=0.0001, sess=sess, dueling=True, output_graph=True)
        sess.run(tf.global_variables_initializer())
        tf.app.run()
