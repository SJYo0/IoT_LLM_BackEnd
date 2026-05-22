from typing import Optional, List, Dict
from pydantic import BaseModel, Field

# --------------------------[ 세부 Input DTO ]---------------------------------

class MinMaxAvg(BaseModel):
    min: float = Field(description="일간 최솟값")
    max: float = Field(description="일간 최댓값")
    avg: float = Field(description="일간 평균값")

class SensorSummary(BaseModel):
    """오늘 하루 동안 수집된 실내 센서 데이터의 통계 요약"""
    temperature: MinMaxAvg = Field(description="실내 온도 통계 (단위: 섭씨)")
    humidity: MinMaxAvg = Field(description="실내 습도 통계 (단위: %)")
    pressure: MinMaxAvg = Field(description="실내 기압 통계 (단위: hPa)")
    tvoc: MinMaxAvg = Field(description="총 휘발성 유기화합물 통계 (단위: ppb)")
    eco2: MinMaxAvg = Field(description="이산화탄소 환산값 통계 (단위: ppm)")

class WeatherSummary(BaseModel):
    """오늘 하루 동안의 실외 기상 데이터 통계 및 특보 내역"""
    temp_ta: MinMaxAvg = Field(description="외부 기온 통계 (단위: 섭씨)")
    wind_speed_ws: MinMaxAvg = Field(description="외부 풍속 통계 (단위: m/s)")
    humidity_hm: MinMaxAvg = Field(description="외부 습도 통계 (단위: %)")
    precipitation_rn: MinMaxAvg = Field(description="외부 강수량 통계 (단위: mm)")
    is_strong_wind_warning: bool = Field(description="하루 중 강풍주의보 발효 이력 유무 (True: 발효됨)")
    is_dry_warning: bool = Field(description="하루 중 건조주의보 발효 이력 유무 (True: 발효됨)")

class AlarmInfo(BaseModel):
    """발생했던 개별 알람 내역"""
    start_time: str = Field(description="알람 발생 시각 (HH:mm:ss)")
    end_time: str = Field(description="알람 상황 종료 시각 (HH:mm:ss) 또는 'Not Resolved'")
    category: str = Field(description="알람 카테고리 (예: FIRE, TEMP, HUMIDITY, TVOC, ECO2)")
    severity: str = Field(description="위험도 (WARNING, CRITICAL)")

class ControlSummaryInput(BaseModel):
    """기기별 가동 횟수 및 시간"""
    count: int = Field(description="하루 동안 켜진 횟수")
    runtime: int = Field(description="하루 총 가동 시간 (단위: 분)")

class AiReportRequestInput(BaseModel):
    date: str = Field(description="리포트 대상 날짜 (YYYY-MM-DD)")
    sensor_summary: SensorSummary = Field(description="실내 환경 데이터 통계")
    weather_summary: WeatherSummary = Field(description="실외 기상 데이터 통계")
    alarms: List[AlarmInfo] = Field(description="오늘 발생한 알람 내역 리스트 (최대 20개)")
    controls: Dict[str, ControlSummaryInput] = Field(
        description="인프라별(air_conditioner, heating 등) 가동 횟수 및 가동 시간 맵"
    )


# -----------------------------[ 세부 Output DTO ]-------------------------------

class AlarmKeyNote(BaseModel):
    title: str = Field(description="주요 알람 특이사항 요약 제목")
    content: str = Field(description="해당 알람의 상세 내용 및 원인 분석 (100자 내외)")

class ApplianceStat(BaseModel):
    count: int = Field(description="가동 횟수 (Input 값을 그대로 반환)")
    runtime: int = Field(description="총 가동 시간 (Input 값을 그대로 반환, 단위: 분)")

class ControlKeyNotes(BaseModel):
    """제어 통계 및 에너지 분석 결과"""
    air_conditioner: ApplianceStat
    heating: ApplianceStat
    humidifier: ApplianceStat
    dehumidifier: ApplianceStat
    air_cleaner: ApplianceStat
    used_energy: float = Field(
        description="각 기기의 런타임을 바탕으로 추정한 오늘 총 에너지 사용량 (단위: kWh). "
                    "에어컨(1.5kW), 난방기(2.0kW), 가습/제습기(0.3kW), 공청기(0.05kW) 기준으로 시간당 전력량을 임의 계산할 것."
    )
    comment: str = Field(
        description="AI 제어 효율에 대한 코멘트. 날씨와 비교하여 에너지를 잘 절약했는지, 내일은 어떻게 제어해야 효율적인지 제안 (200자 내외)"
    )

class AiReportResponseOutput(BaseModel):
    total_report: str = Field(
        description="실내외 환경 통계, 알람 발생 빈도, 기기 제어 효율을 모두 종합한 '오늘의 AI 종합 요약 리포트' (500자 내외), 가독성을 위해 '\n'을 사용할 것"
    )
    alarm_key_notes: List[AlarmKeyNote] = Field(
        description="가장 심각했거나 주의 깊게 봐야 할 주요 알람 특이사항. 최대 4개까지 반환. 알람이 없었다면 빈 리스트([]) 반환."
    )
    control_key_notes: ControlKeyNotes = Field(description="에너지 사용량 및 효율 코멘트")