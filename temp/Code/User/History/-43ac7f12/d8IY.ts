function emi(p: number, annualRate: number, tenureMonths: number): number {
  const r = annualRate / 12 / 100;
  const n = tenureMonths;
  return Math.round((p * r * (1 + r) ** n) / ((1 + r) ** n - 1) * 100) / 100;
}
