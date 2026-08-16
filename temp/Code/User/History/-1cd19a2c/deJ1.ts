interface CIBILBand {
  minCibil: number;
  maxCibil: number;
  roi: number;
}

interface Concession {
  key: string;
  label: string;
  adjustment: number;
  aliases?: string[];
}

class BankRates {
  readonly name: string;
  readonly bands: CIBILBand[];
  readonly concessions: Concession[];
  readonly maxConcession?: number;
  readonly lowestRate?: number;

  constructor(opts: {
    name: string;
    bands: CIBILBand[];
    concessions: Concession[];
    maxConcession?: number;
    lowestRate?: number;
  }) {
    this.name = opts.name;
    this.bands = opts.bands;
    this.concessions = opts.concessions;
    this.maxConcession = opts.maxConcession;
    this.lowestRate = opts.lowestRate;
  }

  getBaseROI(cibil: number): number | null {
    for (const band of this.bands) {
      if (cibil >= band.minCibil && cibil <= band.maxCibil) {
        return band.roi;
      }
    }
    return null;
  }

  getFinalROI(cibil: number, concessionKeys?: string[]): number | null {
    const base = this.getBaseROI(cibil);
    if (base === null) return null;

    let adj = 0;
    if (concessionKeys) {
      const lookup: Record<string, number> = {};
      const aliasMap: Record<string, string> = {};
      for (const c of this.concessions) {
        lookup[c.key] = c.adjustment;
        if (c.aliases) {
          for (const alias of c.aliases) aliasMap[alias] = c.key;
        }
      }
      for (const key of concessionKeys) {
        const actual = aliasMap[key] ?? key;
        adj += lookup[actual] ?? 0;
      }
    }

    if (this.maxConcession !== undefined) adj = Math.max(adj, -this.maxConcession);

    let result = base + adj;
    if (this.lowestRate !== undefined) result = Math.max(result, this.lowestRate);
    return result;
  }
}

function getBaseROI(banks: BankRates[], bankName: string, cibil: number): number | null {
  for (const b of banks) {
    if (b.name === bankName) return b.getBaseROI(cibil);
  }
  return null;
}

function getFinalROI(banks: BankRates[], bankName: string, cibil: number, concessionKeys?: string[]): number | null {
  for (const b of banks) {
    if (b.name === bankName) return b.getFinalROI(cibil, concessionKeys);
  }
  return null;
}

function roiAll(banks: BankRates[], cibil: number, concessionKeys?: string[]): Record<string, number | null> {
  const result: Record<string, number | null> = {};
  for (const b of banks) result[b.name] = b.getFinalROI(cibil, concessionKeys);
  return result;
}

