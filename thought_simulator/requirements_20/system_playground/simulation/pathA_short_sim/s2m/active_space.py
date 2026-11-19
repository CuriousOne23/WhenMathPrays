from typing import List

from s2m.loader import load_active_space, load_majors


def resolve_active_space(space_name: str = "default") -> List[str]:
    known_majors = load_majors()
    if not known_majors:
        return load_active_space(space_name)

    requested = load_active_space(space_name)
    if not requested:
        return known_majors

    known_set = set(known_majors)
    active: List[str] = []
    for major in requested:
        if major in known_set and major not in active:
            active.append(major)
    return active

