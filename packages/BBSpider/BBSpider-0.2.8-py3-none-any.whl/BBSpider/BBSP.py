import requests  # 处理HTTP请求
from bs4 import BeautifulSoup  # 解析HTML
import pandas as pd  # 格式化数据，并方便导出为Excel
import json  # 解析JSON
import time  # 做随机延迟，避免访问频率过高被服务器拒绝
import random  # 正态分布随机
import re  # 正则匹配
import jieba  # 切词
from pyecharts.charts import WordCloud

# 声明B站的API
# https://api.bilibili.com/x/web-interface/view?bvid={BVCode}
# 获取视频描述JSON
VideoDescripAPI_Ahead = "https://api.bilibili.com/x/web-interface/view?bvid="

# "https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={oid}&month={Year}-{m}"
# 获取该月中，有历史弹幕的日期的JSON
HistoryDMDateAPI_Ahead = "https://api.bilibili.com/x/v2/dm/history/index?type=1"

# "https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={oid}&date={date}" date 格式是 "年-月-日"
# 获取某一天的历史弹幕文件
HistoryDMFileAPI_Ahead = "https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1"

# "https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid={oid}&pid={pid}&segment_index=1"
# 获取视频目前直接展示的弹幕文件
CurrentDMFileAPI_Ahead = "https://api.bilibili.com/x/v2/dm/web/seg.so?type=1"

# "https://comment.bilibili.com/{cid}.xml"
# 获取当前视频展示的弹幕xml文件，包括弹幕发送时间、发送弹幕的用户ID、弹幕内容
NewCurrentDMFileAPI_Ahead = "https://comment.bilibili.com/"

# "https://api.bilibili.com/x/v2/reply?type=1&pn={pn}}&oid={oid}" pn表示翻页
# 获取视频评论内容JSON的API
CommentAPI_Ahead = "https://api.bilibili.com/x/v2/reply?type=1"

# 随机的休眠程序，防止被服务器发现是爬虫
def RandomSleep(mu=1, sigma=0.6):
    '''
    正态分布随机睡眠
    mu: 平均值
    sigma: 标准差，决定被动范围
    '''
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu  # 得到的数值太小，就设为平均值
    time.sleep(secs)

