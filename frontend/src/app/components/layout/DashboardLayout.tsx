import { Outlet } from "react-router";
import Sidebar from "./Sidebar";
import TopNav from "./TopNav";

const pageTitles: Record<string, string> = {
  "/": "Fact Check Dashboard",
  "/history": "Fact Check History",
  "/translation": "Language & Translation",
  "/collaboration": "Partner Collaboration",
};

export default function DashboardLayout() {
  const currentPath = window.location.pathname;
  const title = pageTitles[currentPath] || "Fact Check Dashboard";

  return (
    <div className="dark min-h-screen bg-[oklch(0.145_0_0)]">
      <Sidebar />
      <div className="ml-64 flex flex-col min-h-screen">
        <TopNav title={title} />
        <main className="flex-1 p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
