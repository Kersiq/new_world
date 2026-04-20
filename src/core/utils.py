from dataclasses import dataclass, asdict


@dataclass
class ReturnAsDictUtils:

    def to_dict(self):
        return asdict(self)