function buildRateCard(): BankRates[] {
  return [
    new BankRates({
      name: "Axis",
      bands: [
        { minCibil: 800, maxCibil: 900, roi: 7.3 },
        { minCibil: 780, maxCibil: 799, roi: 7.5 },
        { minCibil: 750, maxCibil: 779, roi: 7.55 },
        { minCibil: 730, maxCibil: 749, roi: 7.65 },
        { minCibil: 0, maxCibil: 729, roi: 7.75 },
        { minCibil: -1, maxCibil: 0, roi: 7.75 },
      ],
      concessions: [{ key: "maxgain", label: "Axis Maxgain product", adjustment: 0.25, aliases: ["overdraft"] }],
    }),
    new BankRates({
      name: "BOB",
      bands: [
        { minCibil: 825, maxCibil: 900, roi: 7.25 },
        { minCibil: 800, maxCibil: 824, roi: 7.35 },
        { minCibil: 760, maxCibil: 799, roi: 7.45 },
        { minCibil: 726, maxCibil: 759, roi: 7.70 },
        { minCibil: 701, maxCibil: 725, roi: 7.75 },
        { minCibil: 0, maxCibil: 700, roi: 0 },
        { minCibil: -1, maxCibil: 0, roi: 7.8 },
      ],
      concessions: [
        { key: "insurance", label: "Insurance discount", adjustment: -0.05 },
        { key: "balanceTransfer", label: "Balance transfer discount", adjustment: -0.10 },
        { key: "womenBorrower", label: "Women borrower discount", adjustment: -0.05 },
        { key: "ageBelow40", label: "Age below 40 discount", adjustment: -0.10 },
        { key: "overdraftLoanGt75L", label: "Overdraft with loan above 75L", adjustment: 0.25, aliases: ["maxgain"] },
      ],
      maxConcession: 0.1,
      lowestRate: 7.2,
    }),
    new BankRates({
      name: "BOI",
      bands: [
        { minCibil: 840, maxCibil: 900, roi: 7.10 },
        { minCibil: 800, maxCibil: 839, roi: 7.25 },
        { minCibil: 760, maxCibil: 799, roi: 7.40 },
        { minCibil: 725, maxCibil: 759, roi: 7.90 },
        { minCibil: 700, maxCibil: 724, roi: 8.40 },
        { minCibil: 0, maxCibil: 699, roi: 10.00 },
        { minCibil: -1, maxCibil: 0, roi: 7.90 },
      ],
      concessions: [
        { key: "selfEmployed_cibil726_799", label: "Self-employed with CIBIL 726-799", adjustment: 0.10 },
        { key: "selfEmployed_cibil700_724", label: "Self-employed with CIBIL 700-724", adjustment: 0.05 },
        { key: "balanceTransfer", label: "Balance transfer discount", adjustment: -0.10 },
        { key: "overdraftLoanGt2Cr", label: "Overdraft with loan above 2Cr", adjustment: 0.25, aliases: ["overdraft"] },
      ],
    }),
    new BankRates({
      name: "BOM",
      bands: [
        { minCibil: 800, maxCibil: 900, roi: 7.10 },
        { minCibil: 750, maxCibil: 799, roi: 7.25 },
        { minCibil: 725, maxCibil: 749, roi: 7.70 },
        { minCibil: 700, maxCibil: 724, roi: 7.75 },
        { minCibil: 650, maxCibil: 699, roi: 8.35 },
        { minCibil: 600, maxCibil: 649, roi: 8.75 },
        { minCibil: 0, maxCibil: 599, roi: 9.15 },
        { minCibil: -1, maxCibil: 0, roi: 7.70 },
      ],
      concessions: [
        { key: "selfEmployed_cibil725_850", label: "Self-employed with CIBIL 725-850", adjustment: 0.10 },
        { key: "selfEmployed_cibil600_724", label: "Self-employed with CIBIL 600-724", adjustment: 0.20 },
        { key: "selfEmployed_cibilLt600", label: "Self-employed with CIBIL below 600", adjustment: 0.50 },
        { key: "selfEmployed_noCibil", label: "Self-employed no-score/default", adjustment: 0.20 },
        { key: "overdraft", label: "Overdraft product", adjustment: 0.25, aliases: ["maxgain"] },
      ],
    }),
    new BankRates({
      name: "HDFC",
      bands: [
        { minCibil: 800, maxCibil: 900, roi: 7.15 },
        { minCibil: 780, maxCibil: 799, roi: 7.20 },
        { minCibil: 750, maxCibil: 779, roi: 7.25 },
        { minCibil: 0, maxCibil: 749, roi: 0 },
      ],
      concessions: [
        { key: "underConstructionCibilGt800", label: "Under-construction with CIBIL above 800", adjustment: 0.05 },
        { key: "underConstructionCibilLt800", label: "Under-construction with CIBIL below 800", adjustment: 0.10 },
      ],
    }),
    new BankRates({
      name: "ICICI",
      bands: [
        { minCibil: 800, maxCibil: 900, roi: 7.40 },
        { minCibil: 750, maxCibil: 799, roi: 7.50 },
        { minCibil: 730, maxCibil: 749, roi: 7.85 },
        { minCibil: 700, maxCibil: 729, roi: 8.00 },
        { minCibil: 0, maxCibil: 699, roi: 0 },
        { minCibil: -1, maxCibil: 0, roi: 7.85 },
      ],
      concessions: [
        { key: "property75_199CibilGt800", label: "Property 75-199L, CIBIL above 800", adjustment: 0.10 },
        { key: "propertyLt75CibilGt800", label: "Property below 75L, CIBIL above 800", adjustment: 0.15 },
        { key: "property75_199Cibil750_799", label: "Property 75-199L, CIBIL 750-799", adjustment: 0.25 },
        { key: "propertyLt75Cibil750_799", label: "Property below 75L, CIBIL 750-799", adjustment: 0.25 },
        { key: "property75_199Cibil730_749", label: "Property 75-199L, CIBIL 730-749", adjustment: 0.05 },
        { key: "propertyLt75Cibil730_749", label: "Property below 75L, CIBIL 730-749", adjustment: 0.10 },
        { key: "property75_199Cibil700_729", label: "Property 75-199L, CIBIL 700-729", adjustment: 0.25 },
        { key: "propertyLt75Cibil700_729", label: "Property below 75L, CIBIL 700-729", adjustment: 0.30 },
        { key: "property75_199NoCibil", label: "Property 75-199L, no CIBIL", adjustment: 0.05 },
        { key: "propertyLt75NoCibil", label: "Property below 75L, no CIBIL", adjustment: 0.10 },
        { key: "selfEmployed", label: "Self-employed", adjustment: 0.25 },
        { key: "overdraft", label: "Overdraft product", adjustment: 0.40, aliases: ["maxgain"] },
      ],
    }),
    new BankRates({
      name: "PNB",
      bands: [
        { minCibil: 800, maxCibil: 900, roi: 7.20 },
        { minCibil: 750, maxCibil: 799, roi: 7.25 },
        { minCibil: 0, maxCibil: 749, roi: 0 },
      ],
      concessions: [],
    }),
  ];
}

