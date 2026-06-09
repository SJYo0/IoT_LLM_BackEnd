# IoT LLM BackEnd

스마트 작업장의 실내 환경 센서 데이터, 외부 기상 데이터, 인프라 제어 상태를 LLM으로 분석하는 FastAPI 기반 AI 백엔드입니다. Spring Boot 백엔드에서 전달한 데이터를 받아 실시간 환경 제어 명령을 생성하고, 하루 단위의 환경/알람/에너지 사용 리포트를 생성합니다.

## 주요 기능

- 실시간 실내 환경 분석 및 인프라 제어 명령 생성
- 일일 센서 통계, 알람 이력, 기기 가동 로그 기반 AI 리포트 생성
- Pydantic DTO를 이용한 요청/응답 스키마 검증
- LangChain `ChatOpenAI`의 structured output을 이용한 응답 형식 고정
- Swagger UI를 통한 API 문서 확인

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| Language | Python 3.12 |
| Web Framework | FastAPI, Starlette |
| ASGI Server | Uvicorn |
| Data Validation | Pydantic v2 |
| LLM Orchestration | LangChain, LangChain OpenAI |
| LLM Provider | OpenAI API |
| Environment | python-dotenv |
| HTTP Client/Utils | httpx, requests |

현재 코드 기준 LLM 모델 설정은 다음과 같습니다.

- 실시간 분석 체인: `gpt-5.4-mini`
- 일일 리포트 체인: `gpt-5.4`

사용 가능한 모델명은 OpenAI 계정 및 SDK 지원 상태에 맞게 `AiAnalysis/core/analysis_chain.py`, `AiReport/core/report_chain.py`에서 조정할 수 있습니다.

## 프로젝트 구조

```text
.
├── main.py
├── requirements.txt
├── README.md
├── .env
├── AiAnalysis
│   ├── routers
│   │   └── AiAnalysis.py
│   ├── schemas
│   │   └── analysis_dto.py
│   └── core
│       ├── analysis_config.py
│       └── analysis_chain.py
├── AiReport
│   ├── routers
│   │   └── AiReport.py
│   ├── schemas
│   │   └── report_dto.py
│   └── core
│       ├── report_config.py
│       └── report_chain.py
├── ai_env
└── __pycache__
```

| 경로 | 설명 |
| --- | --- |
| `main.py` | FastAPI 앱 생성, CORS 설정, AI 분석/리포트 라우터 등록 |
| `AiAnalysis/routers/AiAnalysis.py` | `/api/v1/analyze` 엔드포인트 정의 |
| `AiAnalysis/schemas/analysis_dto.py` | 실시간 분석 요청/응답 Pydantic DTO |
| `AiAnalysis/core/analysis_config.py` | 실시간 분석용 프롬프트 템플릿 |
| `AiAnalysis/core/analysis_chain.py` | 실시간 분석용 LangChain 체인 구성 |
| `AiReport/routers/AiReport.py` | `/api/v1/report` 엔드포인트 정의 |
| `AiReport/schemas/report_dto.py` | 일일 리포트 요청/응답 Pydantic DTO |
| `AiReport/core/report_config.py` | 일일 리포트 생성용 프롬프트 템플릿 |
| `AiReport/core/report_chain.py` | 일일 리포트용 LangChain 체인 구성 |
| `requirements.txt` | Python 패키지 의존성 목록 |
| `.env` | 로컬 환경 변수 파일. API 키 등 민감 정보 저장 |
| `ai_env/` | 로컬 Python 가상환경. 재생성 가능한 실행 환경 산출물 |
| `__pycache__/` | Python 바이트코드 캐시. 재생성 가능한 산출물 |

## 실행 준비

### 1. 가상환경 생성 및 활성화

```powershell
python -m venv ai_env
.\ai_env\Scripts\Activate.ps1
```

### 2. 패키지 설치

