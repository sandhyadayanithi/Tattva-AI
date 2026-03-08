import React, { createContext, useContext, useState, useEffect } from "react";

type Role = "client" | "admin" | null;

interface User {
    email: string;
    role: Role;
    name?: string;
}

interface AuthContextType {
    user: User | null;
    login: (email: string, password: string) => Promise<boolean>;
    googleLogin: () => Promise<void>;
    logout: () => void;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Temporary Admin Credentials
const ADMIN_EMAIL = "admin@tattva.ai";
const ADMIN_PASSWORD = "admin123";

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check local storage for existing session
        const savedUser = localStorage.getItem("tattva_user");
        if (savedUser) {
            setUser(JSON.parse(savedUser));
        }
        setIsLoading(false);
    }, []);

    const login = async (email: string, password: string): Promise<boolean> => {
        setIsLoading(true);
        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 800));

        if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
            const adminUser: User = { email, role: "admin", name: "System Admin" };
            setUser(adminUser);
            localStorage.setItem("tattva_user", JSON.stringify(adminUser));
            setIsLoading(false);
            return true;
        } else if (email && password) {
            // Simulate successful client login for any other email
            const clientUser: User = { email, role: "client", name: email.split("@")[0] };
            setUser(clientUser);
            localStorage.setItem("tattva_user", JSON.stringify(clientUser));
            setIsLoading(false);
            return true;
        }

        setIsLoading(false);
        return false;
    };

    const googleLogin = async () => {
        setIsLoading(true);
        // Simulate Google OAuth popup
        await new Promise((resolve) => setTimeout(resolve, 1200));
        const googleUser: User = { email: "user@gmail.com", role: "client", name: "Google User" };
        setUser(googleUser);
        localStorage.setItem("tattva_user", JSON.stringify(googleUser));
        setIsLoading(false);
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem("tattva_user");
    };

    return (
        <AuthContext.Provider value={{ user, login, googleLogin, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
