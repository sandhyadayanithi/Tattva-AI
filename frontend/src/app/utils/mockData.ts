// Mock data generation utilities

export const generateSparklineData = (points: number = 7) => {
  return Array.from({ length: points }, () => Math.floor(Math.random() * 100));
};

export const mockMetrics = {
  totalMessages: 1847293,
  todayMessages: 45678,
  avgProcessingTime: 2.3,
  successRate: 98.7,
  failedJobs: 23,
  pendingQueue: 156,
};

export const mockTrendData = Array.from({ length: 30 }, (_, i) => ({
  date: new Date(2026, 2, i - 29).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  }),
  claims: Math.floor(Math.random() * 200) + 50,
}));

export const mockTopicDistribution = [
  { name: "Health", value: 420, color: "#3b82f6" },
  { name: "Election", value: 380, color: "#8b5cf6" },
  { name: "Religion", value: 290, color: "#ec4899" },
  { name: "Finance", value: 210, color: "#f59e0b" },
];

export const mockTrendingNarratives = [
  {
    id: 1,
    claim: "Fake COVID-19 vaccine side effects claim spreading",
    language: "Tamil",
    messages: 1247,
    virality: 8.4,
    firstDetected: "2026-03-05 14:23",
  },
  {
    id: 2,
    claim: "Election rigging allegations in upcoming state polls",
    language: "Hindi",
    messages: 982,
    virality: 9.2,
    firstDetected: "2026-03-06 09:15",
  },
  {
    id: 3,
    claim: "Religious conversion conspiracy theory",
    language: "Telugu",
    messages: 756,
    virality: 7.8,
    firstDetected: "2026-03-04 18:45",
  },
  {
    id: 4,
    claim: "Cryptocurrency scam warning (false information)",
    language: "Bengali",
    messages: 634,
    virality: 6.9,
    firstDetected: "2026-03-07 11:30",
  },
  {
    id: 5,
    claim: "Fake government policy announcement",
    language: "Hindi",
    messages: 521,
    virality: 7.2,
    firstDetected: "2026-03-03 16:20",
  },
];

export const mockRepeatClaims = [
  {
    id: 1,
    claimText: "5G towers cause health problems and spread diseases",
    firstDetected: "2025-11-15",
    occurrences: 3456,
    languages: ["Tamil", "Hindi", "Telugu"],
    verdict: "False",
    lastSeen: "2026-03-07",
  },
  {
    id: 2,
    claimText: "Government planning to ban cash transactions completely",
    firstDetected: "2026-01-22",
    occurrences: 2890,
    languages: ["Hindi", "Bengali"],
    verdict: "Misleading",
    lastSeen: "2026-03-06",
  },
  {
    id: 3,
    claimText: "Drinking hot water cures all viral infections",
    firstDetected: "2025-12-08",
    occurrences: 2341,
    languages: ["Tamil", "Telugu", "Bengali"],
    verdict: "False",
    lastSeen: "2026-03-07",
  },
  {
    id: 4,
    claimText: "Election results already decided before voting",
    firstDetected: "2026-02-10",
    occurrences: 1987,
    languages: ["Hindi"],
    verdict: "Unverified",
    lastSeen: "2026-03-05",
  },
  {
    id: 5,
    claimText: "Bank accounts frozen due to new regulation",
    firstDetected: "2026-02-28",
    occurrences: 1654,
    languages: ["Tamil", "Hindi", "Telugu", "Bengali"],
    verdict: "False",
    lastSeen: "2026-03-07",
  },
  {
    id: 6,
    claimText: "Religious sites being converted by force",
    firstDetected: "2025-10-05",
    occurrences: 1432,
    languages: ["Hindi", "Telugu"],
    verdict: "False",
    lastSeen: "2026-03-04",
  },
];

export const mockHighRiskClaims = [
  {
    id: 1,
    claim: "Election rigging allegations in upcoming state polls",
    language: "Hindi",
    occurrences: 982,
    viralityScore: 9.2,
    risk: "high",
  },
  {
    id: 2,
    claim: "Fake COVID-19 vaccine side effects claim spreading",
    language: "Tamil",
    occurrences: 1247,
    viralityScore: 8.4,
    risk: "high",
  },
  {
    id: 3,
    claim: "Religious conversion conspiracy theory",
    language: "Telugu",
    occurrences: 756,
    viralityScore: 7.8,
    risk: "high",
  },
  {
    id: 4,
    claim: "Fake government policy announcement",
    language: "Hindi",
    occurrences: 521,
    viralityScore: 7.2,
    risk: "medium",
  },
  {
    id: 5,
    claim: "Cryptocurrency scam warning (false information)",
    language: "Bengali",
    occurrences: 634,
    viralityScore: 6.9,
    risk: "medium",
  },
];

export const mockViralityDistribution = [
  { range: "1-2", count: 145 },
  { range: "3-4", count: 289 },
  { range: "5-6", count: 456 },
  { range: "7-8", count: 312 },
  { range: "9-10", count: 98 },
];

export const mockLanguageDistribution = [
  { name: "Tamil", value: 35, color: "#3b82f6" },
  { name: "Hindi", value: 30, color: "#8b5cf6" },
  { name: "Telugu", value: 20, color: "#ec4899" },
  { name: "Bengali", value: 15, color: "#f59e0b" },
];

export const mockLanguageProcessingTime = [
  { language: "Tamil", time: 2.8 },
  { language: "Hindi", time: 2.3 },
  { language: "Telugu", time: 2.6 },
  { language: "Bengali", time: 3.1 },
];

export const mockLanguageClaimsProcessed = [
  { language: "Tamil", claims: 4532, percentage: 35 },
  { language: "Hindi", claims: 3884, percentage: 30 },
  { language: "Telugu", claims: 2589, percentage: 20 },
  { language: "Bengali", claims: 1942, percentage: 15 },
];

export const mockConfidenceDistribution = Array.from({ length: 10 }, (_, i) => ({
  range: `${i * 10}-${(i + 1) * 10}%`,
  count: Math.floor(Math.random() * 150) + 50,
}));

export const mockVerdictComparison = [
  { verdict: "Agree", count: 7842 },
  { verdict: "Disagree", count: 456 },
  { verdict: "Partial", count: 892 },
];

export const mockAccuracyOverTime = Array.from({ length: 12 }, (_, i) => ({
  month: new Date(2025, i).toLocaleDateString("en-US", { month: "short" }),
  accuracy: 85 + Math.random() * 10,
}));

export const mockModelMetrics = {
  accuracy: 94.5,
  humanOverrideRate: 5.5,
  lowConfidence: 8.2,
  falsePositiveRate: 2.3,
};
