import { createBrowserRouter } from "react-router";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import MisinformationTrends from "./pages/MisinformationTrends";
import RepeatClaims from "./pages/RepeatClaims";
import LanguageAnalytics from "./pages/LanguageAnalytics";
import ModelFeedback from "./pages/ModelFeedback";

// Admin Pages
import AdminDashboard from "./pages/admin/Dashboard";
import AdminTrends from "./pages/admin/MisinformationTrends";
import AdminLanguage from "./pages/admin/LanguageAnalytics";
import AdminFeedback from "./pages/admin/ModelFeedback";
import AdminRepeatClaims from "./pages/admin/RepeatClaims";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: Dashboard },
      { path: "trends", Component: MisinformationTrends },
      { path: "repeat-claims", Component: RepeatClaims },
      { path: "language", Component: LanguageAnalytics },
      { path: "feedback", Component: ModelFeedback },

      // Admin Routes
      { path: "admin", Component: AdminDashboard },
      { path: "admin/trends", Component: AdminTrends },
      { path: "admin/language", Component: AdminLanguage },
      { path: "admin/feedback", Component: AdminFeedback },
      { path: "admin/repeat-claims", Component: AdminRepeatClaims },
    ],
  },
]);
