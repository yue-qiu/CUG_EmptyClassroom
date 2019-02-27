from Spider import EmptyClassroomSpider
import Spider.Config as Config

if __name__ == '__main__':
    spider = EmptyClassroomSpider(Config.account, Config.db_config)
    spider.run()
