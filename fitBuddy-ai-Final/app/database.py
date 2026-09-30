"""SQLite + SQLAlchemy models and DB helper functions."""
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "fitbuddy.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)
    schedule = Column(Integer, default=7)

class WorkoutPlan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_plan = Column(Text)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)

def init_db():
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _user_dict(u):
    return {"id": u.id, "name": u.name, "age": u.age, "weight": u.weight,
            "goal": u.goal, "intensity": u.intensity}


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    with session_scope() as db:
        user = db.get(User, user_id)
        if user:
           user.name, user.age, user.weight = name, age, weight
           user.goal, user.intensity = goal, intensity
        else:
           db.add(User(id=user_id, name=name, age=age, weight=weight,
                 goal=goal, intensity=intensity, schedule=7))


def save_plan(user_id: int, plan: str, tip: str | None = None):
    """Store a fresh plan (replaces any previous plan for this user)."""
    with session_scope() as db:
        wp = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if wp:
            wp.original_plan, wp.updated_plan, wp.nutrition_tip = plan, None, tip
        else:
            db.add(WorkoutPlan(user_id=user_id, original_plan=plan, nutrition_tip=tip))

def update_plan(user_id: int, updated_text: str, tip: str | None = None):
    with session_scope() as db:
        wp = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if wp:
            wp.updated_plan = updated_text
            if tip:
                wp.nutrition_tip = tip


def get_original_plan(user_id: int):
    with session_scope() as db:
        wp = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        return wp.original_plan if wp else None

    
def get_plan(user_id: int):
    with session_scope() as db:
        wp = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if not wp:
            return None
        return {"original_plan": wp.original_plan, "updated_plan": wp.updated_plan,
                "nutrition_tip": wp.nutrition_tip}
def get_user(user_id: int):
    with session_scope() as db:
        u = db.get(User, user_id)
        return _user_dict(u) if u else None


def get_all_users():
    with session_scope() as db:
        return [_user_dict(u) for u in db.query(User).order_by(User.id).all()]


def get_all_plans():
    with session_scope() as db:
        return {p.user_id: {"original_plan": p.original_plan, "updated_plan": p.updated_plan}
                for p in db.query(WorkoutPlan).all()}


def delete_user(user_id: int):
    with session_scope() as db:
        db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).delete()
        db.query(User).filter(User.id == user_id).delete()
