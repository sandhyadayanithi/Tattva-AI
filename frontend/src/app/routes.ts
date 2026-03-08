import { createBrowserRouter } from "react-router";
import DashboardLayout from "./components/layout/DashboardLayout";
import FactCheckHistory from "./pages/FactCheckHistory";
import LanguageTranslation from "./pages/LanguageTranslation";
import PartnerCollaboration from "./pages/PartnerCollaboration";
import Dashboard from "./pages/Dashboard";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: DashboardLayout,
    children: [
      { index: true, Component: Dashboard },
      { path: "history", Component: FactCheckHistory },
      { path: "translation", Component: LanguageTranslation },
      { path: "collaboration", Component: PartnerCollaboration },
    ],
  },
]);
