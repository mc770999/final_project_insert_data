from dataclasses import dataclass, field
from typing import List

@dataclass
class Date:
    day: int
    month: int
    year: int


    def __repr__(self):
        return (f"Date(day={self.day}, month={self.month}, "
                f"year={self.year})")
