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
  BarChart,
  Bar,
} from "recharts";

const claimsOverTimeData = [
  { date: "Feb 28", claims: 145 },
  { date: "Mar 1", claims: 178 },
  { date: "Mar 2", claims: 156 },
  { date: "Mar 3", claims: 203 },
  { date: "Mar 4", claims: 189 },
  { date: "Mar 5", claims: 234 },
  { date: "Mar 6", claims: 267 },
  { date: "Mar 7", claims: 312 },
];

const topicDistributionData = [
  { name: "Health", value: 42, color: "#3b82f6" },
  { name: "Election", value: 28, color: "#10b981" },
  { name: "Religion", value: 18, color: "#f59e0b" },
  { name: "Finance", value: 12, color: "#ef4444" },
];

const claimsByLanguage = [
  { language: "Tamil", claims: 485 },
  { language: "Hindi", claims: 392 },
  { language: "Telugu", claims: 278 },
  { language: "Bengali", claims: 156 },
];

const trendingNarratives = [
  {
    id: 1,
    claim: "Fake cure for diabetes using herbal remedy spreading",
    language: "Tamil",
    messages: 1247,
    virality: 8.4,
    firstDetected: "2026-03-05 14:23",
    topic: "Health",
  },
  {
    id: 2,
    claim: "False information about voting date changes",
    language: "Hindi",
    messages: 982,
    virality: 9.1,
    firstDetected: "2026-03-06 09:15",
    topic: "Election",
  },
  {
    id: 3,
    claim: "Misleading financial investment scheme promise",
    language: "Telugu",
    messages: 756,
    virality: 7.8,
    firstDetected: "2026-03-04 16:42",
    topic: "Finance",
  },
  {
    id: 4,
    claim: "Religious misinformation about temple rituals",
    language: "Bengali",
    messages: 623,
    virality: 6.9,
    firstDetected: "2026-03-06 11:30",
    topic: "Religion",
  },
  {
    id: 5,
    claim: "Fake government policy announcement circulating",
    language: "Hindi",
    messages: 548,
    virality: 7.5,
    firstDetected: "2026-03-05 20:18",
    topic: "Election",
  },
  {
    id: 6,
    claim: "Fabricated celebrity health crisis news spreading",
    language: "Tamil",
    messages: 492,
    virality: 8.1,
    firstDetected: "2026-03-06 15:47",
    topic: "Health",
  },
  {
    id: 7,
    claim: "False claim about religious conversion activities",
    language: "Hindi",
    messages: 437,
    virality: 7.3,
    firstDetected: "2026-03-05 08:25",
    topic: "Religion",
  },
  {
    id: 8,
    claim: "Cryptocurrency scam posing as government initiative",
    language: "Telugu",
    messages: 389,
    virality: 8.7,
    firstDetected: "2026-03-07 10:12",
    topic: "Finance",
  },
];

export default function MisinformationTrends() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-semibold mb-2">Misinformation Trends</h2>
        <p className="text-neutral-400">
          Analyze patterns and emerging misinformation narratives
        </p>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-2 gap-6">
        {/* Claims Over Time */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">Claims Detected Over Time</h3>
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={claimsOverTimeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
              <XAxis dataKey="date" stroke="#a3a3a3" />
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
                strokeWidth={3}
                dot={{ fill: "#3b82f6", r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Topic Distribution */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <h3 className="text-lg font-medium mb-4">Topic Distribution</h3>
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={topicDistributionData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name} ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={110}
                fill="#8884d8"
                dataKey="value"
              >
                {topicDistributionData.map((entry) => (
                  <Cell key={`trends-topic-${entry.name}`} fill={entry.color} />
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

      {/* Claims by Language Bar Chart */}
      <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
        <h3 className="text-lg font-medium mb-4">Claims by Language</h3>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={claimsByLanguage}>
            <CartesianGrid strokeDasharray="3 3" stroke="#404040" />
            <XAxis dataKey="language" stroke="#a3a3a3" />
            <YAxis stroke="#a3a3a3" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#262626",
                border: "1px solid #404040",
                borderRadius: "8px",
              }}
            />
            <Bar dataKey="claims" fill="#3b82f6" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Trending Narratives Table */}
      <div className="bg-neutral-900 border border-neutral-800 rounded-xl overflow-hidden">
        <div className="p-6 border-b border-neutral-800 flex items-center justify-between">
          <h3 className="text-lg font-medium">Trending Misinformation Narratives</h3>
          <div className="flex gap-3">
            <select className="px-4 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-sm focus:outline-none focus:border-blue-500">
              <option>All Languages</option>
              <option>Tamil</option>
              <option>Hindi</option>
              <option>Telugu</option>
              <option>Bengali</option>
            </select>
            <select className="px-4 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-sm focus:outline-none focus:border-blue-500">
              <option>All Topics</option>
              <option>Health</option>
              <option>Election</option>
              <option>Religion</option>
              <option>Finance</option>
            </select>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-800">
              <tr>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Claim Summary
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Topic
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Language
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Messages
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
              {trendingNarratives.map((narrative) => (
                <tr key={narrative.id} className="hover:bg-neutral-800/50 transition-colors">
                  <td className="px-6 py-4 text-sm max-w-md">{narrative.claim}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                        narrative.topic === "Health"
                          ? "bg-blue-950 text-blue-300 border border-blue-800"
                          : narrative.topic === "Election"
                          ? "bg-green-950 text-green-300 border border-green-800"
                          : narrative.topic === "Religion"
                          ? "bg-yellow-950 text-yellow-300 border border-yellow-800"
                          : "bg-red-950 text-red-300 border border-red-800"
                      }`}
                    >
                      {narrative.topic}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-950 text-purple-300 border border-purple-800">
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
                      <span className="text-sm font-medium w-8">{narrative.virality}</span>
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
    </div>
  );
}