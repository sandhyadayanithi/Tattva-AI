import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { TrendingUp, TrendingDown } from "lucide-react";

const confidenceDistribution = [
  { range: "0-20%", count: 12 },
  { range: "21-40%", count: 34 },
  { range: "41-60%", count: 89 },
  { range: "61-80%", count: 234 },
  { range: "81-100%", count: 847 },
];

const aiVsHumanData = [
  { category: "Match", count: 1089 },
  { category: "Partial Match", count: 134 },
  { category: "Disagree", count: 56 },
  { category: "Pending Review", count: 23 },
];

const accuracyOverTime = [
  { week: "Week 1", accuracy: 91.2 },
  { week: "Week 2", accuracy: 92.8 },
  { week: "Week 3", accuracy: 93.5 },
  { week: "Week 4", accuracy: 94.1 },
  { week: "Week 5", accuracy: 94.8 },
  { week: "Week 6", accuracy: 95.2 },
  { week: "Week 7", accuracy: 95.7 },
  { week: "Week 8", accuracy: 96.1 },
];

const lowConfidenceClaims = [
  {
    id: 1,
    claim: "Ambiguous health claim about natural remedies",
    language: "Tamil",
    aiConfidence: 47.3,
    aiVerdict: "Unclear",
    humanVerdict: "Misleading",
    status: "Under Review",
  },
  {
    id: 2,
    claim: "Political statement with mixed factual elements",
    language: "Hindi",
    aiConfidence: 52.8,
    aiVerdict: "Partial Truth",
    humanVerdict: "Misleading",
    status: "Reviewed",
  },
  {
    id: 3,
    claim: "Complex religious context requiring cultural knowledge",
    language: "Bengali",
    aiConfidence: 38.9,
    aiVerdict: "Uncertain",
    humanVerdict: "False",
    status: "Reviewed",
  },
  {
    id: 4,
    claim: "Financial advice with multiple conditional statements",
    language: "Telugu",
    aiConfidence: 55.6,
    aiVerdict: "Mixed",
    humanVerdict: "Misleading",
    status: "Under Review",
  },
  {
    id: 5,
    claim: "Historical event with disputed interpretations",
    language: "Hindi",
    aiConfidence: 44.2,
    aiVerdict: "Inconclusive",
    humanVerdict: "Context Needed",
    status: "Under Review",
  },
];

