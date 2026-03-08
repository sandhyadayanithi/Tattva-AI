import MetricCard from "../../components/MetricCard";
import { Card } from "../../components/ui/card";
import {
    mockMetrics,
    generateSparklineData,
    mockTrendData,
    mockTopicDistribution,
    mockTrendingNarratives,
} from "../../data/adminMockData";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
} from "recharts";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "../../components/ui/table";
import { Badge } from "../../components/ui/badge";

export default function AdminDashboardOverview() {
    return (
        <div className="space-y-6 text-neutral-100">
            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <MetricCard
                    title="Total Messages Processed"
                    value={mockMetrics.totalMessages.toLocaleString()}
                    trend={12.5}
                    sparklineData={generateSparklineData()}
                />
                <MetricCard
                    title="Messages Processed Today"
                    value={mockMetrics.todayMessages.toLocaleString()}
                    trend={8.3}
                    sparklineData={generateSparklineData()}
                />
                <MetricCard
                    title="Average Processing Time"
                    value={mockMetrics.avgProcessingTime}
                    suffix="sec"
                    trend={-5.2}
                    sparklineData={generateSparklineData()}
                />
                <MetricCard
                    title="Pipeline Success Rate"
                    value={mockMetrics.successRate}
                    suffix="%"
                    trend={2.1}
                    sparklineData={generateSparklineData()}
                />
                <MetricCard
                    title="Failed Jobs"
                    value={mockMetrics.failedJobs}
                    trend={-15.4}
                    sparklineData={generateSparklineData()}
                />
                <MetricCard
                    title="Pending Queue Size"
                    value={mockMetrics.pendingQueue}
                    trend={3.7}
                    sparklineData={generateSparklineData()}
                />
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="p-6 bg-neutral-900 border-neutral-800">
                    <h3 className="text-lg font-semibold text-white mb-4">
                        Claims Detected Over Time
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={mockTrendData}>
                            <CartesianGrid
                                strokeDasharray="3 3"
                                stroke="#404040"
                                opacity={0.2}
                            />
                            <XAxis
                                dataKey="date"
                                stroke="#a3a3a3"
                                tick={{ fill: "#a3a3a3" }}
                                style={{ fontSize: "12px" }}
                            />
                            <YAxis stroke="#a3a3a3" tick={{ fill: "#a3a3a3" }} />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: "#171717",
                                    border: "1px solid #262626",
                                    borderRadius: "8px",
                                    color: "#fff",
                                }}
                            />
                            <Line
                                type="monotone"
                                dataKey="claims"
                                stroke="#3b82f6"
                                strokeWidth={2}
                                dot={{ fill: "#3b82f6" }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </Card>

                <Card className="p-6 bg-neutral-900 border-neutral-800">
                    <h3 className="text-lg font-semibold text-white mb-4">
                        Topic Distribution
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={mockTopicDistribution}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={({ name, percent }) =>
                                    `${name} ${(percent * 100).toFixed(0)}%`
                                }
                                outerRadius={80}
                                fill="#8884d8"
                                dataKey="value"
                            >
                                {mockTopicDistribution.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: "#171717",
                                    border: "1px solid #262626",
                                    borderRadius: "8px",
                                    color: "#fff",
                                }}
                            />
                        </PieChart>
                    </ResponsiveContainer>
                </Card>
            </div>

            {/* Trending Narratives Table */}
            <Card className="p-6 bg-neutral-900 border-neutral-800">
                <h3 className="text-lg font-semibold text-white mb-4">
                    Trending Misinformation Narratives
                </h3>
                <div className="overflow-x-auto">
                    <Table>
                        <TableHeader>
                            <TableRow className="border-neutral-800 hover:bg-neutral-800/50">
                                <TableHead className="text-neutral-400">Claim Summary</TableHead>
                                <TableHead className="text-neutral-400">Language</TableHead>
                                <TableHead className="text-right text-neutral-400">Detected Messages</TableHead>
                                <TableHead className="text-right text-neutral-400">Virality Score</TableHead>
                                <TableHead className="text-neutral-400">First Detected</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {mockTrendingNarratives.map((item) => (
                                <TableRow key={item.id} className="border-neutral-800 hover:bg-neutral-800/50">
                                    <TableCell className="font-medium max-w-md text-neutral-200">
                                        {item.claim}
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="secondary" className="bg-neutral-800 text-neutral-300 border-neutral-700">{item.language}</Badge>
                                    </TableCell>
                                    <TableCell className="text-right text-neutral-300">
                                        {item.messages.toLocaleString()}
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Badge
                                            className={
                                                item.virality >= 8
                                                    ? "bg-red-950 text-red-400 border-red-900"
                                                    : item.virality >= 6
                                                        ? "bg-orange-950 text-orange-400 border-orange-900"
                                                        : "bg-green-950 text-green-400 border-green-900"
                                            }
                                        >
                                            {item.virality.toFixed(1)}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-sm text-neutral-400">
                                        {item.firstDetected}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
            </Card>
        </div>
    );
}
