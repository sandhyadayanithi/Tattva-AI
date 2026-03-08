import {
  MessageSquare,
  CheckCircle2,
  ShieldCheck,
  Clock
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";

const stats = [
  {
    title: "Total Claims",
    value: "1,284",
    icon: MessageSquare,
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
    change: "+12%"
  },
  {
    title: "Verified True",
    value: "842",
    icon: CheckCircle2,
    color: "text-green-500",
    bgColor: "bg-green-500/10",
    change: "+18%"
  },
  {
    title: "Average Confidence",
    value: "88%",
    icon: ShieldCheck,
    color: "text-purple-500",
    bgColor: "bg-purple-500/10",
    change: "+2%"
  },
  {
    title: "Pending Review",
    value: "42",
    icon: Clock,
    color: "text-amber-500",
    bgColor: "bg-amber-500/10",
    change: "-5%"
  }
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
