import { Outlet, Link, useLocation } from "react-router";
import {
    LayoutDashboard,
    TrendingUp,
    RefreshCcw,
    Languages,
    MessageSquareDot,
    Search,
    Bell,
    Activity,
    LogOut,
} from "lucide-react";
import { useAuth } from "../../auth/AuthContext";
import { useEffect, useState } from "react";
import { db } from "../../../core/firebase/firebase";
import { collection, query, orderBy, onSnapshot, limit } from "firebase/firestore";
import { toast } from "sonner";

const navigation = [
    { name: "Dashboard Overview", href: "/admin", icon: LayoutDashboard },
    { name: "Misinformation Trends", href: "/admin/trends", icon: TrendingUp },
    { name: "Repeat Claims", href: "/admin/repeat-claims", icon: RefreshCcw },
    { name: "Language Analytics", href: "/admin/language", icon: Languages },
    { name: "Model Feedback", href: "/admin/feedback", icon: MessageSquareDot },
    { name: "Discrepancy Reports", href: "/admin/discrepancies", icon: Bell },
];

export default function AdminLayout() {
    const location = useLocation();
    const { logout } = useAuth();
    const [unreadCount, setUnreadCount] = useState(0);
    const [isInitialLoad, setIsInitialLoad] = useState(true);

    useEffect(() => {
        const q = query(collection(db, "discrepancies"), orderBy("submittedDate", "desc"), limit(20));

        const unsubscribe = onSnapshot(q, (snapshot) => {
            if (isInitialLoad) {
                // Count pending reports on initial load
                const pendingCount = snapshot.docs.filter(doc => doc.data().status === "Pending").length;
                setUnreadCount(pendingCount);
                setIsInitialLoad(false);
            } else {
                // Check if any new documents (added after initial load)
                snapshot.docChanges().forEach((change) => {
                    if (change.type === "added") {
                        const data = change.doc.data();
                        setUnreadCount(prev => prev + 1);
                        toast.info("New Discrepancy Reported", {
                            description: `Claim ${data.claimId}: ${data.issueType}`,
                            action: {
                                label: "View",
                                onClick: () => window.location.href = "/admin/discrepancies"
                            },
                        });
                    }
                });
            }
        });

        return () => unsubscribe();
    }, [isInitialLoad]);

    return (
        <div className="dark flex h-screen bg-neutral-950 text-neutral-100">
            {/* Sidebar */}
            <aside className="w-64 bg-neutral-900 border-r border-neutral-800 flex flex-col">
                <div className="p-6 border-b border-neutral-800">
                    <Link to="/admin">
                        <h1 className="text-xl font-semibold text-blue-400">MisInfo Monitor</h1>
                    </Link>
                </div>
                <nav className="flex-1 p-4 space-y-1">
                    {navigation.map((item) => {
                        const isActive = location.pathname === item.href;
                        return (
                            <Link
                                key={item.name}
                                to={item.href}
                                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${isActive
                                    ? "bg-blue-600 text-white"
                                    : "text-neutral-400 hover:bg-neutral-800 hover:text-neutral-100"
                                    }`}
                            >
                                <item.icon className="w-5 h-5" />
                                <span>{item.name}</span>
                            </Link>
                        );
                    })}
                </nav>

                {/* Logout Button */}
                <div className="p-4 border-t border-neutral-800">
                    <button
                        onClick={logout}
                        className="w-full flex items-center gap-3 px-4 py-3 text-neutral-400 hover:bg-neutral-800 hover:text-red-400 rounded-lg transition-colors"
                    >
                        <LogOut className="w-5 h-5" />
                        <span>Logout</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Top Navigation Bar */}
                <header className="h-16 bg-neutral-900 border-b border-neutral-800 flex items-center justify-between px-8">
                    <h2 className="text-lg font-medium">
                        Misinformation Monitoring Admin Panel
                    </h2>
                    <div className="flex items-center gap-6">
                        {/* Search */}
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-500" />
                            <input
                                type="text"
                                placeholder="Search..."
                                className="pl-10 pr-4 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-sm focus:outline-none focus:border-blue-500 w-64"
                            />
                        </div>

                        {/* System Status */}
                        <div className="flex items-center gap-2 px-3 py-2 bg-green-950 border border-green-800 rounded-lg">
                            <Activity className="w-4 h-4 text-green-400" />
                            <span className="text-sm text-green-400">Online</span>
                        </div>

                        {/* Notifications */}
                        <Link to="/admin/discrepancies" className="relative p-2 hover:bg-neutral-800 rounded-lg transition-colors">
                            <Bell className="w-5 h-5 text-neutral-400" />
                            {unreadCount > 0 && (
                                <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-[10px] text-white font-bold">
                                    {unreadCount > 9 ? "9+" : unreadCount}
                                </span>
                            )}
                        </Link>

                        {/* Admin Profile */}
                        <div className="flex items-center gap-3">
                            <div className="w-9 h-9 bg-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                                AD
                            </div>
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 overflow-auto bg-neutral-950">
                    <div className="p-8">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
}
