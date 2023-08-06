#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program to help Chinses students to learn English.

The original author is HuanFeng Zheng, a student of ZJC, whom the program is named after.

这个程序是帮助我们在平时生活中学习英语的，在平时里我们会通过视频或者阅读碰到各种
生僻的单词，这个程序就是帮助我们查询这个单词，并且帮助我们及时复习掌握单词，程序
有三部分就是查询，复习和退出，当我们选择查询时我们输入单词，程序会在已经有的单词
本中查找。当我们选择复习时，程序会在我们的单词本中随机抽取单词起到及时复习的作用
有利于我学习英语单词。使得自己的英语成绩不断提高

作者：郑焕锋(HuanFeng Zheng)
"""

import pickle
import random
import pathlib

# configuration
PATH = pathlib.Path('mynote.pkl')
DEFAULT_NOTE = {'note': '笔记'}

# business logic
def _query(word):
    """查询单词的意思，如果查不到询问是否存储
    
    Arguments:
        word {str} -- 单词
    """
    if word in note:
        answer = note[word]
        print("单词的中文是：", answer)
    else:
        choice = input("无法找到该单词是否讲此单词加入到单词本中[y/n]：")
        if choice in {"", "y", "Y", "yes", "Yes"}:
            word_meaning = input("请输入单词的中文：")
            note[word] = word_meaning
            print("最新添加的单词单词本为：", note)
            print("添加成功可以复习")

def query():
    name = input("请输入单词：")
    _query(name)

def review():
    # 复习
    print("如果想退出复习直接回车")
    while True:
        word = random.choice(tuple(note.keys()))
        print("请打出单词 %s 的意思：" % word)
        meaning = input("单词的意思是：")
        if meaning == note[word]:
            print("正确！你真棒")
        elif meaning == "":
            break
        else:
            print("再仔细想想, 再给你一次机会")
            meaning = input("单词的意思:")
            if meaning == note[word]:
                print("这次对啦 ^_^ ！")
            elif meaning == "":
                break
            else:
                print("不对哦，单词的意思是：", note[word])

def modify():
    """
    输入修改的单词，和单词意思
    更新note
    询问是否继续修改
    """

    word = input("输入单词:")
    meaning = input("输入单词意思:")
    note[word] = meaning


def run(save=True):
    # 人机交互界面
    print('--进入笔记系统--')
    while True:
        option = input("""
        ==**==
        菜单:
        ------
        1. 查询
        2. 复习
        3. 退出
        4. 修改 （未开通）
        ------
        >>> """)
        if option == "1":
            query()
        elif option == "2":
            review()
        elif option == "3":
            print("谢谢使用!")
            if save:
                print("系统完全退出前笔记会自动保存。")
                with open(PATH, 'wb') as pickle_file:
                    pickle.dump(note, pickle_file)
            break
        elif option == "4":
            modify()
        else:
            print("功能输入错误")
    print('--退出笔记系统--')

# main programming
if PATH.exists():
    with open(PATH, 'b') as pickle_file:
        note = pickle.load(pickle_file)
else:
    note = DEFAULT_NOTE

run()
