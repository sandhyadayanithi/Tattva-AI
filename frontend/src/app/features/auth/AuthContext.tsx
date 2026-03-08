import React, { createContext, useContext, useState, useEffect } from "react";
import { auth, googleProvider } from "../../core/firebase/firebase";
import { signInWithPopup, signOut, onAuthStateChanged, User as FirebaseUser } from "firebase/auth";

type Role = "client" | "admin" | null;

interface User {
    email: string;
    role: Role;
    name?: string;
    photoURL?: string;
}

interface AuthContextType {
    user: User | null;
    login: (email: string, password: string) => Promise<boolean>;
    googleLogin: () => Promise<boolean>;
    logout: () => void;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Temporary Admin Credentials
const ADMIN_EMAIL = "admin@tattva.ai";
const ADMIN_PASSWORD = "admin123";

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(() => {
        const stored = localStorage.getItem("tattva_user");
        try {
            return stored ? JSON.parse(stored) : null;
        } catch (e) {
            return null;
        }
    });
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Use Firebase onAuthStateChanged to persist session
        const unsubscribe = onAuthStateChanged(auth, (firebaseUser: FirebaseUser | null) => {
            if (firebaseUser) {
                const role: Role = firebaseUser.email === ADMIN_EMAIL ? "admin" : "client";
                const userData: User = {
                    email: firebaseUser.email || "",
                    role,
                    name: firebaseUser.displayName || "",
                    photoURL: firebaseUser.photoURL || ""
                };
                setUser(userData);
                localStorage.setItem("tattva_user", JSON.stringify(userData));
            } else {
                // Only clear the user if there's no manual session in localStorage
                // This prevents manual logins (admin/email) from being cleared by the Firebase observer
                const storedUser = localStorage.getItem("tattva_user");
                if (!storedUser) {
                    setUser(null);
                } else {
                    // Sync state with storage for manual sessions
                    try {
                        setUser(JSON.parse(storedUser));
                    } catch (e) {
                        setUser(null);
                        localStorage.removeItem("tattva_user");
                    }
                }
            }
            setIsLoading(false);
        });

        return () => unsubscribe();
    }, []);

    const login = async (email: string, password: string): Promise<boolean> => {
        setIsLoading(true);
        // Simulate API call for admin or custom login
        await new Promise((resolve) => setTimeout(resolve, 800));

        if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
            const adminUser: User = { email, role: "admin", name: "System Admin" };
            setUser(adminUser);
            localStorage.setItem("tattva_user", JSON.stringify(adminUser));
            setIsLoading(false);
            return true;
        } else if (email && password) {
            // Support for other email/password if needed, currently simulate
            const clientUser: User = { email, role: "client", name: email.split("@")[0] };
            setUser(clientUser);
            localStorage.setItem("tattva_user", JSON.stringify(clientUser));
            setIsLoading(false);
            return true;
        }

        setIsLoading(false);
        return false;
    };

    const googleLogin = async (): Promise<boolean> => {
        setIsLoading(true);
        try {
            const result = await signInWithPopup(auth, googleProvider);
            const firebaseUser = result.user;

            const role: Role = firebaseUser.email === ADMIN_EMAIL ? "admin" : "client";
            const userData: User = {
                email: firebaseUser.email || "",
                role,
                name: firebaseUser.displayName || "",
                photoURL: firebaseUser.photoURL || ""
            };

            setUser(userData);
            localStorage.setItem("tattva_user", JSON.stringify(userData));
            setIsLoading(false);
            return true;
        } catch (error) {
            console.error("Google Login Error:", error);
            setIsLoading(false);
            return false;
        }
    };

    const logout = async () => {
        try {
            await signOut(auth);
            setUser(null);
            localStorage.removeItem("tattva_user");
        } catch (error) {
            console.error("Logout Error:", error);
        }
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
