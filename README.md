# 도서관 대출 시스템 - DDD 실습 프로젝트

DDD(Domain-Driven Design)를 직접 체험하며 학습하는 Python 프로젝트

---

## 기술 스택

- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.x
- **Container**: Docker, Docker Compose

---

## 아키텍처

DDD의 레이어드 아키텍처를 적용함

```
api/            → HTTP 요청/응답 처리 (FastAPI Router)
application/    → 비즈니스 흐름 조합 (Use Case)
domain/         → 비즈니스 규칙과 개념 (순수 Python)
infrastructure/ → DB 저장소 구현 (SQLAlchemy)
```

### 의존성 방향

```
api → application → domain ← infrastructure
```

domain은 아무것도 의존하지 않는다.

---

## 도메인 개념

### Value Object
| 이름 | 설명 |
|------|------|
| ISBN | 책의 고유 번호. 불변, 값으로 동등성 비교, 자가 유효성 검사 |

### Entity
| 이름 | 식별자 | 설명 |
|------|--------|------|
| Book | isbn | 도서관의 책. 대출 가능 여부 관리 |
| Member | member_id | 도서관 회원. 대출 가능 여부 판단 |

### Aggregate Root
| 이름 | 설명 |
|------|------|
| Loan | 대출 기록. Book과 Member를 묶어서 상태를 책임지고 관리 |

### Domain Service
| 이름 | 설명 |
|------|------|
| LoanService | 대출 가능 여부 판단 로직 |

---

## 비즈니스 규칙

- 회원은 최대 3권까지 동시 대출 가능
- 이미 대출 중인 책은 중복 대출 불가
- 반납 기한은 대출일로부터 14일
- 연체 회원은 반납 전까지 신규 대출 불가

---

## 프로젝트 구조

```
library-ddd/
├── api/
│   ├── book_router.py
│   ├── member_router.py
│   └── loan_router.py
├── application/
│   ├── book_use_case.py
│   ├── member_use_case.py
│   └── loan_use_case.py
├── domain/
│   ├── book/
│   │   ├── book.py
│   │   ├── isbn.py
│   │   └── book_repository.py
│   ├── member/
│   │   ├── member.py
│   │   └── member_repository.py
│   └── loan/
│       ├── loan.py
│       ├── loan_service.py
│       └── loan_repository.py
├── infrastructure/
│   ├── database.py
│   ├── models.py
│   ├── book_repository.py
│   ├── member_repository.py
│   └── loan_repository.py
├── config.py
├── main.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 실행 방법

### 1. 환경 변수 설정

```bash
cp .env.example .env
```

```bash
# .env
POSTGRES_USER=library
POSTGRES_PASSWORD=library
POSTGRES_DB=library
DATABASE_URL=postgresql://library:library@db:5432/library
```

### 2. 실행

```bash
docker compose up
```

### 3. API 문서 확인

```
http://localhost:8000/docs
```

---

## API 목록

### Book
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /books | 책 등록 |
| GET | /books/{isbn} | 책 조회 |

### Member
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /members | 회원 등록 |
| GET | /members/{member_id} | 회원 조회 |

### Loan
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /loans/borrow | 대출 |
| POST | /loans/{loan_id}/return | 반납 |