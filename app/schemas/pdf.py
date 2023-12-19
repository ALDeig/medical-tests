from typing import Any

from pydantic import BaseModel, field_validator


class SResearchValue(BaseModel):
    result: str 
    units: str
    reference_value: str
    comment: str | None

    # @field_validator("result", mode="before")
    # @classmethod
    # def validate_result(cls, v: Any):
    #     try:
    #         return float(v)
    #     except ValueError:
    #         result = ""
    #         for i in v:
    #             if i.isdigit() or i == ".":
    #                 result += i
    #         if result:
    #             return float(result)
