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
