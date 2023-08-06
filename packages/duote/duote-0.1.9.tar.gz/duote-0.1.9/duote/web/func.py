import requests
from lxml import etree


class duote:
    def __init__(self, acc, psw) -> None:
        self.session = self.login(acc, psw)
        self.table_tr_xpath = '//table[@class="data_table"]//tr[position()>1]'

    def login(self, acc, psw):
        data = {'loginName': acc,
                'Possword': psw}
        session = requests.session()
        response = session.post(
            'https://www.duote.com/default/userlogin', data=data)
        response.encoding = 'gbk'
        return session

    def get_zixun_list_info(self,
                            subclass_id='',
                            editor='',
                            title='',
                            keywords='',
                            news_id='',
                            sort_order=1,
                            start_date='',
                            end_date='',
                            pages=1):
        """_summary_

        Args:
            subclass_id (int, optional): subclass_id 对应栏目
                {
                    "11":"IT业界",
                    "12":"手机数码",
                    "13":"游戏资讯",
                    "15":"娱乐资讯",
                    "16":"社会新闻",
                    "14":"评测",
                }
            editor (str, optional): 编辑人员. Defaults to ''.
            title (str, optional): 文章标题. Defaults to ''.
            keywords (str, optional): 文章关键词. Defaults to ''.
            news_id (int, optional): 文章id. Defaults to ''.
            sort_order (int, optional): 排序id 对应项目
                {
                    "1":"新的在前",
                    "2":"旧的在前",
                    "3":"ID正序",
                    "4":"ID倒序",
                    "5":"总ip正序",
                    "6":"总ip倒序",
                    "7":"周ip正序",
                    "8":"周ip倒序",
                }
            start_date (str, optional): 开始日期,格式: yyyy-mm-dd. Defaults to ''.
            end_date (str, optional): 结束日期,格式: yyyy-mm-dd. Defaults to ''.
            page (int,optional): 翻页, 
        """
        result = []
        result_append = result.append
        url = 'https://www.duote.com/admin/news/index/%s.html'
        payload = {
            "hsearch": "",
            "class_id": "",
            "subclass_id": subclass_id,
            "editor": editor,
            "title": title.encode('gbk', errors="ignore"),
            "keywords": keywords,
            "news_id": news_id,
            "topicId": "",
            "sort_order": sort_order,
            "start_date": start_date,
            "end_date": end_date,
            "btnsubmit": "%CB%D1%CB%F7",
        }
        for p in range(pages):
            response = self.session.get(url % (p+1), params=payload)
            dom = etree.HTML(response.text)
            table_xpath = dom.xpath(self.table_tr_xpath)
            for tr in table_xpath:
                td = tr.xpath('.//td')
                item_dict = {
                    'id': td[1].xpath('./a/text()')[0],
                    'url': td[1].xpath('./a/@href')[0],
                    '总ip': td[2].xpath('./text()')[0],
                    '周ip': td[3].xpath('./text()')[0],
                    '标题': td[4].xpath('./a/text()')[0],
                    '类别': td[5].xpath('./text()')[0],
                    '发布编辑': td[6].xpath('./text()')[0],
                    '创建时间': td[8].xpath('./text()')[0],
                    '修改时间': td[9].xpath('./text()')[0],
                }
                result_append(item_dict)
        return result

    def move_zixun_to_super(self, ids):
        """资讯频道内容进高级后台.

        Args:
            ids (_type_): 文章id,以_str_或_list_形式传入,如果是list,会将list转成以逗号分割的str

        Returns:
            返回json中的msg信息
        """
        url = 'https://www.duote.com/admin/news/issupersave'
        payload = {
            'ids': ids if isinstance(ids, str) else ','.join(ids),
            'is_super': 1
        }
        response = self.session.post(url, data=payload)
        result = response.json()['msg']
        return result

    def get_hanzi_list_info(self, pages=1):
        result = []
        result_append = result.append
        url = 'https://www.duote.com/admin/word/indexword/%s'
        for p in range(pages):
            response = self.session.get(url % (p+1))
            dom = etree.HTML(response.text)
            table_xpath = dom.xpath(self.table_tr_xpath)
            for tr in table_xpath:
                td = tr.xpath('.//td')
                item_dict = {
                    'id': td[1].xpath('.//text()')[0].strip(),
                    'word': td[2].xpath('.//text()')[0].strip(),
                    'pinyin': td[3].xpath('.//text()')[0].strip() if td[3].xpath('.//text()') else '',
                    'bushou': td[4].xpath('.//text()')[0].strip() if td[4].xpath('.//text()') else '',
                    'bihua': td[5].xpath('.//text()')[0].strip() if td[5].xpath('.//text()') else '',
                }
                if pages > 200:
                    yield item_dict
                else:
                    result_append(item_dict)
        return result