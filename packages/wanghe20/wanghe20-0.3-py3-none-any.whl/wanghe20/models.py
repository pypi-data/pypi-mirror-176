# coding=utf-8
from sqlalchemy.orm import registry
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine('sqlite:///test.sqlite', connect_args={'check_same_thread': False})
session = Session(engine) 

my_registry = registry()


# 获取模型类基类
Base = my_registry.generate_base()


class UpdateDeviceVersionClass(Base):
    """
    更新设备版本表 
    """
    __tablename__ = "update_device_version"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    device_name = Column(String(64), nullable=False)
    rule_version = Column(String(32), nullable=True)
    ioc_version = Column(String(32), nullable=True)
    sys_version = Column(String(32), nullable=True)
    product_id = Column(Integer, nullable=False)

Base.metadata.create_all(engine)