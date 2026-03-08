import { Filter, Calendar } from "lucide-react";
import { useState } from "react";

const repeatClaims = [
  {
    id: 1,
    claim: "Drinking hot water with lemon cures COVID-19",
    firstDetected: "2025-12-14",
    occurrences: 3847,
    languages: ["Tamil", "Hindi", "Telugu"],
    verdict: "False",
    lastSeen: "2026-03-07 08:42",
  },
  {
    id: 2,
    claim: "Government is secretly tracking citizens through vaccine chips",
    firstDetected: "2025-11-22",
    occurrences: 2934,
    languages: ["Hindi", "Bengali"],
    verdict: "Debunked",
    lastSeen: "2026-03-07 11:15",
  },
  {
    id: 3,
    claim: "5G towers cause brain damage and health issues",
    firstDetected: "2025-10-08",
    occurrences: 2456,
    languages: ["Tamil", "Telugu", "Hindi"],
    verdict: "False",
    lastSeen: "2026-03-06 19:33",
  },
  {
    id: 4,
    claim: "Election voting machines can be hacked remotely",
    firstDetected: "2026-01-15",
    occurrences: 1893,
    languages: ["Hindi", "Tamil"],
    verdict: "Misleading",
    lastSeen: "2026-03-07 14:28",
  },
  {
    id: 5,
    claim: "Eating garlic prevents all types of cancer",
    firstDetected: "2025-09-03",
    occurrences: 1672,
    languages: ["Tamil", "Bengali", "Telugu"],
    verdict: "False",
    lastSeen: "2026-03-06 22:51",
  },
  {
    id: 6,
    claim: "New tax law will seize 30% of all savings accounts",
    firstDetected: "2026-02-18",
    occurrences: 1534,
    languages: ["Hindi", "Telugu"],
    verdict: "False",
    lastSeen: "2026-03-07 16:07",
  },
  {
    id: 7,
    claim: "Certain religious groups receiving special government benefits",
    firstDetected: "2025-11-29",
    occurrences: 1289,
    languages: ["Hindi", "Bengali", "Tamil"],
    verdict: "Debunked",
    lastSeen: "2026-03-07 09:23",
  },
  {
    id: 8,
    claim: "Cryptocurrency investment guaranteed to double money in 30 days",
    firstDetected: "2026-01-07",
    occurrences: 1156,
    languages: ["Tamil", "Telugu"],
    verdict: "Scam",
    lastSeen: "2026-03-07 12:45",
  },
  {
    id: 9,
    claim: "Drinking cow urine cures diabetes and kidney diseases",
    firstDetected: "2025-08-19",
    occurrences: 1047,
    languages: ["Hindi", "Tamil"],
    verdict: "Dangerous",
    lastSeen: "2026-03-05 20:18",
  },
  {
    id: 10,
    claim: "Government planning to ban certain religious practices",
    firstDetected: "2026-02-05",
    occurrences: 923,
    languages: ["Bengali", "Hindi", "Tamil", "Telugu"],
    verdict: "False",
    lastSeen: "2026-03-07 07:52",
  },
];

const languageColors: Record<string, string> = {
  Tamil: "bg-blue-950 text-blue-300 border-blue-800",
  Hindi: "bg-green-950 text-green-300 border-green-800",
  Telugu: "bg-purple-950 text-purple-300 border-purple-800",
  Bengali: "bg-yellow-950 text-yellow-300 border-yellow-800",
};

const verdictColors: Record<string, string> = {
  False: "bg-red-950 text-red-300 border-red-800",
  Debunked: "bg-orange-950 text-orange-300 border-orange-800",
  Misleading: "bg-yellow-950 text-yellow-300 border-yellow-800",
  Scam: "bg-red-950 text-red-300 border-red-800",
  Dangerous: "bg-red-950 text-red-300 border-red-800",
};

export default function RepeatClaims() {
  const [selectedLanguage, setSelectedLanguage] = useState("all");
  const [selectedVerdict, setSelectedVerdict] = useState("all");

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-semibold mb-2">Repeat Claim Detection</h2>
        <p className="text-neutral-400">
          Track and manage previously detected misinformation claims
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Total Cached Claims</p>
          <p className="text-3xl font-semibold">1,847</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Active Claims (30d)</p>
          <p className="text-3xl font-semibold">342</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Cache Hit Rate</p>
          <p className="text-3xl font-semibold">73.4%</p>
        </div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <p className="text-sm text-neutral-400 mb-1">Avg Response Time</p>
          <p className="text-3xl font-semibold">0.8s</p>
        </div>
      </div>

      {/* Filters and Table */}
      <div className="bg-neutral-900 border border-neutral-800 rounded-xl overflow-hidden">
        <div className="p-6 border-b border-neutral-800 flex items-center justify-between">
          <h3 className="text-lg font-medium">Previously Detected Claims</h3>
          <div className="flex gap-3">
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-500" />
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="pl-10 pr-4 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-sm focus:outline-none focus:border-blue-500 appearance-none"
              >
                <option value="all">All Languages</option>
                <option value="tamil">Tamil</option>
                <option value="hindi">Hindi</option>
                <option value="telugu">Telugu</option>
                <option value="bengali">Bengali</option>
              </select>
            </div>
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-500" />
              <select
                value={selectedVerdict}
                onChange={(e) => setSelectedVerdict(e.target.value)}
                className="pl-10 pr-4 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-sm focus:outline-none focus:border-blue-500 appearance-none"
              >
                <option value="all">All Verdicts</option>
                <option value="false">False</option>
                <option value="debunked">Debunked</option>
                <option value="misleading">Misleading</option>
                <option value="scam">Scam</option>
              </select>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-sm hover:bg-neutral-700 transition-colors">
              <Calendar className="w-4 h-4" />
              Date Range
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-800">
              <tr>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Claim Text
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  First Detected
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Occurrences
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Languages
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Cached Verdict
                </th>
                <th className="text-left px-6 py-4 text-sm font-medium text-neutral-300">
                  Last Seen
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800">
              {repeatClaims.map((claim) => (
                <tr key={claim.id} className="hover:bg-neutral-800/50 transition-colors">
                  <td className="px-6 py-4 text-sm max-w-md">{claim.claim}</td>
                  <td className="px-6 py-4 text-sm text-neutral-400">
                    {claim.firstDetected}
                  </td>
                  <td className="px-6 py-4 text-sm font-medium">
                    {claim.occurrences.toLocaleString()}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-1">
                      {claim.languages.map((lang) => (
                        <span
                          key={lang}
                          className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${languageColors[lang]}`}
                        >
                          {lang}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${
                        verdictColors[claim.verdict]
                      }`}
                    >
                      {claim.verdict}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-neutral-400">
                    {claim.lastSeen}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="p-4 border-t border-neutral-800 flex items-center justify-between">
          <p className="text-sm text-neutral-400">
            Showing 10 of {repeatClaims.length} claims
          </p>
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-sm hover:bg-neutral-700 transition-colors">
              Previous
            </button>
            <button className="px-4 py-2 bg-blue-600 border border-blue-600 rounded-lg text-sm hover:bg-blue-700 transition-colors">
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
