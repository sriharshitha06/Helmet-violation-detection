from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

Base = declarative_base()

class Violation(Base):
    __tablename__ = 'violations'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    plate_number = Column(String)
    image_path = Column(String) # Path to the evidence image
    video_path = Column(String, nullable=True) # Optional path to video clip
    status = Column(String, default='pending') # pending, reviewed, sent

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'plate_number': self.plate_number,
            'image_path': self.image_path,
            'status': self.status
        }

class DatabaseManager:
    def __init__(self, db_path='sqlite:///data/violations.db'):
        # Ensure data directory exists
        if db_path.startswith('sqlite:///'):
            path = db_path.replace('sqlite:///', '')
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_violation(self, plate_number, image_path):
        session = self.Session()
        new_violation = Violation(plate_number=plate_number, image_path=image_path)
        session.add(new_violation)
        session.commit()
        v_id = new_violation.id
        session.close()
        return v_id

    def get_violations(self):
        session = self.Session()
        violations = session.query(Violation).order_by(Violation.timestamp.desc()).all()
        results = [v.to_dict() for v in violations]
        session.close()
        return results
