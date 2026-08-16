from dataclasses import dataclass, field

@dataclass
class CIBILBand:
    min_cibil: int
    max_cibil: int
    roi: float


@dataclass
class Concession:
    key: str
    label: str
    adjustment: float
    aliases: list[str] | None = None


@dataclass
class BankRates:
    name: str
    bands: list[CIBILBand]
    concessions: list[Concession]
    max_concession: float | None = None
    lowest_rate: float | None = None

    def get_base_roi(self, cibil: int) -> float | None:
        for band in self.bands:
            if band.min_cibil <= cibil <= band.max_cibil:
                return band.roi
        return None

    def get_final_roi(self, cibil: int, concession_keys: list[str] | None = None) -> float | None:
        base = self.get_base_roi(cibil)
        if base is None:
            return None

        adj = 0.0
        if concession_keys:
            lookup = {}
            alias_map = {}
            for c in self.concessions:
                lookup[c.key] = c.adjustment
                if c.aliases:
                    for alias in c.aliases:
                        alias_map[alias] = c.key
            for key in concession_keys:
                actual = alias_map.get(key, key)
                adj += lookup.get(actual, 0.0)

        if self.max_concession is not None:
            adj = max(adj, -self.max_concession)

        result = base + adj
        if self.lowest_rate is not None:
            result = max(result, self.lowest_rate)
        return result


