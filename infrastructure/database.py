# engine  → DB와 연결하는 객체
# session → 실제 쿼리를 실행하는 객체 (트랜잭션 단위)
# Base    → 모든 모델이 상속받는 부모 클래스

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import config

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = config.DATABASE_URL

# DB 연결
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # 유지할 커넥션 갯수 (기본값 5)
    max_overflow=10,  # pool_size 초과시 추가로 허용할 갯수
    pool_timeout=30,  # 커넥션 못 얻으면 몇 초 후 에러 (기본값 30)
    pool_recycle=1800,  # 몇 초마다 커넥션 재생성 (기본값 -1, 안함)
)

# 쿼리 실행 객체
session_local = sessionmaker(bind=engine)


def get_session():
    session = session_local()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        # 원래 예외를 그대로 던짐
        raise
    finally:
        # 세션을 커넥션 풀에 반납 (종료가 아님)
        session.close()


# 모든 모델이 상속받을 Base
class Base(DeclarativeBase):
    # DeclarativeBase 클래스는 DB 테이블과 매핑되는 모델이라는걸 알려주는 부모 클래스
    pass


# Base를 상속받은 모든 모델의 테이블을 생성
def init_db():
    import infrastructure.models  # noqa

    # Base가 알고있는 모든 모델의 테이블을 생성한다.
    # 그런데 Base가 모델을 알려면, 그 모델이 메모리에 로드되어 있어야 한다.
    # python은 import 하지 않은 파일은 메모리에 없으니까
    # 위에서 infrastructure.models 를 import 해준다.
    Base.metadata.create_all(bind=engine)
