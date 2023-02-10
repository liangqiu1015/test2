import requests
import json
import pkuseg
from lxml import etree


'''爬虫部分，获取相关文章内容，用来生成词云'''
headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
url = 'https://sa.sogou.com/new-weball/api/sgs/epi-protection/list?type='
type_ = ['jujia','chunyun','waichu','kexue']

def down_text(type_):
    r = requests.get(url=url+type_,headers=headers)
    res = json.loads(r.text)
    for i in res['list']:
        print(i['linkUrl'])
        r = requests.get(url = i['linkUrl'],headers=headers)
        html = etree.HTML(r.text)
        # 获取文章所有文本
        div = html.xpath('//div[@class="word-box ui-article"]//text()')
        string = ''
        for i in div:
            string += i+'\n'
        # 保存文本到note.txt
        with open('note.txt','a',encoding='utf-8') as f:
            f.write(string)
def down_all():
    for i in type_:
        down_text(i)

'''分词统计部分，用pkuseg对下载的文本进行分词并统计词频'''
def word_count():
    with open('note.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    # 自定义词典，意味着分词时会专门保留出这些词
    user_dict = ['冠状病毒']
    # 以默认配置加载模型
    seg = pkuseg.pkuseg(user_dict=user_dict)
    # 进行分词
    text = seg.cut(text)
    # 读取停用词表
    with open('stop_word.txt', 'r', encoding='utf-8') as f:
        s_word = f.readlines()
    # 停用词表一个停用词占一行，因为这样读readlines()会带上换行符在每个词后面
    # 使用map对列表所有词去掉空字符
    s_word = list(map(lambda x: x.strip(), s_word))
    count = {}
    # 统计词频
    for word in text:
        # 当这个词不在停用词表中并且长度不为1才统计
        if word in s_word or len(word) == 1:
            continue
        else:
            if word in count:
                # 已经记录过，加1
                count[word] += 1
            else:
                # 否则将该词添加到字典中
                count[word] = 1
    all_pair = []
    # 将统计的字典转换为pyecharts词云要求的输入
    # 比如这样：words = [("Sam S Club", 10000),("Macys", 6181)]，前面是词，后面是词频
    for pair in count:
        all_pair.append((pair, count[pair]))
    # 对结果排序
    li = sorted(all_pair, key=lambda x: x[1], reverse=True)
    # 将列表转str直接写入文件中，到时直接给pyecharts用
    # 不要每次都分词，分词过程有点慢
    with open('word_count.txt','w',encoding='utf-8') as f:
        f.write(str(li))
if __name__ == '__main__':
    down_all()
    word_count()