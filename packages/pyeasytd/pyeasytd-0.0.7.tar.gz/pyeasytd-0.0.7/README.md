## pyeasy - python eaasy to develop  
## 使Python开发变的更简单
使用示例：  
1.Mysql操作  
from pyeasytd.mysql_util import MysqlUtil  
obj = MysqlUtil.connect(...)  
MysqlUtil.xxx(obj, ...)  
2.Json操作  
from pyeasytd.json_util import JsonUtil  
obj = JsonUtil.loads(...)  
JsonUtil.xxx(obj, ...)  
3.普通文件处理  
from pyeasytd.file_util import FileUtil  
FileUtil.xxx(...)  
4.xlsx文件操作  
from pyeasytd.file_util import XlsxFileUtil  
obj = XlsxFileUtil(...)  
XlsxFileUtil.xxx(...)  
5 企业微信机器人推送消息操作  
from pyeasytd.wechat import send_message_to_enterprise_wechat  
send_message_to_enterprise_wechat(...)    
6.发送邮件操作  
from pyeasytd import send_mail_old, send_mail  
send_mail_old(...)  或 send_mail(...)  

0.0.5版本变更内容  
1.新增发送邮件方法  

0.0.4版本变更内容  
1.新增企业微信群机器人推送方法  

0.0.3版本变更内容：  
1.新增XlsxFileEasyEntry实体  
2.新增XlsxFileUtil工具类  

0.0.2版本变更内容：  
1.新增FileUtil工具类  

0.0.1版本变更内容：  
1.新增MysqlEasyEntry,JsonEasyEntry实体  
2.新增MysqlUtil,JsonUtil工具类  