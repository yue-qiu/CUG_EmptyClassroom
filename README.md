# 地大空教室爬虫

爬虫主体 EmptyClassroomSpider 位于 Spider 包，初始化该类需要 account 和 db_config 两个字典型参数。
要求使用 mysql 作为数据库

account 和 db_config 都位于 Spider.Config 模块

account 包含中登录数字地大账号`username`，密码`password`，开始抓取周`start`，结束周`end`，起始周与结束周可以相同：

```angular2html
account = {'username': 'xxxxxxxx', 'password': 'xxxxxxxx', 'start': 'x', 'end': 'xx'}
```

db_config 包含 mysql 主机`host`，账号`username`，密码`password`，数据库名`database`：

```angular2html
db_config = {'host': 'xxxxxx', 'username': 'xxxxx', 'password': 'xxxxxx', 'database': 'xxxxx'}
```

使用 `pipenv` 作为包管理。安装方法：
```
pip install pipenv
```
创建虚拟环境同时安装依赖：
```
pipenv install
```

爬取所得数据位于 empty_classroom 表中：

```angular2html
date：日期。如 "2019-04-06"
week：周。
day：星期。星期一为 0，星期二为 1......
session：空闲时间。如"1,2"（注意中间无空格）, "白天"
data：空教室信息
update_at：更新时间
```

完成配置(见`./Spide/Config.py.example`文件)后，执行:

```shell
python main.py
```
等待一段时间后控制台显示 Succeed 则成功，否则查看 log 获取帮助
