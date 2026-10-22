from pydantic import BaseModel
from typing import Optional


class BlogState(BaseModel):
    ##user Input
    topic: str =""
    audience : str = "general"
    research: Optional[str] = None

    ##Researher Output
    reseacher : str = ""
    research_feedback : str = ""

    ##Writter Output
    draft : str = ""
    draft_feedback : str = ""

    ##Editor Output
    final_blog : str = ""

    ##MetaData
    revision_count : int = 0