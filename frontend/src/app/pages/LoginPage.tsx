import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, useLocation } from "react-router";
import { Mail, Lock, ShieldCheck, Github, Chrome, AlertCircle } from "lucide-react";

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { login, googleLogin } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const from = (location.state as any)?.from?.pathname || "/";

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        const success = await login(email, password);
        if (success) {
            if (email === "admin@tattva.ai") {
                navigate("/admin");
            } else {
                navigate("/dashboard");
            }
        } else {
            setError("Invalid credentials. Use admin@tattva.ai / admin123 for Admin access.");
        }
    };

    const handleGoogleLogin = async () => {
        await googleLogin();
        navigate("/dashboard");
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-black relative overflow-hidden">
            {/* Background Decorative Elements */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-900/20 blur-[120px] rounded-full"></div>

            <div className="w-full max-w-md p-8 relative z-10">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-600/10 border border-blue-600/20 mb-4">
                        <ShieldCheck className="w-8 h-8 text-blue-500" />
                    </div>
                    <h1 className="text-3xl font-bold text-white tracking-tight">Tattva-AI</h1>
                    <p className="text-neutral-400 mt-2">Unified Fact-Checking & Verification</p>
                </div>

                <div className="bg-neutral-900/50 backdrop-blur-xl border border-neutral-800 p-8 rounded-3xl shadow-2xl">
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="block text-sm font-medium text-neutral-300 mb-2">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full bg-neutral-800/50 border border-neutral-700 text-white pl-11 pr-4 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                                    placeholder="name@example.com"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-neutral-300 mb-2">Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full bg-neutral-800/50 border border-neutral-700 text-white pl-11 pr-4 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        {error && (
                            <div className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/20 text-red-500 text-sm rounded-xl">
                                <AlertCircle className="w-4 h-4" />
                                <span>{error}</span>
                            </div>
                        )}

                        <button
                            type="submit"
                            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 rounded-xl shadow-lg shadow-blue-600/20 transition-all transform active:scale-[0.98]"
                        >
                            Sign In
                        </button>
                    </form>

                    <div className="relative my-8">
                        <div className="absolute inset-0 flex items-center">
                            <div className="w-full border-t border-neutral-800"></div>
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                            <span className="bg-neutral-900 px-2 text-neutral-500 uppercase tracking-widest">Or continue with</span>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <button
                            onClick={handleGoogleLogin}
                            className="flex items-center justify-center gap-2 bg-neutral-800 hover:bg-neutral-700 text-white font-medium py-3 px-4 rounded-xl border border-neutral-700 transition-all"
                        >
                            <Chrome className="w-5 h-5 text-blue-400" />
                            Google
                        </button>
                        <button className="flex items-center justify-center gap-2 bg-neutral-800 hover:bg-neutral-700 text-white font-medium py-3 px-4 rounded-xl border border-neutral-700 transition-all">
                            <Github className="w-5 h-5" />
                            GitHub
                        </button>
                    </div>
                </div>

                <p className="text-center text-neutral-500 text-sm mt-8">
                    Admin Creds: <span className="text-neutral-300">admin@tattva.ai / admin123</span>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;
