#pydantic

from pydantic import BaseModel, Field
from typing import Optional, List


class IdeaInput(BaseModel):
    niche : str = Field(
        ..., 
        min_length=2,
        max_length=100,
        description="e.g. Fitness, food, tech, education"
    )

    details : str = Field(
        ...,
        min_length=20,
        description="Long-form description of the idea"
    )

    skill : int = Field(
        ...,
        ge=1,
        le=10,
        description="Self Rated skill level from 1 (beginner) - 10 (expert)"
    )                           

    skill_details : str = Field(

        ...,

        min_length= 20,
        description= "Describe your relevant experience or background"
    )

class LocalBusiness(BaseModel):
    name: str = Field(..., description="Name of the local business")
    type: str = Field(..., description="Type of business e.g. gym, clinic, restaurant")
    url: Optional[str] = Field(default=None, description="Google Maps URL of the business")


class ProjectIdea(BaseModel):
    model_config = {"frozen": False}
    name: str = Field(..., min_length=3, max_length=100, description="Name of the project idea")
    description: str = Field(..., min_length=20, description="Brief description of the project")
    potential_client: str = Field(..., description="Type of client this idea targets e.g. local gym owners, mid-size retailers")
    is_local: bool = Field(..., description="Whether this idea can target local businesses")
    local_businesses: Optional[List[LocalBusiness]] = Field(
        default=None,
        description="List of local businesses only populated if is_local is True"
    )
    business_type: Optional[str] = Field(
    default=None,
    description="Type of local business to search e.g. gym, clinic, restaurant"
)

class IdeaOutput(BaseModel):
    ideas: List[ProjectIdea] = Field(
        ...,
        min_length=5,
        max_length=5,
        description="Always 5 project ideas"
    )