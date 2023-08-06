## pyeasy - python eaasy to develop  
## 使Python开发变的更简单

使用示例：  
1.Mysql操作（常用于爬虫场景, 不支持事务）
```python
from pyeasytd.mysql_util import MysqlUtil

# 通过工具获取连接对象MysqlEasyConnection   
conn = MysqlUtil.connect(host='xx', port=3306, username='xx', password='xx', db='xx')  

# 使用sql插入数据
conn.insert(sql='insert into test_tb(name) values("name1")') # 不推荐
conn.insert(sql='insert into test_tb(name) values(%s)', args=('name1', ))

# 插入一个字典对象
conn.insert_dict(table='test_tb', data={'name': 'name2'})
# 插入一个字典对象，若已存在则覆盖
conn.insert_dict(table='test_tb', data={'name': 'name2'}, mode='overwrite')
# 插入一个字典对象，若已存在则忽略
conn.insert_dict(table='test_tb', data={'name': 'name2'}, mode='ignore')

# 插入一个字典对象，若不存在表则创建表，若缺失列则添加列, 以key为字段名,key不支持中文,若有中文建议使用拼音转换工具转为拼音存储
conn.insert_dict_auto_add_table_and_column(table='test_tb', data={'name': 'name2', 'age': 18})
# 插入一个字典对象，若表不存在建表时使用字典对象的一个字段作为主键
conn.insert_dict_auto_add_table_and_column(table='test_tb', data={'name': 'name2', 'unique_id': 'xxxx'}, primary_name='unique_id')

# 批量插入数据,对数据内部进行分批多次写入,默认每条sql批量写入200条
conn.insert_dicts(table='test_tb', data=[{'name': 'name1'}, {'name': 'name2'}])

# 自定义对象插入
class User:
    name = None
    age = None
    def __init__(self, name, age):
        self.name = name
        self.age = age
conn.insert_dict(table='user_tb', data=User('name1', None))

# sql查询, 默认返回[{}, {}] 结构
conn.query('select * from test_tb where id=1') # 不推荐
conn.query('select * from test_tb where id=%s', args=(1,))
# sql查询返回tuple[(), ()]
conn.query('select * from test_tb where id=%s', args=(1,), type='tuple')
```  
2 企业微信机器人推送消息操作  
```python
from pyeasytd.wechat import send_message_to_enterprise_wechat  
send_message_to_enterprise_wechat(...)
```
3.发送邮件操作  
```python
from pyeasytd import send_email_old, send_mail  
send_email_old(...)
send_mail(...)
```
#### 0.0.9版本变更内容
1.Mysql查询工具优化

#### 0.0.5版本变更内容  
1.新增发送邮件方法  

#### 0.0.4版本变更内容  
1.新增企业微信群机器人推送方法  

#### 0.0.3版本变更内容：  
1.新增XlsxFileEasyEntry实体  
2.新增XlsxFileUtil工具类  

0.0.2版本变更内容：  
1.新增FileUtil工具类  

0.0.1版本变更内容：  
1.新增MysqlEasyEntry,JsonEasyEntry实体  
2.新增MysqlUtil,JsonUtil工具类  