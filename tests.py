from pymsg import DingTalkRobot


def test_ding_talk():
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=248882788a58145bb11ae618dda95a1fca3859e4f29a1ee04ce42b6c225de9cd'
    msg = DingTalkRobot(webhook)

    msg.text('我就是我,  @1825718XXXX 是不一样的烟火', at_all=True)
    msg.link(title='自定义机器人协议',
             text='群机器人是钉钉群的高级扩展功能。群机器人可以将第三方服务的信息聚合到群聊中，实现自动化的信息同步。例如：通过聚合GitHub，GitLab等源码管理服务，实现源码更新同步；通过聚合Trello，JIRA等项目协调服务，实现项目信息同步。不仅如此，群机器人支持Webhook协议的自定义接入，支持更多可能性，例如：你可将运维报警提醒通过自定义机器人聚合到钉钉群。',
             msg_url='https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.Rqyvqo&treeId=257&articleId=105735&docType=1',
             pic_url='https://www.baidu.com/img/bd_logo1.png'
             )
    msg.markdown(title='杭州天气',
                 text='#### 杭州天气  \n > 9度，@1825718XXXX 西北风1级，空气良89，相对温度73%\n\n > ![screenshot](http://i01.lw.aliimg.com/media/lALPBbCc1ZhJGIvNAkzNBLA_1200_588.png)\n  > ###### 10点20分发布 [天气](http://www.thinkpage.cn/) ',
                 at_all=True)
    msg.action_card(title='乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身',
                    text='![screenshot](@lADOpwk3K80C0M0FoA) \n #### 乔布斯 20 年前想打造的苹果咖啡厅 \n\n Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划',
                    btn=('阅读全文', 'https://www.dingtalk.com/'),
                    hide_avatar=True)
    msg.action_card('乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身',
                    '![screenshot](@lADOpwk3K80C0M0FoA) \n #### 乔布斯 20 年前想打造的苹果咖啡厅 \n\n Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划',
                    ('内容不错', 'https://www.dingtalk.com/'), ('不感兴趣', 'https://www.dingtalk.com/'),
                    btns_vertically=False,
                    hide_avatar=True)
    msg.feed_card(('时代的火车向前开',
                   'https://mp.weixin.qq.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI',
                   'https://www.dingtalk.com/'),
                  ('时代的火车向前开2',
                   'https://mp.weixin.qq.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI',
                   'https://www.dingtalk.com/'))


if __name__ == '__main__':
    test_ding_talk()
