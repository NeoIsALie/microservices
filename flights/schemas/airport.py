from typing import Annotated

from pydantic import BaseModel, constr


class Airport(BaseModel):
    name: Annotated[str, constr(max_length=255)]
    city: Annotated[str, constr(max_length=255)]
    country: Annotated[str, constr(max_length=255)]

