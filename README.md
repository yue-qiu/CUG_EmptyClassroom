# 地大空教室爬虫

## 配置
爬虫主体 EmptyClassroomSpider 位于 Spider ，
配置文件 Config.ini 位于 Config 包。
已经给出 Config.ini.example，根据需要补全字段后更名为 Config.ini 即可使用


account 含登录数字地大账号`username`，密码`password`

week 含开始抓取周`start`，结束周`end`，起始周与结束周可以相同，如果没有`start`与`end`字段则爬虫自行会爬取以当前周为起始结束周的数据

db 含主机地址`host`，账号`username`，密码`password`，数据库`database`


## 依赖管理
使用 `pipenv` 作为包管理。安装方法：
```
pip install pipenv
```
创建虚拟环境同时安装依赖：
```
pipenv install
```

## 运行结果
爬取所得数据位于 empty_classroom 表中：

```angular2html
date：日期。如 "2019-04-06"
week：周。
day：星期。星期一为 0，星期二为 1......
session：空闲时间。如"1,2"（注意无空格）, "白天"
data：空教室信息
update_at：更新时间
```

完成配置后，执行:

```shell
python main.py
```
等待一段时间后控制台显示 Succeed 则成功，否则查看 log 获取帮助