```powershell
pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트의 `.env` 파일에 OpenAI API 키를 설정합니다.

```env
OPENAI_API_KEY=your_openai_api_key
```

현재 코드는 `python-dotenv`의 `load_dotenv()`를 통해 `.env` 파일을 자동으로 로드합니다.

### 4. 서버 실행

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

실행 후 다음 주소에서 API 문서를 확인할 수 있습니다.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API 명세

### POST `/api/v1/analyze`

실시간 실내 센서 데이터, 외부 기상 데이터, 설치 인프라 정보, 현재 제어 상태, 알람 정보를 기반으로 환경 상태를 평가하고 제어 명령을 반환합니다.

#### Request Body

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `macAddress` | `string` | 분석 대상 기기의 MAC 주소 |
| `indoor` | `object` | 실내 센서 데이터 |
| `outdoor` | `object` | 외부 기상 데이터 |
| `setting` | `object` | 창문, 에어컨, 난방기, 공기청정기 등 인프라 설치 유무 |
| `control` | `object` | 현재 인프라 동작 상태 |
| `alert` | `object` | 현재 발생한 비정상 알람 정보 |

`indoor` 주요 필드는 `temperature`, `humidity`, `pressure`, `tvoc`, `eco2`, `flame`입니다.

`outdoor` 주요 필드는 `ta`, `wd`, `ws`, `hm`, `rn`, `isSW`, `isDW`입니다.

#### Response Body

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `macAddress` | `string` | 요청으로 들어온 MAC 주소 |
| `status.score` | `integer` | 실내 환경 통합 점수 |
| `status.severity` | `GOOD`, `NORMAL`, `BAD`, `TOO BAD` | 위험도 등급 |
| `summary.comment` | `string[]` | 환경 상태 분석 코멘트 |
| `summary.control_sum` | `string[]` | 제어 명령 요약 |
| `summary.todo` | `string[]` | 관리자/근무자 행동 지침 |
| `control` | `object` | 인프라별 제어 명령 |

`control` 값은 `true`, `false`, `null` 중 하나입니다. 설치되지 않은 인프라는 `null`로 반환되도록 프롬프트와 DTO가 구성되어 있습니다.

### POST `/api/v1/report`

하루 동안 집계된 센서 통계, 외부 기상 통계, 알람 목록, 기기별 가동 횟수/시간을 기반으로 일일 종합 리포트를 생성합니다.

#### Request Body

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `date` | `string` | 리포트 대상 날짜. `YYYY-MM-DD` 형식 |
| `sensor_summary` | `object` | 실내 센서별 일간 최솟값/최댓값/평균값 |
| `weather_summary` | `object` | 외부 기상별 일간 최솟값/최댓값/평균값 및 특보 이력 |
| `alarms` | `object[]` | 발생 알람 목록 |
| `controls` | `object` | 인프라별 가동 횟수와 총 가동 시간 |

`sensor_summary`는 `temperature`, `humidity`, `pressure`, `tvoc`, `eco2` 통계를 포함합니다.

`weather_summary`는 `temp_ta`, `wind_speed_ws`, `humidity_hm`, `precipitation_rn`, `is_strong_wind_warning`, `is_dry_warning`을 포함합니다.

#### Response Body

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `total_report` | `string` | 일일 종합 요약 리포트 |
| `alarm_key_notes` | `object[]` | 주요 알람 특이사항. 알람이 없으면 빈 배열 |
| `control_key_notes` | `object` | 기기별 가동 통계, 추정 에너지 사용량, 효율 코멘트 |

`control_key_notes.used_energy`는 프롬프트 기준으로 다음 공식을 사용해 산정됩니다.

```text
((에어컨 분 * 1.5) + (난방기 분 * 2.0) + (가습기 분 * 0.3) + (제습기 분 * 0.3) + (공기청정기 분 * 0.05)) / 60
```

## 동작 흐름

```text
Client 또는 Spring Boot Backend
        |
        v
FastAPI Router
        |
        v
Pydantic Request DTO 검증
        |
        v
LangChain PromptTemplate + ChatOpenAI
        |
        v
Pydantic Structured Output
        |
        v
FastAPI Response
```

## CORS 설정

`main.py`에서 모든 origin, method, header를 허용하도록 설정되어 있습니다.

```python
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

운영 환경에서는 허용 origin을 실제 프론트엔드/백엔드 도메인으로 제한하는 것을 권장합니다.

## 개발 메모

- 현재 테스트 코드는 포함되어 있지 않습니다.
- 라우터는 `/api/v1/analyze`, `/api/v1/report` 두 개가 등록되어 있습니다.
- OpenAPI 기본 문서 경로인 `/docs`, `/redoc`, `/openapi.json`도 함께 제공됩니다.
- `.env`, `ai_env/`, `__pycache__/`는 로컬 환경 또는 생성 산출물 성격이 강하므로 저장소 관리 시 민감 정보와 불필요한 파일 포함 여부를 확인하는 것이 좋습니다.
