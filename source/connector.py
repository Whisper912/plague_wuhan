# 导入:
from entity import Result
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from configparser import ConfigParser

cp = ConfigParser()
cp.read("res/db.cfg")
host = cp.get('mysql', 'host')
port = cp.get('mysql', 'port')
user = cp.get('mysql', 'user')
pwd = cp.get('mysql', 'pwd')
database = cp.get('mysql', 'database')
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://'+user+':'+pwd+'@'+host+':'+port+'/'+database)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def updateResult(newResult):
    try:
        # 先根据 name 查询出这条数据，再更新
        result = session.query(Result).filter(Result.name == newResult.name).one()
        if newResult.total:
            result.total=newResult.total
        if newResult.cure:
            result.cure=newResult.cure
        if newResult.dead:
            result.dead=newResult.dead
        result.update_time=datetime.now()
        # 提交即保存到数据库:
        session.commit()
    except SQLAlchemyError as e:
        # 加入数据库commit提交失败，必须回滚！！！
        session.rollback()
        print("Update Fail!")
        print(e)
    else:
        # logger = Logger.Logger(log_name="result_log")
        # logger.info("Update Success!")
        # logger.info("name = "+name+", total = "+total)
        print("Update Success! "+result.__str__())

def getTotalResult():
    try:
        all_result = session.query(Result.name, Result.total).all()
        return all_result
    except SQLAlchemyError as e:
        print("Get Result Fail!")
        print(e)

def initResultName():
    with open("res/Url.json", 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())
    for t in temp:
        name = t['name']
        session.add(Result(name, 0, datetime.now()))
    session.commit()


# 关闭session:
session.close()