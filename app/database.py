# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,Index
from . import db

class Base(db.Model):
    __abstract__ = True

def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    
Base.to_dict = to_dict

class SECOND_HOME(Base):
    __tablename__ = 'SECOND_HOME'
    part1_pid = db.Column(db.Integer,primary_key=True)
    part1_bah = db.Column(db.Integer)
    part1_zycs = db.Column(db.Integer)
    part1_ylfkfs = db.Column(db.Integer)
    part1_nl = db.Column(db.Integer)
    part1_tz = db.Column(db.String(120))
    part1_sg = db.Column(db.String(120))
    part1_xb = db.Column(db.Integer)
    part1_sjzyts = db.Column(db.Integer)
    part1_HIS = db.Column(db.Integer)
    part1_cyzd1 = db.Column(db.String(120))
    part1_mzfs = db.Column(db.String(120))
    part1_ssmc = db.Column(db.String(120))
    # fee = relationship("Fee")
    # lis = relationship()
class HOME(Base):
    __tablename__ = 'HOME'
    part1_pid = db.Column(db.Integer,primary_key=True)
    part1_bah = db.Column(db.Integer)
    part1_zycs = db.Column(db.Integer)
    part1_ylfkfs = db.Column(db.Integer)
    part1_nl = db.Column(db.Integer)
    part1_tz = db.Column(db.String(120))
    part1_sg = db.Column(db.String(120))
    part1_xb = db.Column(db.Integer)
    part1_sjzyts = db.Column(db.Integer)
    part1_HIS = db.Column(db.Integer)
    part1_cyzd1 = db.Column(db.String(120))
    part1_mzfs = db.Column(db.String(120))
    part1_ssmc = db.Column(db.String(120))
    part1_rysj = db.Column(db.String(120))
    part1_cysj = db.Column(db.String(120))
    
class SECOND_FEE(db.Model):
    __tablename__ = 'SECOND_FEE'
    part2_pid = db.Column(db.Integer,primary_key=True)
    part2_bah = db.Column(db.Integer, ForeignKey('SECOND_HOME.part1_bah'))
    part2_zyzfy = db.Column(db.Float)
    part2_ybylfwf = db.Column(db.Float)
    part2_ybzlczf = db.Column(db.Float)
    part2_hlf = db.Column(db.Float)
    part2_zhylfwlqtfy = db.Column(db.Float)
    part2_blzdf = db.Column(db.Float)
    part2_syszdf = db.Column(db.Float)
    part2_yxxzdf = db.Column(db.Float)
    part2_lczdxmf = db.Column(db.Float)
    part2_fsszlxmf = db.Column(db.Float)
    part2_sszlf = db.Column(db.Float)
    part2_mzf = db.Column(db.Float)
    part2_ssf = db.Column(db.Float)
    part2_kff = db.Column(db.Float)
    part2_zyzlf = db.Column(db.Float)
    part2_xyf = db.Column(db.Float)
    part2_kjywfy = db.Column(db.Float)
    part2_zcyf = db.Column(db.Float)
    part2_jcyycxyyclf = db.Column(db.Float)
    part2_zlyycxyyclf = db.Column(db.Float)
    part2_ssyycxyyclf = db.Column(db.Float)
    # home_id = db.Column(db.Inter, ForeignKey('SECOND_HOME.part1_bah'))
class FEE(db.Model):
    __tablename__ = 'FEE'
    part2_pid = db.Column(db.Integer,primary_key=True)
    part2_bah = db.Column(db.Integer, ForeignKey('SECOND_HOME.part1_bah'))
    part2_zyzfy = db.Column(db.Float)
    part2_ybylfwf = db.Column(db.Float)
    part2_ybzlczf = db.Column(db.Float)
    part2_hlf = db.Column(db.Float)
    part2_zhylfwlqtfy = db.Column(db.Float)
    part2_blzdf = db.Column(db.Float)
    part2_syszdf = db.Column(db.Float)
    part2_yxxzdf = db.Column(db.Float)
    part2_lczdxmf = db.Column(db.Float)
    part2_fsszlxmf = db.Column(db.Float)
    part2_sszlf = db.Column(db.Float)
    part2_mzf = db.Column(db.Float)
    part2_ssf = db.Column(db.Float)
    part2_kff = db.Column(db.Float)
    part2_zyzlf = db.Column(db.Float)
    part2_xyf = db.Column(db.Float)
    part2_kjywfy = db.Column(db.Float)
    part2_zcyf = db.Column(db.Float)
    part2_jcyycxyyclf = db.Column(db.Float)
    part2_zlyycxyyclf = db.Column(db.Float)
    part2_ssyycxyyclf = db.Column(db.Float)

    
class SECOND_LIS(db.Model):
    __tabkename__= 'SECOND_LIS'
    part3_pid = db.Column(db.Integer, primary_key=True)
    part3_INSPECTION_DATE = db.Column(db.String(120))
    part3_PATIENT_NAME = db.Column(db.String(120))
    part3_OUTPATIENT_ID = db.Column(db.Integer, ForeignKey('SHECOND_HOME.part1_bah'))
    part3_INPATIENT_ID = db.Column(db.Integer)
    part3_PATIENT_SEX = db.Column(db.Integer)
    part3_AGE_INPUT = db.Column(db.String(120))
    part3_CLINICAL_DIAGNOSES_NAME = db.Column(db.String(300))
    part3_TEST_ORDER_NAME = db.Column(db.String(300))
    part3_CHINESE_NAME = db.Column(db.String(300))
    part3_QUANTITATIVE_RESULT = db.Column(db.String(120))
    part3_QUALITATIVE_RESULT = db.Column(db.String(120))

# class Patient(db.Model):
#     part3_pid = db.Column(db.Integer, primary_key=True)
#     part1_pid = db.Column(db.Integer)

