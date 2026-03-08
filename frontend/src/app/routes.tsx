import { createBrowserRouter } from "react-router";
import DashboardLayout from "./shared/components/layout/DashboardLayout";
import Dashboard from "./features/client/Dashboard";
import FactCheckHistory from "./features/client/FactCheckHistory";
import LanguageTranslation from "./features/client/LanguageTranslation";
import PartnerCollaboration from "./features/client/PartnerCollaboration";
import LoginPage from "./features/auth/LoginPage";
import ProtectedRoute from "./shared/components/ProtectedRoute";

// Admin Components & Layout
import AdminLayout from "./features/admin/components/AdminLayout";
import AdminDashboardOverview from "./features/admin/AdminDashboardOverview";

// Admin Sub-Pages
import AdminTrends from "./features/admin/MisinformationTrends";
import AdminLanguage from "./features/admin/LanguageAnalytics";
import AdminFeedback from "./features/admin/ModelFeedback";
import AdminRepeatClaims from "./features/admin/RepeatClaims";
import DiscrepancyList from "./features/admin/DiscrepancyList";

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
      { path: "discrepancies", Component: DiscrepancyList },
    ],
  },
]);
