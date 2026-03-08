import MetricCard from "../components/MetricCard";
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const metricsData = [
  {
    title: "Total Messages Processed",
    value: "2,847,392",
    trend: 12.5,
    sparklineData: [45, 52, 48, 61, 55, 68, 72, 69, 75],
  },
  {
    title: "Messages Processed Today",
    value: "18,247",
    trend: 8.3,
    sparklineData: [32, 38, 35, 42, 45, 48, 52, 49, 54],
  },
  {
    title: "Average Processing Time",
    value: "2.4s",
    trend: -5.2,
    sparklineData: [65, 62, 58, 55, 53, 51, 48, 46, 44],
  },
  {
    title: "Pipeline Success Rate",
    value: "98.7%",
    trend: 0.4,
    sparklineData: [95, 96, 97, 96, 98, 97, 98, 99, 98],
  },
  {
    title: "Failed Jobs",
    value: "127",
    trend: -12.8,
    sparklineData: [180, 165, 152, 145, 138, 132, 128, 125, 127],
  },
  {
    title: "Pending Queue Size",
    value: "342",
    trend: 3.2,
    sparklineData: [285, 298, 312, 305, 318, 325, 332, 338, 342],
  },
];

const claimsOverTimeData = [
  { month: "Sep", claims: 245 },
  { month: "Oct", claims: 312 },
  { month: "Nov", claims: 428 },
  { month: "Dec", claims: 389 },
  { month: "Jan", claims: 502 },
  { month: "Feb", claims: 634 },
  { month: "Mar", claims: 718 },
];

const topicDistributionData = [
  { name: "Health", value: 42, color: "#3b82f6" },
  { name: "Election", value: 28, color: "#10b981" },
  { name: "Religion", value: 18, color: "#f59e0b" },
  { name: "Finance", value: 12, color: "#ef4444" },
];

const trendingNarratives = [
  {
    claim: "Fake cure for diabetes using herbal remedy spreading",
    language: "Tamil",
    messages: 1247,
    virality: 8.4,
    firstDetected: "2026-03-05 14:23",
  },
  {
    claim: "False information about voting date changes",
    language: "Hindi",
    messages: 982,
    virality: 9.1,
    firstDetected: "2026-03-06 09:15",
  },
  {
    claim: "Misleading financial investment scheme promise",
    language: "Telugu",
    messages: 756,
    virality: 7.8,
    firstDetected: "2026-03-04 16:42",
  },
  {
    claim: "Religious misinformation about temple rituals",
    language: "Bengali",
    messages: 623,
    virality: 6.9,
    firstDetected: "2026-03-06 11:30",
  },
  {
    claim: "Fake government policy announcement circulating",
    language: "Hindi",
    messages: 548,
    virality: 7.5,
    firstDetected: "2026-03-05 20:18",
  },
];

export default function Dashboard() {
  return (
    <div className="space-y-8">
<<<<<<< HEAD
      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title} className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-[oklch(0.708_0_0)]">
                  {stat.title}
                </CardTitle>
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-4 w-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-semibold text-white">{stat.value}</div>
                <p className="text-xs text-[oklch(0.696_0.17_162.48)] mt-1">
                  {stat.change} from last month
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Welcome Section */}
      <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
        <CardHeader>
          <CardTitle className="text-white">Welcome to FactCheck Portal</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 text-[oklch(0.708_0_0)]">
            <p>
              This dashboard provides you with comprehensive tools to review fact-check results
              from WhatsApp voice messages processed through our AI-powered verification system.
            </p>
            <div className="grid grid-cols-2 gap-4 mt-6">
              <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                <h4 className="font-medium text-white mb-2">📊 Review History</h4>
                <p className="text-sm">
                  Access all previously fact-checked claims with detailed verdicts and explanations.
                </p>
              </div>
              <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                <h4 className="font-medium text-white mb-2">🌐 Multi-Language Support</h4>
                <p className="text-sm">
                  View claims in their original language alongside English translations.
                </p>
              </div>
              <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                <h4 className="font-medium text-white mb-2">🤝 Partner Collaboration</h4>
                <p className="text-sm">
                  Report discrepancies and collaborate with fact-checking organizations.
                </p>
              </div>
              <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                <h4 className="font-medium text-white mb-2">🔍 Advanced Search</h4>
                <p className="text-sm">
                  Quickly find specific claims using our powerful search and filter tools.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
        <CardHeader>
          <CardTitle className="text-white">Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <button className="flex-1 px-4 py-3 bg-[oklch(0.488_0.243_264.376)] text-white rounded-lg hover:bg-[oklch(0.488_0.243_264.376)]/90 transition-colors">
              View Recent Claims
            </button>
            <button className="flex-1 px-4 py-3 bg-[oklch(0.269_0_0)] text-white rounded-lg hover:bg-[oklch(0.269_0_0)]/80 transition-colors">
              Report Issue
            </button>
            <button className="flex-1 px-4 py-3 bg-[oklch(0.269_0_0)] text-white rounded-lg hover:bg-[oklch(0.269_0_0)]/80 transition-colors">
              View Documentation
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
=======
      {/* Section 1: System Overview */}
      <section>
        <h2 className="text-2xl font-semibold mb-6">System Overview</h2>
        <div className="grid grid-cols-3 gap-6">
          {metricsData.map((metric, index) => (
            <MetricCard key={index} {...metric} />
          ))}
        </div>
      </section>

      {/* Section 2: Misinformation Trends Preview */}
      <section>
        <h2 className="text-2xl font-semibold mb-6">Misinformation Trends</h2>
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Claims Over Time Chart */}
          <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
            <h3 className="text-lg font-medium mb-4">Claims Detected Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={claimsOverTimeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
                <XAxis dataKey="month" stroke="#a3a3a3" />
                <YAxis stroke="#a3a3a3" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#262626",
                    border: "1px solid #404040",
                    borderRadius: "8px",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="claims"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={{ fill: "#3b82f6", r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Topic Distribution Chart */}
          <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
            <h3 className="text-lg font-medium mb-4">Topic Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={topicDistributionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {topicDistributionData.map((entry) => (
                    <Cell key={`dashboard-topic-${entry.name}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#262626",
                    border: "1px solid #404040",
                    borderRadius: "8px",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Trending Narratives Table */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl overflow-hidden">
          <div className="p-6 border-b border-neutral-800">
            <h3 className="text-lg font-medium">Trending Misinformation Narratives</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-neutral-800">
                <tr>
                  <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                    Claim Summary
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                    Language
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                    Detected Messages
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                    Virality Score
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                    First Detected
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-800">
                {trendingNarratives.map((narrative, index) => (
                  <tr key={index} className="hover:bg-neutral-800/50 transition-colors">
                    <td className="px-6 py-4 text-sm">{narrative.claim}</td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-950 text-blue-300 border border-blue-800">
                        {narrative.language}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium">
                      {narrative.messages.toLocaleString()}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-neutral-800 rounded-full h-2 w-20">
                          <div
                            className={`h-2 rounded-full ${
                              narrative.virality >= 8
                                ? "bg-red-500"
                                : narrative.virality >= 6
                                ? "bg-yellow-500"
                                : "bg-green-500"
                            }`}
                            style={{ width: `${narrative.virality * 10}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium">{narrative.virality}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-neutral-400">
                      {narrative.firstDetected}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}
>>>>>>> 009a52ca1ffae4c2f23641b736d59688f7687a9b
