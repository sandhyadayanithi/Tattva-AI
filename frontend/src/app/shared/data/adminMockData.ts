// Mock data generation utilities for Admin Dashboard

export const generateSparklineData = (points: number = 7) => {
    return Array.from({ length: points }, () => Math.floor(Math.random() * 100));
};

export const mockMetrics = {
    totalMessages: 2847392,
    todayMessages: 18247,
    avgProcessingTime: 2.4,
    successRate: 98.7,
    failedJobs: 127,
    pendingQueue: 342,
};

export const mockTrendData = [
    { date: "Sep", claims: 245 },
    { date: "Oct", claims: 312 },
    { date: "Nov", claims: 428 },
    { date: "Dec", claims: 389 },
    { date: "Jan", claims: 502 },
    { date: "Feb", claims: 634 },
    { date: "Mar", claims: 718 },
];

export const mockTopicDistribution = [
    { name: "Health", value: 42, color: "#3b82f6" },
    { name: "Election", value: 28, color: "#10b981" },
    { name: "Religion", value: 18, color: "#f59e0b" },
    { name: "Finance", value: 12, color: "#ef4444" },
];

export const mockTrendingNarratives = [
    {
        id: 1,
        claim: "Fake cure for diabetes using herbal remedy spreading",
        language: "Tamil",
        messages: 1247,
        virality: 8.4,
        firstDetected: "2026-03-05 14:23",
    },
    {
        id: 2,
        claim: "False information about voting date changes",
        language: "Hindi",
        messages: 982,
        virality: 9.1,
        firstDetected: "2026-03-06 09:15",
    },
    {
        id: 3,
        claim: "Misleading financial investment scheme promise",
        language: "Telugu",
        messages: 756,
        virality: 7.8,
        firstDetected: "2026-03-04 16:42",
    },
    {
        id: 4,
        claim: "Religious misinformation about temple rituals",
        language: "Bengali",
        messages: 623,
        virality: 6.9,
        firstDetected: "2026-03-06 11:30",
    },
    {
        id: 5,
        claim: "Fake government policy announcement circulating",
        language: "Hindi",
        messages: 548,
        virality: 7.5,
        firstDetected: "2026-03-05 20:18",
    },
];
