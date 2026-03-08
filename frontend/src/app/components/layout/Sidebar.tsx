import { Link, useLocation } from "react-router";
import { LayoutDashboard, History, Languages, Users } from "lucide-react";

const navigationItems = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/history", label: "Fact Check History", icon: History },
  { path: "/translation", label: "Language & Translation", icon: Languages },
  { path: "/collaboration", label: "Partner Collaboration", icon: Users },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 bg-[oklch(0.205_0_0)] border-r border-[oklch(0.269_0_0)] flex flex-col h-screen fixed left-0 top-0">
      <div className="p-6 border-b border-[oklch(0.269_0_0)]">
        <h1 className="text-xl text-white font-semibold">FactCheck Portal</h1>
        <p className="text-sm text-[oklch(0.708_0_0)] mt-1">Client Dashboard</p>
      </div>
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? "bg-[oklch(0.488_0.243_264.376)] text-white"
                      : "text-[oklch(0.708_0_0)] hover:bg-[oklch(0.269_0_0)] hover:text-white"
                  }`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      <div className="p-4 border-t border-[oklch(0.269_0_0)]">
        <div className="text-xs text-[oklch(0.708_0_0)]">
          © 2026 FactCheck Portal
        </div>
      </div>
    </aside>
  );
}
