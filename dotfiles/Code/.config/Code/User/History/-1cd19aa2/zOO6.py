# Data

banks = {
    "Axis": {
        "bands": [
            (800, 900, 7.3),
            (780, 799, 7.5),
            (750, 779, 7.55),
            (730, 749, 7.65),
            (0, 729, 7.75),
            (-1, 0, 7.75),
        ],
        "concessions": {"Maxgain": 0.25},
    },
    "BOB": {
        "bands": [
            (825, 900, 7.25),
            (800, 824, 7.35),
            (760, 799, 7.45),
            (726, 759, 7.70),
            (701, 725, 7.75),
            (0, 700, 0),
            (-1, 0, 7.8),
        ],
        "concessions": {
            "Insurance": -0.05,
            "BT": -0.10,
            "Women": -0.05,
            "Below40": -0.10,
            "OD>75L": 0.25,
        },
    },
    "BOI": {
        "bands": [
            (840, 900, 7.10),
            (800, 839, 7.25),
            (760, 799, 7.40),
            (725, 759, 7.90),
            (700, 724, 8.40),
            (0, 699, 10.00),
            (-1, 0, 7.90),
        ],
        "concessions": {
            "Self-employed_726-799": 0.10,
            "Self-employed_700-724": 0.05,
            "BT": -0.10,
            "OD_>2cr": 0.25,
        },
    },
    "BOM": {
        "bands": [
            (800, 900, 7.10),
            (750, 799, 7.25),
            (725, 749, 7.70),
            (700, 724, 7.75),
            (650, 699, 8.35),
            (600, 649, 8.75),
            (0, 599, 9.15),
            (-1, 0, 7.70),
        ],
        "concessions": {
            "Self-employed_725-850": 0.10,
            "Self-employed_600-724": 0.20,
            "Self-employed_<600": 0.50,
            "Self-employed_-1": 0.20,
            "OD": 0.25,
        },
    },
    "HDFC": {
        "bands": [(800, 900, 7.15), (780, 799, 7.20), (750, 779, 7.25), (0, 749, 0)],
        "concessions": {"UC_>800": -0.05, "UC_<800": -0.10},
    },
    "ICICI": {
        "bands": [
            (800, 900, 7.40),
            (750, 799, 7.50),
            (730, 749, 7.85),
            (700, 729, 8.00),
            (0, 699, 0),
            (-1, 0, 7.85),
        ],
        "concessions": {
            ">75-199_>800": 0.10,
            "<75_>800": 0.15,
            ">75-199_750-799": 0.25,
            "<75_750-799": 0.25,
            ">75-199_730-749": 0.05,
            "<75_730-749": 0.10,
            ">75-199_700-729": 0.25,
            "<75_700-729": 0.30,
            ">75-199_-1": 0.05,
            "<75_-1": 0.10,
            "Self-employed_All": 0.25,
            "OD": 0.40,
        },
    },
    "PNB": {
        "bands": [(800, 900, 7.20), (750, 799, 7.25), (0, 749, 0)],
        "concessions": {},
    },
}


# Functions
def get_base_roi(bank: str, cibil: int, banks):
    for low, high, roi in banks[bank]["bands"]:
        if low <= cibil <= high:
            return roi
    return None


def get_final_roi(bank: str, cibil: int, banks, applied_concessions=None):
    base_roi = get_base_roi(bank, cibil, banks)
    if base_roi is None:
        return None

    total_adj = 0
    if applied_concessions:
        for name in applied_concessions:
            total_adj += banks[bank]["concessions"].get(name, 0)

    return base_roi + total_adj


def roi(cibil: int, banks, applied_concessions=None):
    result = {}

    for bank in banks:
        result[bank] = get_final_roi(bank, cibil, banks, applied_concessions)

    return result


# Result
concessions = ["Women", "Below40", "UC_<800"]

cibil = 799

print("BASE RATE:")
for bank in banks:
    print(bank, "", get_base_roi(bank, cibil, banks))

print("CONCESSION:")
for bank in banks:
    print(bank, "", get_final_roi(bank, cibil, banks, concessions))
print("\n")
print(roi(cibil, banks, concessions))
