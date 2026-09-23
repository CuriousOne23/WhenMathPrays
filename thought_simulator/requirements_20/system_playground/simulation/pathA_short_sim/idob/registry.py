from typing import List

from idob.legacy import legacy_monolith
from idob.object import IdOBObject


def build_r1_registry() -> List[IdOBObject]:
    return [legacy_monolith]


registry = build_r1_registry()