function getRateInfo(bankName: string | null, cibil: number, concessions?: string[]): string {
  const banks = buildRateCard();
  if (bankName) {
    const b = banks.find(b => b.name.toLowerCase() === bankName.toLowerCase());
    if (!b) return JSON.stringify({ error: `Bank '${bankName}' not found`, available: banks.map(b => b.name) });
    return JSON.stringify({
      bank: b.name,
      base_roi: b.getBaseROI(cibil),
      final_roi: b.getFinalROI(cibil, concessions),
      concessions_applied: concessions ?? [],
    });
  }
  return JSON.stringify(roiAll(banks, cibil, concessions));
}

const TOOL_SCHEMA = {
  name: "get_rate_info",
  description: "Get home loan interest rates for Indian banks. Returns ROI based on CIBIL score and optional concession keys.",
  parameters: {
    type: "object",
    properties: {
      bank_name: {
        type: "string",
        description: "Bank name (e.g. 'HDFC', 'ICICI', 'Axis'). Omit to query all banks.",
      },
      cibil: {
        type: "number",
        description: "CIBIL score (0-900)",
      },
      concessions: {
        type: "array",
        items: { type: "string" },
        description: "Concession keys to apply (e.g. 'womenBorrower', 'overdraft', 'selfEmployed')",
      },
    },
    required: ["cibil"],
  },
} as const;

// Demo
if (require.main === module) {
  console.log(getRateInfo("HDFC", 801, ["womenBorrower"]));
  console.log(getRateInfo(null, 801));
  console.log(JSON.stringify(TOOL_SCHEMA, null, 2));
}

export { BankRates, buildRateCard, getBaseROI, getFinalROI, roiAll, getRateInfo, TOOL_SCHEMA };
export type { CIBILBand, Concession };
