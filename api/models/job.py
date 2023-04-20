from pydantic import BaseModel

class Job(BaseModel):
    JOB_ID: str
    JOB_TITLE: str
    JOB_ACTIVEDATE: str
    DATE_VIEW: str
    EMP_NAME: str
    BENEFIT_NAME: str
    LINK_JOB: str
    JOB_SALARY_STRING: str
    LOCATION_NAME_ARR: [str]