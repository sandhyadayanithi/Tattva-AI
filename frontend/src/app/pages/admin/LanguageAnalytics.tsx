import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import MetricCard from "../../components/MetricCard";
import { LanguageTags } from "../../components/LanguageTags";

const languageDistribution = [
  { name: "Tamil", value: 485, percentage: 38.7, color: "#3b82f6" },
  { name: "Hindi", value: 392, percentage: 31.3, color: "#10b981" },
  { name: "Telugu", value: 278, percentage: 22.2, color: "#f59e0b" },
  { name: "Bengali", value: 98, percentage: 7.8, color: "#ef4444" },
];

const processingTimeByLanguage = [
  { language: "Tamil", avgTime: 2.8 },
  { language: "Hindi", avgTime: 2.3 },
  { language: "Telugu", avgTime: 2.6 },
  { language: "Bengali", avgTime: 3.1 },
];

const claimsByLanguageDetails = [
  {
    language: "Tamil",
    totalClaims: 485,
    todayClaims: 42,
    avgProcessingTime: "2.8s",
    accuracy: "96.4%",
    percentage: 38.7,
  },
  {
    language: "Hindi",
    totalClaims: 392,
    todayClaims: 38,
    avgProcessingTime: "2.3s",
    accuracy: "97.2%",
    percentage: 31.3,
  },
  {
    language: "Telugu",
    totalClaims: 278,
    todayClaims: 24,
    avgProcessingTime: "2.6s",
    accuracy: "95.8%",
    percentage: 22.2,
  },
  {
    language: "Bengali",
    totalClaims: 98,
    todayClaims: 9,
    avgProcessingTime: "3.1s",
    accuracy: "94.3%",
    percentage: 7.8,
  },
];

export default function LanguageAnalytics() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-semibold mb-2">Language Analytics</h2>
        <p className="text-neutral-400">
          Multi-lingual processing insights and performance metrics
        </p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Languages Supported</p>
          <p className="text-3xl font-semibold">4</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Total Messages</p>
          <p className="text-3xl font-semibold">1,253</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Avg Accuracy</p>
          <p className="text-3xl font-semibold">95.9%</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Multilingual Claims</p>
          <p className="text-3xl font-semibold">247</p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-2 gap-6">
        {/* Language Distribution Pie Chart */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">Language Distribution</h3>
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={languageDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name} ${percentage}%`}
                outerRadius={110}
                fill="#8884d8"
                dataKey="value"
              >
                {languageDistribution.map((entry) => (
                  <Cell key={`language-dist-${entry.name}`} fill={entry.color} />
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

        {/* Processing Time by Language Bar Chart */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">
            Average Processing Time by Language
          </h3>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={processingTimeByLanguage}>
              <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
              <XAxis dataKey="language" stroke="#a3a3a3" />
              <YAxis stroke="#a3a3a3" label={{ value: "Seconds", angle: -90 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#262626",
                  border: "1px solid #404040",
                  borderRadius: "8px",
                }}
              />
              <Bar dataKey="avgTime" fill="#10b981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Language Breakdown */}
      <div className="bg-neutral-900 border border-neutral-800 rounded-xl overflow-hidden">
        <div className="p-6 border-b border-neutral-800">
          <h3 className="text-lg font-medium">Claims Processed by Language</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-800">
              <tr>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Language
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Total Claims
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Today's Claims
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Avg Processing Time
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Accuracy
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Distribution
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800">
              {claimsByLanguageDetails.map((lang, index) => (
                <tr key={index} className="hover:bg-neutral-800/50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{
                          backgroundColor: languageDistribution[index].color,
                        }}
                      />
                      <span className="font-medium">{lang.language}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm font-medium">
                    {lang.totalClaims.toLocaleString()}
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-950 text-blue-300 border border-blue-800">
                      +{lang.todayClaims}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">{lang.avgProcessingTime}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">{lang.accuracy}</span>
                      <div className="flex-1 bg-neutral-800 rounded-full h-2 w-20">
                        <div
                          className="h-2 rounded-full bg-green-500"
                          style={{
                            width: lang.accuracy,
                          }}
                        />
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-neutral-800 rounded-full h-2">
                        <div
                          className="h-2 rounded-full"
                          style={{
                            width: `${lang.percentage}%`,
                            backgroundColor: languageDistribution[index].color,
                          }}
                        />
                      </div>
                      <span className="text-sm text-neutral-400 w-12">
                        {lang.percentage}%
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Language-Specific Insights */}
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">Top Performing Languages</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
              <div>
                <p className="font-medium">Hindi</p>
                <p className="text-sm text-neutral-400">Highest Accuracy</p>
              </div>
              <span className="text-2xl font-semibold text-green-400">97.2%</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
              <div>
                <p className="font-medium">Tamil</p>
                <p className="text-sm text-neutral-400">Most Claims Processed</p>
              </div>
              <span className="text-2xl font-semibold text-blue-400">485</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
              <div>
                <p className="font-medium">Hindi</p>
                <p className="text-sm text-neutral-400">Fastest Processing</p>
              </div>
              <span className="text-2xl font-semibold text-yellow-400">2.3s</span>
            </div>
          </div>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">Language Challenges</h3>
          <div className="space-y-4">
            <div className="p-4 bg-neutral-800 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <p className="font-medium">Bengali</p>
                <span className="text-sm text-yellow-400">Attention Needed</span>
              </div>
              <p className="text-sm text-neutral-400">
                Slowest processing time (3.1s) - Consider model optimization
              </p>
            </div>
            <div className="p-4 bg-neutral-800 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <p className="font-medium">Bengali</p>
                <span className="text-sm text-yellow-400">Lowest Volume</span>
              </div>
              <p className="text-sm text-neutral-400">
                Only 7.8% of total claims - May need more training data
              </p>
            </div>
            <div className="p-4 bg-neutral-800 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <p className="font-medium">Telugu</p>
                <span className="text-sm text-orange-400">Moderate Issue</span>
              </div>
              <p className="text-sm text-neutral-400">
                Accuracy below 96% - Review false positives
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}