import { useEffect, useState } from "react";
import { db } from "../../core/firebase/firebase";
import { collection, query, orderBy, onSnapshot, doc, updateDoc } from "firebase/firestore";
import { Card, CardContent, CardHeader, CardTitle } from "../../shared/components/ui/card";
import StatusBadge from "../../shared/components/ui/StatusBadge";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "../../shared/components/ui/table";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../shared/components/ui/select";
import { toast } from "sonner";

export default function DiscrepancyList() {
    const [reports, setReports] = useState<any[]>([]);

    useEffect(() => {
        const q = query(collection(db, "discrepancies"), orderBy("submittedDate", "desc"));
        const unsubscribe = onSnapshot(q, (snapshot) => {
            const docs = snapshot.docs.map((doc) => ({
                id: doc.id,
                ...doc.data(),
            }));
            setReports(docs);
        });

        return () => unsubscribe();
    }, []);

    const handleStatusChange = async (id: string, newStatus: string) => {
        try {
            await updateDoc(doc(db, "discrepancies", id), {
                status: newStatus,
            });
            toast.success(`Status updated to ${newStatus}`);
        } catch (error) {
            console.error("Error updating status:", error);
            toast.error("Failed to update status");
        }
    };

    return (
        <div className="space-y-6 text-neutral-100">
            <div>
                <h2 className="text-2xl font-semibold mb-2">Discrepancy Reports</h2>
                <p className="text-neutral-400">
                    Review and manage discrepancies submitted by partners
                </p>
            </div>

            <Card className="bg-neutral-900 border-neutral-800">
                <CardHeader>
                    <CardTitle className="text-white">Partner Submissions</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="overflow-x-auto">
                        <Table>
                            <TableHeader>
                                <TableRow className="border-neutral-800 hover:bg-neutral-800/50">
                                    <TableHead className="text-neutral-400">Report ID</TableHead>
                                    <TableHead className="text-neutral-400">Claim ID</TableHead>
                                    <TableHead className="text-neutral-400">Issue Type</TableHead>
                                    <TableHead className="text-neutral-400">Date</TableHead>
                                    <TableHead className="text-neutral-400">Status</TableHead>
                                    <TableHead className="text-neutral-400">Action</TableHead>
                                    <TableHead className="text-neutral-400">Explanation</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {reports.map((report) => (
                                    <TableRow key={report.id} className="border-neutral-800 hover:bg-neutral-800/50">
                                        <TableCell className="font-medium text-neutral-200 truncate max-w-[100px]">
                                            {report.id}
                                        </TableCell>
                                        <TableCell className="text-neutral-300">{report.claimId}</TableCell>
                                        <TableCell className="text-neutral-200">{report.issueType}</TableCell>
                                        <TableCell className="text-neutral-400">
                                            {report.submittedDate?.seconds
                                                ? new Date(report.submittedDate.seconds * 1000).toLocaleDateString()
                                                : "Pending..."}
                                        </TableCell>
                                        <TableCell>
                                            <StatusBadge status={report.status} />
                                        </TableCell>
                                        <TableCell>
                                            <Select
                                                value={report.status}
                                                onValueChange={(value) => handleStatusChange(report.id, value)}
                                            >
                                                <SelectTrigger className="w-[130px] bg-neutral-800 border-neutral-700 text-neutral-200">
                                                    <SelectValue placeholder="Update Status" />
                                                </SelectTrigger>
                                                <SelectContent className="bg-neutral-800 border-neutral-700 text-neutral-200">
                                                    <SelectItem value="Pending">Pending</SelectItem>
                                                    <SelectItem value="Reviewing">Reviewing</SelectItem>
                                                    <SelectItem value="Resolved">Resolved</SelectItem>
                                                    <SelectItem value="Dismissed">Dismissed</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </TableCell>
                                        <TableCell className="text-neutral-400 max-w-xs truncate">
                                            {report.explanation}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                    {reports.length === 0 && (
                        <div className="text-center py-12 text-neutral-500">
                            <p>No discrepancy reports found</p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
