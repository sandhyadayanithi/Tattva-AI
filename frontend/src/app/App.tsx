import { RouterProvider } from "react-router";
import { router } from "./routes";
import { Toaster } from "./shared/components/ui/sonner";
import { AuthProvider } from "./features/auth/AuthContext";

export default function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
      <Toaster />
    </AuthProvider>
  );
}

