from typing import Optional, List, Literal
from pydantic import BaseModel, Field

# -------[ 세부 Input DTO ]--------------------------------------

class IndoorData(BaseModel):
    """
    기기가 설치된 실내 환경 정보
    실내 환경 정보를 참고해 실내를 쾌적하고 안전하게 유지해야 함.
    """
    temperature: float = Field(description="실내 온도 (단위: 섭씨)")
    humidity: float = Field(description="실내 습도 (단위: %)")
    pressure: float = Field(description="실내 기압 (단위: hPa)")
    tvoc: int = Field(description="총 휘발성 유기화합물 수치 (단위: ppb, 수치가 높을수록 유해함, 500이상 주의, 1000이상 치명적)")
    eco2: int = Field(description="실내 이산화탄소 환산값 (단위: ppm, 정상치 400대, 수치가 높을수록 환기 필요, 1000이상 주의, 1500이상 치명적)")
    flame: int = Field(description="화염 센서 아날로그 수치 (0~1024, 값이 낮을수록 위험, 정상치 700 / 화재의심 500 / 화재 발생 300)")

class OutdoorData(BaseModel):
    """
    작업장 외부의 날씨 정보
    실내 정보와 더불어 실외 정보를 고려하여 실내 환경 인프라를 제어해야합니다.
    """
    ta: float = Field(description="외부 기온 (단위: 섭씨)")
    wd: float = Field(description="외부 풍향 (36방위)")
    ws: float = Field(description="외부 풍속 (단위: m/s)")
    hm: float = Field(description="외부 습도 (단위: %)")
    rn: float = Field(description="외부 1시간 강수량 (단위: mm)")
    isSW: bool = Field(description="강풍주의보 발효 여부 (True: 발효 중, False: 해제)")
    isDW: bool = Field(description="건조주의보 발효 여부 (True: 발효 중, False: 해제)")

class SettingData(BaseModel):
    """
    기기가 설치된 환경의 실내 환경 인프라 유무입니다..
    이 값이 False(또는 None)라면 해당 인프라는 존재하지 않으므로 제어해서는 안됩니다..
    """
    north_window: Optional[bool] = Field(description="북향 창문 존재 유무 (True: 있음, False: 없음)")
    south_window: Optional[bool] = Field(description="남향 창문 존재 유무")
    east_window: Optional[bool] = Field(description="동향 창문 존재 유무")
    west_window: Optional[bool] = Field(description="서향 창문 존재 유무")
    air_conditioner: Optional[bool] = Field(description="에어컨 설치 유무")
    heating: Optional[bool] = Field(description="난방기 설치 유무")
    humidifier: Optional[bool] = Field(description="가습기 설치 유무")
    dehumidifier: Optional[bool] = Field(description="제습기 설치 유무")
    air_cleaner: Optional[bool] = Field(description="공기청정기 설치 유무")
    sprinkler: Optional[bool] = Field(description="스프링클러 설치 유무")
    fire_alarm: Optional[bool] = Field(description="화재 경보기 설치 유무")

class ControlData(BaseModel):
    """
    설치된 실내 환경 인프라들의 '현재 동작 상태'를 나타냅니다.
    인프라들의 동작 상태를 확인하고 제어하여 실내 환경을 쾌적 및 안전하게 관리해야 합니다.
    """
    north_window: Optional[bool] = Field(description="북향 창문 현재 개폐 상태 (True: 열림, False: 닫힘)")
    south_window: Optional[bool] = Field(description="남향 창문 현재 개폐 상태")
    east_window: Optional[bool] = Field(description="동향 창문 현재 개폐 상태")
    west_window: Optional[bool] = Field(description="서향 창문 현재 개폐 상태")
    air_conditioner: Optional[bool] = Field(description="에어컨 현재 동작 상태 (True: ON, False: OFF)")
    heating: Optional[bool] = Field(description="난방기 현재 동작 상태")
    humidifier: Optional[bool] = Field(description="가습기 현재 동작 상태")
    dehumidifier: Optional[bool] = Field(description="제습기 현재 동작 상태")
    air_cleaner: Optional[bool] = Field(description="공기청정기 현재 동작 상태")
    sprinkler: Optional[bool] = Field(description="스프링클러 현재 동작 상태")
    fire_alarm: Optional[bool] = Field(description="화재 경보기 현재 동작 상태")

