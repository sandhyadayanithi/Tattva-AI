import React from "react";
import { Navigate, useLocation } from "react-router";
import { useAuth } from "../../features/auth/AuthContext";

interface ProtectedRouteProps {
    children: React.ReactNode;
    requiredRole?: "admin" | "client";
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole }) => {
    const { user, isLoading } = useAuth();
    const location = useLocation();

    if (isLoading) {
        return (
            <div className="h-screen w-screen flex items-center justify-center bg-black">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (!user) {
        // Redirect to login if not authenticated
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    if (requiredRole && user.role !== requiredRole) {
        // Redirect to appropriate dashboard if role doesn't match
        return <Navigate to={user.role === "admin" ? "/admin" : "/"} replace />;
    }

    return <>{children}</>;
};

export default ProtectedRoute;
