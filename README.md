# 地大空教室爬虫

爬虫主体 EmptyClassroomSpider 位于 Spider 包，初始化该类需要 account 和 db_config 两个字典型参数。
要求使用 mysql 作为数据库

account 和 db_config 都位于 Spider.Config 模块

account 包含中登录数字地大账号`username`，密码`password`，开始抓取周`start`，结束周`end`：

```angular2html
account = {'username': 'xxxxxxxx', 'password': 'xxxxxxxx', 'start': 'x', 'end': 'xx'}
```

db_config 包含 mysql 主机`host`，账号`username`，密码`password`，数据库名`database`：

```angular2html
db_config = {'host': 'xxxxxx', 'username': 'xxxxx', 'password': 'xxxxxx', 'database': 'xxxxx'}
```

爬取所得数据位于 empty_classroom 表中：

```angular2html
date：日期
week：周
day：星期。星期一为 0，星期二为 1......
session：空闲时间
data：空教室
update_at：更新时间
```

完成配置后，执行:

```shell
python main.py
```