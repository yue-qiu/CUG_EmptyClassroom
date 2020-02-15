# 地大空教室爬虫

**需要在 CUG 校园网及 MYSQL 环境下使用！**

## 配置

爬虫主体 EmptyClassroomSpider 位于 Spider ，
配置文件 Config.ini 位于 Config 包。
已经给出 Config.ini.example，根据需要补全字段后更名为 Config.ini 即可使用


account 含登录数字地大账号`username`，密码`password`

week 含开始抓取周`start`，结束周`end`，起始周与结束周可以相同，

`start` 与 `end` 不是必须的，如果没有`start`与`end`字段爬虫会爬取当前周的数据：

```ini
# 没有 start 与 end 字段
[week]

```
db 含主机地址`host`，账号`username`，密码`password`，数据库`database`

## 运行结果
爬取所得数据位于 empty_classroom 表中：

```ini
date：日期。如 "2019-04-06"
week：周。
day：星期。星期一为 0，星期二为 1......
session：空闲时间。如"1,2"（注意无空格）, "白天"
data：空教室信息
update_at：更新时间
```

完成配置后，执行:

```shell script
python main.py
```
等待一段时间后控制台显示 Succeed 则成功，否则查看 log 获取帮助
