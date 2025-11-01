from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# 데이터베이스 엔진 생성 (AWS RDS MySQL)
# DATABASE_URL 형식: mysql+pymysql://username:password@host:port/database
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 연결 유효성 검사 (AWS RDS 연결 유지에 중요)
    pool_recycle=3600,   # 1시간마다 연결 재생성
    pool_size=10,        # 연결 풀 크기
    max_overflow=20,     # 최대 추가 연결 수
    echo=False  # SQL 쿼리 로깅 (개발 시 True로 변경 가능)
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 (모델이 상속받을 클래스)
Base = declarative_base()

def get_db():
    """
    데이터베이스 세션 의존성 함수
    FastAPI의 Depends()와 함께 사용
    
    사용 예시:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    데이터베이스 테이블 초기화
    프로덕션에서는 Alembic 마이그레이션 사용 권장
    """
    # 모든 모델을 import해야 테이블이 생성됨
    # from app.models import user, subscription_info, preference, announcement, application, notification
    
    Base.metadata.create_all(bind=engine)

