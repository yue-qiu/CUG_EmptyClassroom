from Spider import EmptyClassroomSpider
import Config

if __name__ == '__main__':
    spider = EmptyClassroomSpider(Config.account, Config.db_config, Config.week)
    spider.run()
