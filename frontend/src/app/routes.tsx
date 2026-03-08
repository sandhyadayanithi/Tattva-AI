import { createBrowserRouter } from "react-router";
import DashboardLayout from "./components/layout/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import FactCheckHistory from "./pages/FactCheckHistory";
import LanguageTranslation from "./pages/LanguageTranslation";
import PartnerCollaboration from "./pages/PartnerCollaboration";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./components/ProtectedRoute";

// Admin Components & Layout
import AdminLayout from "./components/admin/AdminLayout";
import AdminDashboardOverview from "./pages/admin/AdminDashboardOverview";

// Admin Sub-Pages
import AdminTrends from "./pages/admin/MisinformationTrends";
import AdminLanguage from "./pages/admin/LanguageAnalytics";
import AdminFeedback from "./pages/admin/ModelFeedback";
import AdminRepeatClaims from "./pages/admin/RepeatClaims";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: LoginPage,
  },
  {
    path: "/login",
    Component: LoginPage,
  },
  {
    path: "/dashboard",
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, Component: Dashboard },
      { path: "history", Component: FactCheckHistory },
      { path: "translation", Component: LanguageTranslation },
      { path: "collaboration", Component: PartnerCollaboration },
    ],
  },
  {
    path: "/admin",
    element: (
      <ProtectedRoute requiredRole="admin">
        <AdminLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, Component: AdminDashboardOverview },
      { path: "trends", Component: AdminTrends },
      { path: "language", Component: AdminLanguage },
      { path: "feedback", Component: AdminFeedback },
      { path: "repeat-claims", Component: AdminRepeatClaims },
    ],
  },
]);
