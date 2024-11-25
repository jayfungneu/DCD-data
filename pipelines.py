# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql
class DcdPipeline:

    def __init__(self):
        self.connect = pymysql.Connect(host="localhost", user="root", password="rootroot", port=3306, db="cop",
                                       charset="utf8")
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        # sql = "INSERT INTO comment (user_title,user_name,user_comment,using_age) VALUES ('%s','%s','%s','%s')"
        # self.cursor.execute(sql % (item['user_title'], item['user_name'], item['user_comment'],item['using_age']))
        # self.connect.commit()
        return item


    # 关闭资源
    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
