from dataclasses import dataclass, asdict
from datetime import datetime



#Class for every crosshair
@dataclass
class Crosshair:
    name: str
    code: str
    created_at: str = None
    is_active: bool = True  

    def __post_init__(self):

        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return asdict(self)