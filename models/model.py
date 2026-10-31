# Layer Model: Hanya mengurus struktur tabel database
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    ipk = Column(Float)
    sks = Column(Integer)
    status_kelulusan = Column(String)