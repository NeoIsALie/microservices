from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, constr


class Flight(BaseModel):
    flight_number: Annotated[str, constr(max_length=20)]
    datetime: datetime
    from_airport_id: int
    to_airport_id: int
    price: int