def build_rate_card() -> list[BankRates]:
    return [
        BankRates(
            name="Axis",
            bands=[
                CIBILBand(800, 900, 7.3),
                CIBILBand(780, 799, 7.5),
                CIBILBand(750, 779, 7.55),
                CIBILBand(730, 749, 7.65),
                CIBILBand(0, 729, 7.75),
                CIBILBand(-1, 0, 7.75),
            ],
            concessions=[Concession("maxgain", "Axis Maxgain product", 0.25, aliases=["overdraft"])],
        ),
        BankRates(
            name="BOB",
            bands=[
                CIBILBand(825, 900, 7.25),
                CIBILBand(800, 824, 7.35),
                CIBILBand(760, 799, 7.45),
                CIBILBand(726, 759, 7.70),
                CIBILBand(701, 725, 7.75),
                CIBILBand(0, 700, 0),
                CIBILBand(-1, 0, 7.8),
            ],
            concessions=[
                Concession("insurance", "Insurance discount", -0.05),
                Concession("balanceTransfer", "Balance transfer discount", -0.10),
                Concession("womenBorrower", "Women borrower discount", -0.05),
                Concession("ageBelow40", "Age below 40 discount", -0.10),
                Concession("overdraftLoanGt75L", "Overdraft with loan above 75L", 0.25, aliases=["overdraft"]),
            ],
            max_concession=0.1,
            lowest_rate=7.2,
        ),
        BankRates(
            name="BOI",
            bands=[
                CIBILBand(840, 900, 7.10),
                CIBILBand(800, 839, 7.25),
                CIBILBand(760, 799, 7.40),
                CIBILBand(725, 759, 7.90),
                CIBILBand(700, 724, 8.40),
                CIBILBand(0, 699, 10.00),
                CIBILBand(-1, 0, 7.90),
            ],
            concessions=[
                Concession("selfEmployed_cibil726_799", "Self-employed with CIBIL 726-799", 0.10),
                Concession("selfEmployed_cibil700_724", "Self-employed with CIBIL 700-724", 0.05),
                Concession("balanceTransfer", "Balance transfer discount", -0.10),
                Concession("overdraftLoanGt2Cr", "Overdraft with loan above 2Cr", 0.25, aliases=["overdraft"]),
            ],
        ),
        BankRates(
            name="BOM",
            bands=[
                CIBILBand(800, 900, 7.10),
                CIBILBand(750, 799, 7.25),
                CIBILBand(725, 749, 7.70),
                CIBILBand(700, 724, 7.75),
                CIBILBand(650, 699, 8.35),
                CIBILBand(600, 649, 8.75),
                CIBILBand(0, 599, 9.15),
                CIBILBand(-1, 0, 7.70),
            ],
            concessions=[
                Concession("selfEmployed_cibil725_850", "Self-employed with CIBIL 725-850", 0.10),
                Concession("selfEmployed_cibil600_724", "Self-employed with CIBIL 600-724", 0.20),
                Concession("selfEmployed_cibilLt600", "Self-employed with CIBIL below 600", 0.50),
                Concession("selfEmployed_noCibil", "Self-employed no-score/default", 0.20),
                Concession("overdraft", "Overdraft product", 0.25, aliases=["maxgain"]),
            ],
        ),
        BankRates(
            name="HDFC",
            bands=[
                CIBILBand(800, 900, 7.15),
                CIBILBand(780, 799, 7.20),
                CIBILBand(750, 779, 7.25),
                CIBILBand(0, 749, 0),
            ],
            concessions=[
                Concession("underConstructionCibilGt800", "Under-construction with CIBIL above 800", 0.05),
                Concession("underConstructionCibilLt800", "Under-construction with CIBIL below 800", 0.10),
            ],
        ),
        BankRates(
            name="ICICI",
            bands=[
                CIBILBand(800, 900, 7.40),
                CIBILBand(750, 799, 7.50),
                CIBILBand(730, 749, 7.85),
                CIBILBand(700, 729, 8.00),
                CIBILBand(0, 699, 0),
                CIBILBand(-1, 0, 7.85),
            ],
            concessions=[
                Concession("property75_199CibilGt800", "Property 75-199L, CIBIL above 800", 0.10),
                Concession("propertyLt75CibilGt800", "Property below 75L, CIBIL above 800", 0.15),
                Concession("property75_199Cibil750_799", "Property 75-199L, CIBIL 750-799", 0.25),
                Concession("propertyLt75Cibil750_799", "Property below 75L, CIBIL 750-799", 0.25),
                Concession("property75_199Cibil730_749", "Property 75-199L, CIBIL 730-749", 0.05),
                Concession("propertyLt75Cibil730_749", "Property below 75L, CIBIL 730-749", 0.10),
                Concession("property75_199Cibil700_729", "Property 75-199L, CIBIL 700-729", 0.25),
                Concession("propertyLt75Cibil700_729", "Property below 75L, CIBIL 700-729", 0.30),
                Concession("property75_199NoCibil", "Property 75-199L, no CIBIL", 0.05),
                Concession("propertyLt75NoCibil", "Property below 75L, no CIBIL", 0.10),
                Concession("selfEmployed", "Self-employed", 0.25),
                Concession("overdraft", "Overdraft product", 0.40, aliases=["maxgain"]),
            ],
        ),
        BankRates(
            name="PNB",
            bands=[
                CIBILBand(800, 900, 7.20),
                CIBILBand(750, 799, 7.25),
                CIBILBand(0, 749, 0),
            ],
            concessions=[],
        ),
    ]


# Convenience lookups

def get_base_roi(banks: list[BankRates], bank_name: str, cibil: int) -> float | None:
    for b in banks:
        if b.name == bank_name:
            return b.get_base_roi(cibil)
    return None


def get_final_roi(banks: list[BankRates], bank_name: str, cibil: int, concession_keys: list[str] | None = None) -> float | None:
    for b in banks:
        if b.name == bank_name:
            return b.get_final_roi(cibil, concession_keys)
    return None


def roi_all(banks: list[BankRates], cibil: int, concession_keys: list[str] | None = None) -> dict[str, float | None]:
    return {b.name: b.get_final_roi(cibil, concession_keys) for b in banks}


# Demo
if __name__ == "__main__":
    banks = build_rate_card()
    cibil = 801
    concessions = ["womenBorrower", "ageBelow40", "underConstructionCibilLt800"]

    print("BASE RATES:")
    for b in banks:
        print(f"  {b.name}: {b.get_base_roi(cibil)}")

    print("\nWITH CONCESSIONS:")
    for b in banks:
        print(f"  {b.name}: {b.get_final_roi(cibil, concessions)}")

    print("\nALL BANKS:")
    print(roi_all(banks, cibil, concessions))