class AlertData(BaseModel):
    category: str = Field(description="비정상 상황이 발생한 센서 카테고리 (예: 'UNKNOWN', 'FIRE', 'TEMP', 'HUMIDITY', 'TVOC', 'ECO2')")
    severity: str = Field(description="발생한 알람의 위험도 (예: 'UNKNOWN', 'NORMAL', 'WARNING', 'CRITICAL')")


# -------[ Main Request DTO ]--------------------------------------

class AiRequestInput(BaseModel):
    """
    Spring Boot 백엔드로부터 전달받는 AI 분석 요청 데이터의 최상위 DTO입니다.
    """
    macAddress: str = Field(description="분석 대상 기기의 고유 MAC 주소")
    indoor: IndoorData = Field(description="실시간 실내 센서 측정 데이터")
    outdoor: OutdoorData = Field(description="해당 지역의 실시간 외부 날씨 및 기상특보 데이터")
    setting: SettingData = Field(description="해당 공간의 실내 환경 인프라 유무")
    control: ControlData = Field(description="해당 공간에 존재하는 실내 환경 인프라들의 동작 상태")
    alert: AlertData = Field(description="현재 발생한 비정상 데이터 알람의 상세 정보")


# -------[ 세부 Output DTO ]--------------------------------------

class StatusOutput(BaseModel):
    score: int = Field(description="실내 환경 통합 점수 (0~100 사이의 정수. 높을수록 우수하고 쾌적함)")
    severity: Literal["GOOD", "NORMAL", "BAD", "TOO BAD"] = Field(
        description="현재 실내 환경 위험도 등급. 반드시 'GOOD', 'NORMAL', 'BAD', 'TOO BAD' 중 하나로 출력"
    )

class SummaryOutput(BaseModel):
    comment: List[str] = Field(
        description="실내 환경에 대한 종합 평가 코멘트 (각 문장을 요소로 하는 3개 내외의 문자열 리스트)"
    )
    control_sum: List[str] = Field(
        description="실내 환경 인프라 제어 명령에 대한 요약 및 이유 (예: '온도를 낮추기 위해 에어컨을 가동합니다.', 3개 내외의 리스트)"
    )
    todo: List[str] = Field(
        description="근무자 및 관리자가 직접 수행해야 할 권장 행동 지침 (예: '현장 작업자들을 대피시키세요.', 3개 내외의 리스트)"
    )

class ControlOutput(BaseModel):
    """
    LLM이 판단한 최종 실내 환경 인프라 제어 명령.
    주의: Input의 'setting(인프라 유무)' 데이터에서 False나 null로 전달된 기기는
    설치되지 않은 기기이므로 반드시 null(None)로 반환.
    """
    north_window: Optional[bool] = Field(description="북향 창문 개폐 제어 (True: 열기, False: 닫기, 변경 없음/기기 없음: null)")
    south_window: Optional[bool] = Field(description="남향 창문 개폐 제어 (True: 열기, False: 닫기, 변경 없음/기기 없음: null)")
    east_window: Optional[bool] = Field(description="동향 창문 개폐 제어")
    west_window: Optional[bool] = Field(description="서향 창문 개폐 제어")
    air_conditioner: Optional[bool] = Field(description="에어컨 제어 명령 (True: ON, False: OFF, 변경 없음/기기 없음: null)")
    heating: Optional[bool] = Field(description="난방기 제어 명령")
    humidifier: Optional[bool] = Field(description="가습기 제어 명령")
    dehumidifier: Optional[bool] = Field(description="제습기 제어 명령")
    air_cleaner: Optional[bool] = Field(description="공기청정기 제어 명령")
    sprinkler: Optional[bool] = Field(description="스프링클러 제어 명령")
    fire_alarm: Optional[bool] = Field(description="화재 경보기 제어 명령")

# -------[ Main Response DTO ]--------------------------------------

class AiResponseOutput(BaseModel):
    """
    LLM이 최종적으로 반환해야 하는 JSON 규격이며 해당 형태를 반드시 지켜야합니다.
    """
    macAddress: str = Field(description="분석 대상 기기의 고유 MAC 주소, Input으로 들어온 값을 그대로 반환")
    status: StatusOutput = Field(description="실내 환경 쾌적함, 안전 등을 종합 평가한 점수 및 등급")
    summary: SummaryOutput = Field(description="실내 환경 평가, 제어 요약 및 행동 지침 리스트")
    control: ControlOutput = Field(description="실내 환경 인프라 제어 명령값")