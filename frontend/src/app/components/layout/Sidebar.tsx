import { Link, useLocation } from "react-router";
import { LayoutDashboard, History, Languages, Users, Settings, BarChart3, Repeat, MessageSquareText, LogOut, User } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

const clientNavigation = [
  { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { path: "/dashboard/history", label: "Fact Check History", icon: History },
  { path: "/dashboard/translation", label: "Language & Translation", icon: Languages },
  { path: "/dashboard/collaboration", label: "Partner Collaboration", icon: Users },
];

const adminNavigation = [
  { path: "/admin", label: "Admin Dashboard", icon: BarChart3 },
  { path: "/admin/trends", label: "Misinformation Trends", icon: LayoutDashboard },
  { path: "/admin/language", label: "Language Analytics", icon: Languages },
  { path: "/admin/repeat-claims", label: "Repeat Claims", icon: Repeat },
  { path: "/admin/feedback", label: "Model Feedback", icon: MessageSquareText },
];

export default function Sidebar() {
  const location = useLocation();
  const { user, logout } = useAuth();

  const isAdmin = user?.role === "admin";

  return (
    <aside className="w-64 bg-[oklch(0.205_0_0)] border-r border-[oklch(0.269_0_0)] flex flex-col h-screen fixed left-0 top-0">
      <div className="p-6 border-b border-[oklch(0.269_0_0)]">
        <h1 className="text-xl text-white font-semibold">FactCheck Portal</h1>
        <p className="text-sm text-[oklch(0.708_0_0)] mt-1">Client Dashboard</p>
      </div>
      <nav className="flex-1 p-4 overflow-y-auto">
        <div className="mb-4">
          <p className="px-4 text-xs font-semibold text-[oklch(0.708_0_0)] uppercase tracking-wider mb-2">
            Client
          </p>
          <ul className="space-y-1">
            {clientNavigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${isActive
                      ? "bg-[oklch(0.488_0.243_264.376)] text-white"
                      : "text-[oklch(0.708_0_0)] hover:bg-[oklch(0.269_0_0)] hover:text-white"
                      }`}
                  >
                    <Icon size={18} />
                    <span>{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>

        {isAdmin && (
          <div className="mt-8">
            <p className="px-4 text-xs font-semibold text-[oklch(0.708_0_0)] uppercase tracking-wider mb-2">
              Admin
            </p>
            <ul className="space-y-1">
              {adminNavigation.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;

                return (
                  <li key={item.path}>
                    <Link
                      to={item.path}
                      className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${isActive
                        ? "bg-[oklch(0.488_0.243_264.376)] text-white"
                        : "text-[oklch(0.708_0_0)] hover:bg-[oklch(0.269_0_0)] hover:text-white"
                        }`}
                    >
                      <Icon size={18} />
                      <span>{item.label}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        )}
      </nav>
      <div className="p-4 border-t border-[oklch(0.269_0_0)] mt-auto">
        {user && (
          <div className="flex items-center gap-3 px-4 py-3 mb-4 bg-[oklch(0.269_0_0)] rounded-xl">
            <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-500">
              <User size={16} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-white truncate">{user.name || "User"}</p>
              <p className="text-[10px] text-[oklch(0.708_0_0)] truncate">{user.role}</p>
            </div>
          </div>
        )}
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-4 py-2 text-[oklch(0.708_0_0)] hover:bg-red-500/10 hover:text-red-500 rounded-lg transition-colors mb-2"
        >
          <LogOut size={18} />
          <span className="text-sm font-medium">Logout</span>
        </button>
        <div className="text-[10px] text-[oklch(0.708_0_0)] text-center">
          © 2026 Tattva-AI
        </div>
      </div>
    </aside>
  );
}
