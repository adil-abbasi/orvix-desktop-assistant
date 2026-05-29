from pathlib import Path

SOFTWARE_INDEX = {}


SEARCH_LOCATIONS = [
    Path("C:/Program Files"),
    Path("C:/Program Files (x86)")
]


def build_software_index():

    global SOFTWARE_INDEX

    SOFTWARE_INDEX = {}

    for root in SEARCH_LOCATIONS:

        if not root.exists():
            continue

        try:
            for exe in root.rglob("*.exe"):

                name = exe.stem.lower().strip()

                if name not in SOFTWARE_INDEX:
                    SOFTWARE_INDEX[name] = exe

        except Exception:
            pass

    return SOFTWARE_INDEX


def find_software(name):

    if not SOFTWARE_INDEX:
        build_software_index()

    query = name.lower().strip()

    if query in SOFTWARE_INDEX:
        return SOFTWARE_INDEX[query]

    return None