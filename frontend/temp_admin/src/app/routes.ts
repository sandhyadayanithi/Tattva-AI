import { createBrowserRouter } from "react-router";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import MisinformationTrends from "./pages/MisinformationTrends";
import RepeatClaims from "./pages/RepeatClaims";
import LanguageAnalytics from "./pages/LanguageAnalytics";
import ModelFeedback from "./pages/ModelFeedback";

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
    ],
  },
]);