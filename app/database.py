import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fitbuddy.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    username = Column(String)
    age = Column(Integer)
    weight = Column(Integer)
    goal = Column(String)
    intensity = Column(String)

class PlanDB(Base):
    __tablename__ = "plans"

    user_id = Column(String, primary_key=True, index=True)
    original_plan = Column(Text)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_user(db, user_id: str, username: str, age: int, weight: int, goal: str, intensity: str):
    user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not user:
        user = UserDB(user_id=user_id, username=username, age=age, weight=weight, goal=goal, intensity=intensity)
        db.add(user)
    else:
        user.username = username
        user.age = age
        user.weight = weight
        user.goal = goal
        user.intensity = intensity
    db.commit()
    db.refresh(user)
    return user

def save_plan(db, user_id: str, original_plan: str, nutrition_tip: str):
    plan = db.query(PlanDB).filter(PlanDB.user_id == user_id).first()
    if not plan:
        plan = PlanDB(user_id=user_id, original_plan=original_plan, nutrition_tip=nutrition_tip)
        db.add(plan)
    else:
        plan.original_plan = original_plan
        plan.nutrition_tip = nutrition_tip
    db.commit()
    db.refresh(plan)
    return plan

def update_plan_db(db, user_id: str, updated_plan_text: str):
    plan = db.query(PlanDB).filter(PlanDB.user_id == user_id).first()
    if plan:
        plan.updated_plan = updated_plan_text
        db.commit()
        db.refresh(plan)
    return plan

def get_all_users_with_plans(db):
    users = db.query(UserDB).all()
    result = []
    for u in users:
        p = db.query(PlanDB).filter(PlanDB.user_id == u.user_id).first()
        result.append({
            "user_id": u.user_id,
            "username": u.username,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "original_plan": p.original_plan if p else "N/A",
            "updated_plan": p.updated_plan if p and p.updated_plan else "None",
            "nutrition_tip": p.nutrition_tip if p else "N/A"
        })
    return result
