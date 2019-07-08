import numpy as np
import random
import pandas as pd
import re
import jieba
from collections import Counter


sentence_1 = """
sentence_1 = 人称 时间 地点 动作  
人称 = 小孩 |大妈 |美女| 帅哥  
时间 = 前天 |昨天| 今天| 明天| 后天
地点 = 在商场 |在广场 |在游戏厅| 在酒吧
动作 = 购物 |跳广场舞 |喝酒 |打游戏
"""

sentence_2 = """
sentence_2 = 人称 动词 形容词 名词  
人称 = 你| 我 |他| 她  
动词 = 穿了| 想吃 |想玩| 学习 
形容词 = 美美的 |漂亮的 |高级的 |酷炫的
名词 = 一件上衣| 大餐| Python编程知识 |电脑游戏
"""

def creat_grammer(grammar_str,split= '= '):
    grammar = {}
    for line in grammar_str.split('\n'):
        if not line.strip(): continue

        exp , stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split('|') ]
    return grammar


def generate(gram, target):
    if target not in gram:
        return target
    expaned = [generate(gram, t) for t in random.choice(gram[target])]
    return ''.join([e if e != '/n' else '\n' for e in expaned if e != 'null'])


def generate_n():
    for i in range(10):
        print(generate(gram=creat_grammer(grammar_str=sentence_2), target='sentence_2'))

#语料太少所以没有用
# articles = []
# for line in open("train.txt","r"):
#     articles.append(line)
#
#
# def token(string):
#     return re.findall(r'[\u4e00-\u9fff]',string)
# articles_clean = [''.join(token(str(a))) for a in articles ]
#
#
# TOKENS = []
# def cut(string):
#     return list(jieba.cut(string))
# for line in articles_clean:
#     TOKENS+=cut(line)


filename= 'sqlResult_1558435.csv'
content = pd.read_csv(filename,encoding= 'gb18030')
articles = content['content'].tolist()

def token(string):
    return re.findall('\w+',string)

articles_clean = [''.join(token(str(a))) for a in articles ]

with open('articles_9k.txt','w') as f :
    for a in articles_clean:
        # f.write(a)
        f.write(a+'\n')




TOKENS = []
def cut(string):
    return list(jieba.cut(string))
for i, line in enumerate(open('articles_9k.txt')):
    if i%5000 == 0:
        print(i)
    if i>30000:#89611
        break
    TOKENS+=cut(line)


def prob_1(word):
    if word in TOKENS:
        return Counter(TOKENS)[word] / len(TOKENS)
    else:
        return 1 / len(TOKENS)



TOKENS = [ str(t) for t in TOKENS]
TOKENS_2_GRAM = [''.join(TOKENS[i:i+2]) for i in range(len(TOKENS[:-2]))]
def prob_2(word1,word2):
    if word1 + word2 in TOKENS_2_GRAM:
        return Counter(TOKENS_2_GRAM)[word1+word2] / len(TOKENS_2_GRAM)
    else:
        return 1 / len(TOKENS_2_GRAM)


def get_probablity(sentence):
    words = cut(sentence)
    sentence_prob = 1
    for i, word in enumerate(words[:-1]):
        next = words[i+1]
        probability = prob_2(word, next) / prob_1(word)
        sentence_prob *= probability
    return sentence_prob


Final = []
def generate_best():
    for i in range(5):
        random_sentence = generate(gram=creat_grammer(grammar_str=sentence_1), target='sentence_1')
        P = get_probablity(random_sentence)
        Final.append((random_sentence,P))
    return sorted(Final, key=lambda x: x[1], reverse=True)

Rank = generate_best()
print('The result of Rank is:',Rank)
print('The best sentence is :',Rank[0])

#运行结果
#The result of Rank is: [('美女前天在游戏厅打游戏', 9.86395935174127e-09), ('帅哥今天在广场打游戏', 5.459916991080328e-10), ('小孩前天在酒吧购物', 8.274932465290547e-11), ('美女今天在广场购物', 4.747753905287242e-11), ('帅哥后天在酒吧跳广场舞', 2.9566099570556155e-11)]
#The best sentence is : ('美女前天在游戏厅打游戏', 9.86395935174127e-09)

