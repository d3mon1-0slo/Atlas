# calls LLM 


from fastapi import APIRouter, HTTPException

from models.model import IdeaInput

from services.ai_service import CALL_LLM
from services.scraper_service import GET_BUSINESSES

router = APIRouter()
generate_path = CALL_LLM()
scrape = GET_BUSINESSES()


@router.post('/generate')
async def generate_projct(data: IdeaInput):
    response = await generate_path.generate_project(data)
    for project in response.ideas:
        if project.business_type and project.business_type != "null":
            project.is_local = True
            businesses = await scrape.get_business(project.business_type)
            project.local_businesses = businesses
        else:
            project.is_local = False
            project.local_businesses = None

    return {
        "Response": "Success",
        "Data": response
    }
 
@router.get("/get_business")
async def get_business():
    try:
        z = await scrape.get_business("gym")
        print(z)
        return {
            "Status" : "True"
        }
    except Exception:
        return {
            "Status" : "Failed"
        }

@router.post("/validate")
async def validate_idea():
    return {
        "Status" : "Validated"
    }