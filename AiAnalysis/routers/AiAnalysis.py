from fastapi import APIRouter, HTTPException
from AiAnalysis.schemas.analysis_dto import AiRequestInput, AiResponseOutput
from AiAnalysis.core.analysis_chain import analysis_chain

router = APIRouter(
    tags=["AI Analysis"]
)
@router.post("/api/v1/analyze", response_model=AiResponseOutput)
async def analyze_sensor_data(request_data: AiRequestInput):
    try:
        result = await analysis_chain.ainvoke({
            "input_data": request_data.model_dump_json()
        })

        return result

    except Exception as e:
        print(f"[ERROR] AI 분석 프로세스 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI 분석 중 오류가 발생했습니다: {str(e)}"
        )