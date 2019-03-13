# pymsy

### 安装
```bash
pip install pymsg
```

### 功能
#### _class_ DingTalkRobot

> 因钉钉的[自定义机器人](https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.karFPe&treeId=257&articleId=105735&docType=1)存在限制："每个机器人每分钟最多发送20条"；为方便使用，该类实例会暂存不能发送的消息，并在适当的时候发送出去，且所有方法均是线程安全的

**示例**
```
>>> from pymsg import DingTalkRobot

>>> robot = DingTalkRobot('https://oapi.dingtalk.com/robot/send?access_token=***')

>>> robot.set_cache_size(30)    # 设置缓存大小，默认：20

>>> robot.text(
...     content='我就是我,  @1825718**** 是不一样的烟火',  # 消息内容
...     at='1825718****',   # 被@人的手机号, 可传多个
...     at_all=False    # @所有人，默认：False
... )
```
**结果**

<img src="http://i01.lw.aliimg.com/media/lADPBbCc1ZgiBN3M0M0C6A_744_208.jpg" width="500">

###### _详细功能请参考[代码](https://github.com/Dog-Egg/pymsg/blob/dev/pymsg.py)_