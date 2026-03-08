import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../../shared/components/ui/card";
import { Input } from "../../shared/components/ui/input";
import { Search, ChevronLeft, ChevronRight } from "lucide-react";
import { mockClaims, type Claim } from "../../shared/data/mockData";
import VerdictBadge from "../../shared/components/ui/VerdictBadge";
import RiskMeter from "./components/RiskMeter";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../shared/components/ui/select";
import { Button } from "../../shared/components/ui/button";

export default function FactCheckHistory() {
  const [selectedClaim, setSelectedClaim] = useState<Claim | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [verdictFilter, setVerdictFilter] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Filter claims
  const filteredClaims = mockClaims.filter((claim) => {
    const matchesSearch = claim.claimSummary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      claim.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesVerdict = verdictFilter === "all" || claim.verdict === verdictFilter;
    return matchesSearch && matchesVerdict;
  });

  // Pagination
  const totalPages = Math.ceil(filteredClaims.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedClaims = filteredClaims.slice(startIndex, startIndex + itemsPerPage);

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[oklch(0.708_0_0)]" size={18} />
              <Input
                type="text"
                placeholder="Search by claim or ID..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white placeholder:text-[oklch(0.708_0_0)]"
              />
            </div>
            <Select value={verdictFilter} onValueChange={setVerdictFilter}>
              <SelectTrigger className="w-48 bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white">
                <SelectValue placeholder="Filter by verdict" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Verdicts</SelectItem>
                <SelectItem value="True">True</SelectItem>
                <SelectItem value="False">False</SelectItem>
                <SelectItem value="Misleading">Misleading</SelectItem>
                <SelectItem value="Unverified">Unverified</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-2 gap-6">
        {/* Claims Table */}
        <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
          <CardHeader>
            <CardTitle className="text-white">Fact Check Results</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[oklch(0.269_0_0)]">
                    <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">Claim</th>
                    <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">Verdict</th>
                    <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">Language</th>
                    <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">Confidence</th>
                    <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">Risk</th>
                    <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {paginatedClaims.map((claim) => (
                    <tr
                      key={claim.id}
                      onClick={() => setSelectedClaim(claim)}
                      className={`border-b border-[oklch(0.269_0_0)] cursor-pointer transition-colors ${selectedClaim?.id === claim.id
                        ? "bg-[oklch(0.488_0.243_264.376)]/10"
                        : "hover:bg-[oklch(0.269_0_0)]"
                        }`}
                    >
                      <td className="py-3 px-4">
                        <div className="text-sm text-white max-w-xs truncate">{claim.claimSummary}</div>
                        <div className="text-xs text-[oklch(0.708_0_0)] mt-1">{claim.id}</div>
                      </td>
                      <td className="py-3 px-4">
                        <VerdictBadge verdict={claim.verdict} />
                      </td>
                      <td className="py-3 px-4 text-sm text-[oklch(0.708_0_0)]">{claim.language}</td>
                      <td className="py-3 px-4 text-sm text-white">{claim.confidence}%</td>
                      <td className="py-3 px-4">
                        <span className={`text-sm font-medium ${claim.viralityRisk > 6 ? "text-[oklch(0.645_0.246_16.439)]" :
                          claim.viralityRisk > 3 ? "text-[oklch(0.769_0.188_70.08)]" :
                            "text-[oklch(0.696_0.17_162.48)]"
                          }`}>
                          {claim.viralityRisk}/10
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-[oklch(0.708_0_0)]">
                        {new Date(claim.dateChecked).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between mt-4 pt-4 border-t border-[oklch(0.269_0_0)]">
              <div className="text-sm text-[oklch(0.708_0_0)]">
                Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, filteredClaims.length)} of {filteredClaims.length} results
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white hover:bg-[oklch(0.269_0_0)]/80"
                >
                  <ChevronLeft size={16} />
                </Button>
                <span className="px-4 py-2 text-sm text-white">
                  Page {currentPage} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white hover:bg-[oklch(0.269_0_0)]/80"
                >
                  <ChevronRight size={16} />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Claim Details */}
        <div className="space-y-6">
          {selectedClaim ? (
            <>
              <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-white">Claim Details</CardTitle>
                      <p className="text-sm text-[oklch(0.708_0_0)] mt-1">{selectedClaim.id}</p>
                    </div>
                    <VerdictBadge verdict={selectedClaim.verdict} />
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Original Language */}
                  <div>
                    <h4 className="text-sm font-medium text-[oklch(0.708_0_0)] mb-2">Original Language</h4>
                    <p className="text-white">{selectedClaim.language}</p>
                  </div>

                  {/* Original Transcript */}
                  <div>
                    <h4 className="text-sm font-medium text-[oklch(0.708_0_0)] mb-2">Original Transcript</h4>
                    <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                      <p className="text-white">{selectedClaim.originalTranscript}</p>
                    </div>
                  </div>

                  {/* Translated Claim */}
                  <div>
                    <h4 className="text-sm font-medium text-[oklch(0.708_0_0)] mb-2">Translated Claim (English)</h4>
                    <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                      <p className="text-white">{selectedClaim.translatedClaim}</p>
                    </div>
                  </div>

                  {/* Verdict and Confidence */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-[oklch(0.708_0_0)] mb-2">Verdict</h4>
                      <VerdictBadge verdict={selectedClaim.verdict} />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-[oklch(0.708_0_0)] mb-2">Confidence Score</h4>
                      <p className="text-2xl font-semibold text-white">{selectedClaim.confidence}%</p>
                    </div>
                  </div>

                  {/* Virality Risk */}
                  <div>
                    <RiskMeter score={selectedClaim.viralityRisk} />
                  </div>
                </CardContent>
              </Card>

              {/* Explanation */}
              <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
                <CardHeader>
                  <CardTitle className="text-white">Fact Check Explanation</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-[oklch(0.708_0_0)] leading-relaxed">{selectedClaim.explanation}</p>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
              <CardContent className="py-12">
                <div className="text-center text-[oklch(0.708_0_0)]">
                  <p>Select a claim from the table to view details</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
