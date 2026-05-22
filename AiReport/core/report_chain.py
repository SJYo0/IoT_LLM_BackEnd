import json
from AiReport.schemas.report_dto import AiReportResponseOutput, AiReportRequestInput
from AiReport.core.report_config import PROMPT_REPORT_TEXT

#-------[LangChain Core]--------------------
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

#-------------------------------------------
from dotenv import load_dotenv
load_dotenv()
#-------------------------------------------

# AI 환경 평가 및 인프라 제어 chain

llm = ChatOpenAI(
    model="gpt-5.4",
    temperature=0.1
)

structured_llm = llm.with_structured_output(AiReportResponseOutput)

input_schema_str = json.dumps(
    AiReportRequestInput.model_json_schema(),
    ensure_ascii=False,
    indent=2
)

report_prompt = PromptTemplate(
    template=PROMPT_REPORT_TEXT,
    input_variables=["input_data"],
    partial_variables={
        "input_schema": input_schema_str, # input 설명 작성
        "format_instructions": "반드시 제공된 출력 스키마(Function Calling)에 맞추어 답변하십시오."
    }
)

def get_report_chain(
        prompt: PromptTemplate,
        model
) -> RunnableSequence:
    chain = prompt | model
    return chain

report_chain = get_report_chain(
    prompt=report_prompt,
    model=structured_llm
)