# 定义 HTTPRequestHeader
def GetHeaders():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55", "Cookie": "_uuid=B8A3F472-091C-0780-F857-C4E98C5C5E0829363infoc; buvid3=6E6D6A49-688D-4CC7-8008-313C2BE5BE7F18534infoc; CURRENT_FNVAL=80; rpdid=|(mmJmlmmlJ0J'uYu|~Ylm)Y; buvid_fp=6E6D6A49-688D-4CC7-8008-313C2BE5BE7F18534infoc; buvid_fp_plain=6E6D6A49-688D-4CC7-8008-313C2BE5BE7F18534infoc; LIVE_BUVID=AUTO3816124350664535; dy_spec_agreed=1; CURRENT_QUALITY=120; fingerprint3=d3beef554a97a81d0635fbffb944b8ac; fingerprint_s=7c5f3fc3853ba1c53b439f7a0b644b18; blackside_state=1; fingerprint=a6c9b0fb0336c0a40208f0569ba545b4; SESSDATA=17c1eacc%2C1642209456%2Caeb2d%2A71; bili_jct=8b82ddfa3b5966b94d6de72f8d52f210; DedeUserID=19131632; DedeUserID__ckMd5=16416db9cc777f9e; sid=a91l1eeg; CURRENT_BLACKGAP=1; bsource=search_baidu; PVID=1; bp_t_offset_19131632=553091903973577321; bp_video_offset_19131632=553148889596970939; bfe_id=1bad38f44e358ca77469025e0405c4a6"}

# 获取视频描述
def GetVideoDescriptionJson(BVCode):
    if len(BVCode) <= 0:
        print("并未指定BV号，请指定")
        return
    url = f"{VideoDescripAPI_Ahead}{BVCode}"

    r = requests.get(url, headers=GetHeaders())
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        print(f"获取视频描述失败，错误代码：{r}")
        return

class BBSpider():

    # 记录存储了视频描述的 JSON对象
    __VideoDescriptionJson = None
    # 指定视频的BV号
    BVCode = "BV1fV411Y7ng"
    
    def __init__(self, BVCode):
        self.BVCode = BVCode
        self.__VideoDescriptionJson = GetVideoDescriptionJson(BVCode)
    

    # 获这一年有弹幕的日期 返回的是一个 list
    def __GetHistoryDMAvailableDate(self):
        if self.__VideoDescriptionJson == None:
            print("错误：获取历史弹幕列表失败\n原因：视频描述JSON为空")
            return

        oid = self.__VideoDescriptionJson['data']['cid']

        # 获取现在的年份、月份
        TimeStruct = time.localtime()
        Year = TimeStruct[0]
        Month = TimeStruct[1]

        AvailableDate = []

        for i in range(1, Month + 1):
            # 拼凑url
            m = f"0{i}" if i < 10 else i
            url = f"{HistoryDMDateAPI_Ahead}&oid={oid}&month={Year}-{m}"
            print(url)

            # 随机睡眠程序，防止频率过高被服务器屏蔽
            RandomSleep()

            # 访问 API 获取JSON信息
            r = requests.get(url, headers=GetHeaders())
            if r.status_code != 200:
                print(r)
                continue

            JsonContent = json.loads(r.text)

            # 如果不为空就把有弹幕的日期的 list 添加进列表中
            if JsonContent['data'] != None:
                DateList = JsonContent['data']
                AvailableDate.append(DateList)
            else:
                print(f"{Year}-{i}没有弹幕")

        return AvailableDate


    # 获取历史弹幕 List
    def __GetHistoryDMList(self,DateList):
        DMList = []
        # 检查全局变量是否被赋值过
        if self.__VideoDescriptionJson == None:
            print("错误:获取历史弹幕失败\n原因:视频描述JSON为空")
            return

        oid = self.__VideoDescriptionJson['data']['cid']

        for Date in DateList:
            for date in Date:
                url = f"{HistoryDMFileAPI_Ahead}&oid={oid}&date={date}"

                # 随机睡眠程序，防止频率过高被服务器屏蔽
                RandomSleep()

                # 访问 API 获取JSON信息
                print(url)
                r = requests.get(url, headers=GetHeaders())
                if r.status_code != 200:
                    print(r)
                    continue

                DM_Raw = r.text
                DM = re.findall(
                    r'((?<=:.)[\u4E00-\u9FA5A-Za-z0-9_ ]*)(?=@)', DM_Raw)
                if DM == None:
                    print("正则匹配未匹配内容")
                else:
                    #print(DM)
                    DMList = DMList+DM  # 拼接List
        return DMList


    # 获取现在视频显示的弹幕
    def __GetCurrentDMList(self):
        DMList = []
        # 检查全局变量是否被赋值过
        if self.__VideoDescriptionJson == None:
            print("错误:获取目前弹幕失败\n原因:视频描述JSON为空")
            return

        oid = self.__VideoDescriptionJson['data']['cid']
        pid = self.__VideoDescriptionJson['data']['aid']

        url = f"{CurrentDMFileAPI_Ahead}&oid={oid}&pid={pid}&segment_index=1"

        r = requests.get(url, headers=GetHeaders())

        if r.status_code != 200:
            print(r)
            return

        DM_Raw = r.text
        DM = re.findall(r'((?<=:.)[\u4E00-\u9FA5A-Za-z0-9_ ]*)(?=@)', DM_Raw)
        if DM == None:
            print("正则匹配未匹配内容")
        else:
            DMList = DMList + DM  # 拼接List

        return DMList

    # 新版本 获取现在视频显示的弹幕
    def __GetCurrentDMList_New(self):
        DMDict = {}
        # 检查全局变量是否被赋值过
        if self.__VideoDescriptionJson == None:
            print("错误:获取目前弹幕失败\n原因:视频描述JSON为空")
            return
        cid = self.__VideoDescriptionJson['data']['cid']

        url = f"{NewCurrentDMFileAPI_Ahead}/{cid}.xml"

        r = requests.get(url, headers=GetHeaders())
        
        # 尝试获取文件编码，防止文件乱码
        r.encoding = r.apparent_encoding

        if r.status_code != 200:
            print(r)
            return

        xml = r.text
        soup = BeautifulSoup(xml, 'lxml')
        content_all = soup.find_all(name="d")
        for content in content_all:
            Time = float(content.attrs["p"].split(",")[0])
            Message = content.string
            DMDict[Time] = Message
        return DMDict



    # 处理所有弹幕内容的空格,并进行分词
    def __CutDM(self,DMList):
        CutWordList = []

        for DM in DMList:
            Cutwords = jieba.lcut(DM)   # 切词
            for word in Cutwords:
                Temp = word.replace(' ', '')
                # 当一个词的长度大于1 又小于4，才加入 list
                if len(Temp) > 1:
                    if len(Temp) < 5:
                        CutWordList.append(Temp)
        return CutWordList


    # 获取视频评论的JSON解析后对象
    def __GetAllCommentsJsonObj(self):
        AllComments = []        # 获取所有的评论JSON对象
        Headers = GetHeaders()  # 指定requestHeader
        CommentsNum = 0         # 存储评论总数的变量

        # 检查全局变量是否被赋值过
        if self.__VideoDescriptionJson == None:
            print("错误:获取目前弹幕失败\n原因:视频描述JSON为空")
            return

        oid = self.__VideoDescriptionJson['data']['aid']
        FUrl = f"{CommentAPI_Ahead}&pn=0&oid={oid}"

        # 访问一次,获取评论总数
        FirstR = requests.get(FUrl, Headers)
        if FirstR.status_code == 200:
            J = json.loads(FirstR.text)
            
            CommentsNum = J['data']['page']['acount']
        else:
            return None

        for Count in range(0, CommentsNum//20+1 if CommentsNum % 20 > 0 else CommentsNum//20):
            # 获取URL
            url = f"{CommentAPI_Ahead}&pn={Count}&oid={oid}"
            # 获取JSON
            response = requests.get(url, Headers)

            # 人工停顿预防爬虫检测
            RandomSleep()

            print(f"正在获取第 {Count} 页的评论内容...")

            if response.status_code == 200:
                # 解析JSON
                JsonContent = json.loads(response.text)
                for i in range(len(JsonContent['data']['replies'])):
                    comment = JsonContent['data']['replies'][i]
                    AllComments.append(comment)
            else:
                print(response)

        return AllComments 


    # 把评论转化成 Pandas 的 DataFrame 数据结构
    def __GetDataFrameByComment(self,Comments):
        if len(Comments) <= 0:
            return None
        Count = 0
        messageList = []
        nameList = []
        sexList = []
        signList = []
        levelList = []
        for content in Comments:
            # 获取评论内容
            message = content['content']['message']
            messageList.append(message)
            # 获取评论者名字
            name = content['member']['uname']
            nameList.append(name)
            # 获取评论者性别
            sex = content['member']['sex']
            sexList.append(sex)
            # 获取评论者个性签名
            sign = content['member']['sign']
            signList.append(sign)
            # 获取评论者等级
            level = content['member']['level_info']['current_level']
            levelList.append(level)
        data = {'Name': nameList, 'Level': levelList,
                'Sex': sexList, 'Sign': signList, 'Comment': messageList}
        df = pd.DataFrame(data)
        return df

    # 统计弹幕词频
    def __CalculateWordFrequence(self, DMList):
        Words = self.__CutDM(DMList)
        WordDict = {}
        
        for Word in Words:
            if Word not in WordDict.keys():
                WordDict[Word] = 1
            else:
                WordDict[Word] = WordDict[Word] + 1
        
        return WordDict
    
    # 一键获取弹幕
    def 去吧小蜘蛛抓弹幕(self, bIsHistory=False):
        if bIsHistory:
            return self.__GetHistoryDMList(self.__GetHistoryDMAvailableDate())
        else:
            return self.__GetCurrentDMList_New()
        

    # 一键获取评论
    def 去吧小蜘蛛抓评论(self):
        Result = self.__GetAllCommentsJsonObj()
        return self.__GetDataFrameByComment(Result)

    # 生成词云图
    def 生成词云图(self, MessageList, fileName, wordSizeRange =[10,100], height=1080, width=1920):
        # 统计一下词频
        Result = self.__CalculateWordFrequence(MessageList)
        wordCloud = WordCloud()
        wordCloud.add(series_name="", data_pair=Result.items(),
                    word_size_range=wordSizeRange, height=height, width=1280)
        wordCloud.render(f"{fileName}.html")

    # 获取弹幕并生成词云图
    def 获取弹幕并生成词云图(self, FileName = "Result", WordSizeRange =[10,100], Height=1080, Width=1920, bIsHistory=False):
        DMDict = {}
        DMDict = self.去吧小蜘蛛抓弹幕(bIsHistory)
        self.生成词云图(list(DMDict.values()), FileName, WordSizeRange, Height, Width)
        
    # 获取评论并生成词云图
    def 获取评论并生成词云图(self, FileName="Result", WordSizeRange=[10, 100], Height=1080, Width=1920, bIsHistory=False):
        CommentDataFrame = self.去吧小蜘蛛抓评论()
        MessageList = CommentDataFrame["Comment"].tolist()
        self.生成词云图(MessageList, FileName, WordSizeRange, Height,Width)

