from dacite import from_dict
from dataclasses import asdict, dataclass
import yaml



@dataclass(frozen=True)
class DictLoader:
    @classmethod
    def from_dict(cls, data):
        return from_dict(data_class=cls, data=data)

    def to_dict(self):
        return asdict(self)

class YamlReader:
    @staticmethod
    def from_file(file, cls=None)->dict:
        with open(file, "r") as fp:
            text = fp.read()
            obj = yaml.safe_load(text)
        
        if cls:
            obj = cls(obj)
        return obj