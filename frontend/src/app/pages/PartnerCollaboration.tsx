import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Button } from "../components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../components/ui/select";
import { mockReports, type Claim } from "../data/mockData";
import StatusBadge from "../components/StatusBadge";
import { AlertCircle, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

export default function PartnerCollaboration() {
  const [formData, setFormData] = useState({
    claimId: "",
    issueType: "",
    explanation: "",
  });

  const [submittedReports, setSubmittedReports] = useState(mockReports);
  const [claims, setClaims] = useState<Claim[]>([]);

  useEffect(() => {
    fetch("/api/claims")
      .then(res => res.json())
      .then(data => setClaims(data))
      .catch(err => console.error("Error fetching claims:", err));
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.claimId || !formData.issueType || !formData.explanation) {
      toast.error("Please fill in all fields");
      return;
    }

    const newReport = {
      id: `DR-${String(submittedReports.length + 1).padStart(3, "0")}`,
      claimId: formData.claimId,
      issueType: formData.issueType,
      submittedDate: new Date().toISOString().split("T")[0],
      status: "Pending" as const,
      explanation: formData.explanation,
    };

    setSubmittedReports([newReport, ...submittedReports]);
    setFormData({ claimId: "", issueType: "", explanation: "" });
    
    toast.success("Report submitted successfully", {
      description: "Your discrepancy report has been received and will be reviewed.",
    });
  };

  return (
    <div className="space-y-6">
      {/* Info Banner */}
      <Card className="bg-[oklch(0.488_0.243_264.376)]/10 border-[oklch(0.488_0.243_264.376)]/30">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="text-[oklch(0.488_0.243_264.376)] mt-0.5" size={20} />
            <div>
              <h3 className="text-white font-medium mb-1">Partner Collaboration Portal</h3>
              <p className="text-sm text-[oklch(0.708_0_0)]">
                As a trusted partner, you can report discrepancies in fact-check results to help improve 
                accuracy. Our team will review your submissions and update the records accordingly.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-2 gap-6">
        {/* Discrepancy Report Form */}
        <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
          <CardHeader>
            <CardTitle className="text-white">Report Discrepancy</CardTitle>
            <p className="text-sm text-[oklch(0.708_0_0)]">
              Submit issues or corrections for fact-check results
            </p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Claim ID Selector */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Claim ID</label>
                <Select 
                  value={formData.claimId} 
                  onValueChange={(value) => setFormData({ ...formData, claimId: value })}
                >
                  <SelectTrigger className="bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white">
                    <SelectValue placeholder="Select a claim" />
                  </SelectTrigger>
                  <SelectContent>
                    {claims.map((claim) => (
                      <SelectItem key={claim.id} value={claim.id}>
                        {claim.id} - {claim.claimSummary?.substring(0, 50)}...
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Issue Type */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Issue Type</label>
                <Select 
                  value={formData.issueType} 
                  onValueChange={(value) => setFormData({ ...formData, issueType: value })}
                >
                  <SelectTrigger className="bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white">
                    <SelectValue placeholder="Select issue type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Incorrect verdict">Incorrect verdict</SelectItem>
                    <SelectItem value="Incorrect transcript">Incorrect transcript</SelectItem>
                    <SelectItem value="Missing evidence">Missing evidence</SelectItem>
                    <SelectItem value="Translation error">Translation error</SelectItem>
                    <SelectItem value="Other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Explanation */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Explanation</label>
                <Textarea
                  value={formData.explanation}
                  onChange={(e) => setFormData({ ...formData, explanation: e.target.value })}
                  placeholder="Describe the issue in detail..."
                  className="bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white placeholder:text-[oklch(0.708_0_0)] min-h-32"
                />
              </div>

              {/* Submit Button */}
              <Button 
                type="submit"
                className="w-full bg-[oklch(0.488_0.243_264.376)] hover:bg-[oklch(0.488_0.243_264.376)]/90 text-white"
              >
                Submit Report
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Guidelines */}
        <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
          <CardHeader>
            <CardTitle className="text-white">Reporting Guidelines</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="text-[oklch(0.696_0.17_162.48)] mt-0.5 flex-shrink-0" size={18} />
              <div>
                <h4 className="text-white font-medium mb-1">Be Specific</h4>
                <p className="text-sm text-[oklch(0.708_0_0)]">
                  Provide detailed information about the issue, including specific references to the claim or explanation.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <CheckCircle2 className="text-[oklch(0.696_0.17_162.48)] mt-0.5 flex-shrink-0" size={18} />
              <div>
                <h4 className="text-white font-medium mb-1">Provide Evidence</h4>
                <p className="text-sm text-[oklch(0.708_0_0)]">
                  Include links, references, or sources that support your observation or correction.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <CheckCircle2 className="text-[oklch(0.696_0.17_162.48)] mt-0.5 flex-shrink-0" size={18} />
              <div>
                <h4 className="text-white font-medium mb-1">Professional Tone</h4>
                <p className="text-sm text-[oklch(0.708_0_0)]">
                  Maintain a constructive and professional tone in your explanations.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <CheckCircle2 className="text-[oklch(0.696_0.17_162.48)] mt-0.5 flex-shrink-0" size={18} />
              <div>
                <h4 className="text-white font-medium mb-1">Response Time</h4>
                <p className="text-sm text-[oklch(0.708_0_0)]">
                  Reports are typically reviewed within 48-72 hours. You'll receive updates via email.
                </p>
              </div>
            </div>

            <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg mt-6">
              <h4 className="text-white font-medium mb-2">Contact Support</h4>
              <p className="text-sm text-[oklch(0.708_0_0)]">
                For urgent issues, contact us at{" "}
                <span className="text-[oklch(0.488_0.243_264.376)]">support@factcheck.org</span>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* My Submitted Reports */}
      <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
        <CardHeader>
          <CardTitle className="text-white">My Submitted Reports</CardTitle>
          <p className="text-sm text-[oklch(0.708_0_0)]">
            Track the status of your discrepancy reports
          </p>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-[oklch(0.269_0_0)]">
                  <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">
                    Report ID
                  </th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">
                    Claim ID
                  </th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">
                    Issue Type
                  </th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">
                    Submitted Date
                  </th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">
                    Status
                  </th>
                  <th className="text-left py-3 px-4 text-xs font-medium text-[oklch(0.708_0_0)] uppercase">
                    Explanation
                  </th>
                </tr>
              </thead>
              <tbody>
                {submittedReports.map((report) => (
                  <tr
                    key={report.id}
                    className="border-b border-[oklch(0.269_0_0)] hover:bg-[oklch(0.269_0_0)] transition-colors"
                  >
                    <td className="py-3 px-4 text-sm text-white font-medium">{report.id}</td>
                    <td className="py-3 px-4 text-sm text-[oklch(0.708_0_0)]">{report.claimId}</td>
                    <td className="py-3 px-4 text-sm text-white">{report.issueType}</td>
                    <td className="py-3 px-4 text-sm text-[oklch(0.708_0_0)]">
                      {new Date(report.submittedDate).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-4">
                      <StatusBadge status={report.status} />
                    </td>
                    <td className="py-3 px-4 text-sm text-[oklch(0.708_0_0)] max-w-md truncate">
                      {report.explanation}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {submittedReports.length === 0 && (
            <div className="text-center py-12 text-[oklch(0.708_0_0)]">
              <p>No reports submitted yet</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
