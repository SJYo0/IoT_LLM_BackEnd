from fastapi import APIRouter, HTTPException
from AiReport.schemas.report_dto import AiReportResponseOutput, AiReportRequestInput

from AiReport.core.report_chain import report_chain

router = APIRouter(
    tags=["AI Report"]
)
@router.post("/api/v1/report", response_model=AiReportResponseOutput)
async def create_daily_report(request_data: AiReportRequestInput):
    try:
        result = await report_chain.ainvoke({
            "input_data": request_data.model_dump_json()
        })

        return result

    except Exception as e:
        print(f"[ERROR] AI 리포트 생성 프로세스 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI 리포트 생성 중 오류가 발생했습니다: {str(e)}"
        )