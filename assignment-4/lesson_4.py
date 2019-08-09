#步骤1：解析XML文件
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os.path
import sys
from gensim.corpora import WikiCorpus

if __name__ == '__main__':

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
    # check and process input arguments
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    space = ' '
    i = 0
    output = open(outp, 'w', encoding='utf-8')
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        s = space.join(text) + "\n"
        output.write(s)
        i = i + 1
        if (i % 10000 == 0):
            logger.info("Saved " + str(i) + " articles")
    output.close()
    logger.info("Finished Saved " + str(i) + " articles")
#执行命令： python process.py zhwiki-20190720-pages-articles-multistream.xml.bz2  wiki.zh.text





#步骤2：使用opencc实现繁体转简体
#执行命令：opencc -i wiki.zh.text -o wiki.zh.jian.txt -c t2s.json






#步骤3：jieba分词
import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs,sys
import re

def token(string):
    r1 = "[a-zA-Z\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、：；;《》“”~@#￥%……&*（）ʔ]+"
    clean_string = re.sub(r1, '', string)
    return clean_string

f=codecs.open('wiki.zh.jian.txt','r',encoding="utf8")
target = codecs.open("wiki.zh.jian.seg.txt", 'w',encoding="utf8")
line_num=1

line = f.readline()
while line:
    print('---- processing ', line_num, ' article----------------')

    line = ''.join(token(str(line)))

    line_seg = " ".join(jieba.cut(line))
    target.writelines(line_seg)
    line_num = line_num + 1
    line = f.readline()

f.close()
target.close()
#执行命令：python jieba.py






#步骤4：Word2vec模型训练
import logging
import os.path
import sys
import multiprocessing
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

if __name__ == '__main__':

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
    # check and process input arguments
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, outp1, outp2 = sys.argv[1:4]
    model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=5, workers=multiprocessing.cpu_count())
    model.save(outp1)
    model.model.wv.save_word2vec_format(outp2, binary=False)


#执行命令： python word2vec_model.py  wiki.zh.jian.seg.txt  wiki.zh.text.model  wiki.zh.text.vector






#步骤5：测试模型
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],xy=(x[i], y[i]),xytext=(5, 2),textcoords='offset points',ha='right',va='bottom')
    plt.show()

en_wiki_word2vec_model = Word2Vec.load('wiki.zh.text.model')

tsne_plot(en_wiki_word2vec_model)


testwords = ['苹果','数学','学术','白痴','篮球']
for i in range(5):
    res = en_wiki_word2vec_model.most_similar(testwords[i])
    print (testwords[i])
    print (res)

# 苹果
# [('apple', 0.5410169363021851), ('苹果公司', 0.4918888807296753), ('咬一口', 0.4741284251213074), ('洋葱', 0.4696866571903229), ('冰淇淋', 0.4614587426185608), ('苹果电脑', 0.45998817682266235), ('黑莓', 0.4557930827140808), ('水果', 0.4546721577644348), ('iphone', 0.44593721628189087), ('草莓', 0.4437388479709625)]
# 数学
# [('微积分', 0.7083343267440796), ('算术', 0.6934097409248352), ('数学分析', 0.663016140460968), ('概率论', 0.6389687061309814), ('数论', 0.6296793222427368), ('逻辑学', 0.6191371083259583), ('几何学', 0.60764479637146), ('数理逻辑', 0.5989662408828735), ('物理', 0.5965093970298767), ('高等数学', 0.5895018577575684)]
# 学术
# [('学术研究', 0.7319201231002808), ('汉学', 0.5988526344299316), ('学术活动', 0.5887891054153442), ('科学研究', 0.5864561796188354), ('学术界', 0.5863242149353027), ('教学研究', 0.5767545700073242), ('教研', 0.5732147097587585), ('学术交流', 0.561274528503418), ('科研', 0.5595779418945312), ('医学教育', 0.5571168661117554)]
# 白痴
# [('疯子', 0.5986206531524658), ('书呆子', 0.5612877607345581), ('骗子', 0.538498044013977), ('怪胎', 0.5305827856063843), ('爱哭鬼', 0.5293511152267456), ('傻子', 0.5216787457466125), ('自恋', 0.5185167789459229), ('变态', 0.5165976285934448), ('自以为是', 0.516464114189148), ('蠢', 0.5106762051582336)]
# 篮球
# [('美式足球', 0.633753776550293), ('橄榄球', 0.6222437620162964), ('排球', 0.5964736938476562), ('棒球', 0.5949814319610596), ('男子篮球', 0.5927262306213379), ('冰球', 0.591292142868042), ('篮球员', 0.5610231161117554), ('篮球运动', 0.5576823353767395), ('足球', 0.5409365892410278), ('橄榄球队', 0.5348620414733887)]