export default function ModelFeedback() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-semibold mb-2">Model Feedback & Performance</h2>
        <p className="text-neutral-400">
          AI model accuracy, confidence metrics, and human oversight
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <div className="flex items-start justify-between mb-2">
            <p className="text-sm text-neutral-400">AI Verdict Accuracy</p>
            <TrendingUp className="w-4 h-4 text-green-400" />
          </div>
          <p className="text-3xl font-semibold mb-1">96.1%</p>
          <p className="text-sm text-green-400">+2.3% this month</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <div className="flex items-start justify-between mb-2">
            <p className="text-sm text-neutral-400">Human Override Rate</p>
            <TrendingDown className="w-4 h-4 text-green-400" />
          </div>
          <p className="text-3xl font-semibold mb-1">4.3%</p>
          <p className="text-sm text-green-400">-0.8% this month</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <div className="flex items-start justify-between mb-2">
            <p className="text-sm text-neutral-400">Low Confidence Claims</p>
            <TrendingDown className="w-4 h-4 text-green-400" />
          </div>
          <p className="text-3xl font-semibold mb-1">135</p>
          <p className="text-sm text-green-400">-12% this week</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <div className="flex items-start justify-between mb-2">
            <p className="text-sm text-neutral-400">False Positive Rate</p>
            <TrendingDown className="w-4 h-4 text-green-400" />
          </div>
          <p className="text-3xl font-semibold mb-1">2.1%</p>
          <p className="text-sm text-green-400">-0.3% this month</p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-2 gap-6">
        {/* AI Confidence Score Distribution */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">AI Confidence Score Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={confidenceDistribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
              <XAxis dataKey="range" stroke="#a3a3a3" />
              <YAxis stroke="#a3a3a3" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#262626",
                  border: "1px solid #404040",
                  borderRadius: "8px",
                }}
              />
              <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* AI vs Human Verdict Comparison */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">AI vs Human Verdict Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={aiVsHumanData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
              <XAxis type="number" stroke="#a3a3a3" />
              <YAxis dataKey="category" type="category" stroke="#a3a3a3" width={120} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#262626",
                  border: "1px solid #404040",
                  borderRadius: "8px",
                }}
              />
              <Bar dataKey="count" fill="#10b981" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Model Accuracy Over Time */}
      <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
        <h3 className="text-lg font-medium mb-4">Model Accuracy Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={accuracyOverTime}>
            <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
            <XAxis dataKey="week" stroke="#a3a3a3" />
            <YAxis stroke="#a3a3a3" domain={[90, 100]} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#262626",
                border: "1px solid #404040",
                borderRadius: "8px",
              }}
            />
            <Line
              type="monotone"
              dataKey="accuracy"
              stroke="#10b981"
              strokeWidth={3}
              dot={{ fill: "#10b981", r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Performance Summary Cards */}
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h4 className="text-sm font-medium text-neutral-400 mb-3">
            Agreement Rate
          </h4>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">Full Agreement</span>
              <span className="text-sm font-medium">83.5%</span>
            </div>
            <div className="w-full bg-neutral-800 rounded-full h-2">
              <div className="bg-green-500 h-2 rounded-full" style={{ width: "83.5%" }} />
            </div>
          </div>
          <div className="space-y-3 mt-4">
            <div className="flex items-center justify-between">
              <span className="text-sm">Partial Agreement</span>
              <span className="text-sm font-medium">10.3%</span>
            </div>
            <div className="w-full bg-neutral-800 rounded-full h-2">
              <div
                className="bg-yellow-500 h-2 rounded-full"
                style={{ width: "10.3%" }}
              />
            </div>
          </div>
          <div className="space-y-3 mt-4">
            <div className="flex items-center justify-between">
              <span className="text-sm">Disagreement</span>
              <span className="text-sm font-medium">4.3%</span>
            </div>
            <div className="w-full bg-neutral-800 rounded-full h-2">
              <div className="bg-red-500 h-2 rounded-full" style={{ width: "4.3%" }} />
            </div>
          </div>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h4 className="text-sm font-medium text-neutral-400 mb-4">Error Analysis</h4>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-neutral-800 rounded-lg">
              <span className="text-sm">False Positives</span>
              <span className="text-lg font-semibold text-red-400">27</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-neutral-800 rounded-lg">
              <span className="text-sm">False Negatives</span>
              <span className="text-lg font-semibold text-orange-400">18</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-neutral-800 rounded-lg">
              <span className="text-sm">Uncertain Cases</span>
              <span className="text-lg font-semibold text-yellow-400">135</span>
            </div>
          </div>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h4 className="text-sm font-medium text-neutral-400 mb-4">Review Queue</h4>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-neutral-800 rounded-lg">
              <span className="text-sm">Pending Review</span>
              <span className="text-lg font-semibold text-blue-400">23</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-neutral-800 rounded-lg">
              <span className="text-sm">Under Investigation</span>
              <span className="text-lg font-semibold text-yellow-400">12</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-neutral-800 rounded-lg">
              <span className="text-sm">Reviewed Today</span>
              <span className="text-lg font-semibold text-green-400">47</span>
            </div>
          </div>
        </div>
      </div>

      {/* Low Confidence Claims Table */}
      <div className="bg-neutral-900 border border-neutral-800 rounded-xl overflow-hidden">
        <div className="p-6 border-b border-neutral-800">
          <h3 className="text-lg font-medium">Low Confidence Claims Requiring Review</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-800">
              <tr>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Claim
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Language
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  AI Confidence
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  AI Verdict
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Human Verdict
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800">
              {lowConfidenceClaims.map((claim) => (
                <tr key={claim.id} className="hover:bg-neutral-800/50 transition-colors">
                  <td className="px-6 py-4 text-sm max-w-md">{claim.claim}</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-950 text-blue-300 border border-blue-800">
                      {claim.language}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-neutral-800 rounded-full h-2 w-20">
                        <div
                          className={`h-2 rounded-full ${
                            claim.aiConfidence < 50 ? "bg-red-500" : "bg-yellow-500"
                          }`}
                          style={{ width: `${claim.aiConfidence}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium w-12">
                        {claim.aiConfidence}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-950 text-yellow-300 border border-yellow-800">
                      {claim.aiVerdict}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-950 text-purple-300 border border-purple-800">
                      {claim.humanVerdict}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                        claim.status === "Reviewed"
                          ? "bg-green-950 text-green-300 border border-green-800"
                          : "bg-orange-950 text-orange-300 border border-orange-800"
                      }`}
                    >
                      {claim.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
