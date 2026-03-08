import { Link } from "react-router";
import { Button } from "../../shared/components/ui/button";
import PrismaticBurst from "../../shared/components/ui/PrismaticBurst";
import { Megaphone, Zap, Languages, Users } from "lucide-react";

export default function LandingPage() {
    return (
        <div className="relative min-h-screen bg-[oklch(0.145_0_0)] text-white overflow-hidden selection:bg-[oklch(0.488_0.243_264.376)]/30">
            {/* Dynamic Background */}
            <div className="absolute inset-0 z-0 opacity-40">
                <PrismaticBurst
                    intensity={1.5}
                    speed={0.2}
                    animationType="rotate3d"
                    distort={0.3}
                    rayCount={8}
                />
            </div>

            {/* Navigation */}
            <nav className="relative z-10 flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
                <div className="flex items-center gap-3 group">
                    <Link to="/" className="flex items-center gap-3">
                        <div className="w-12 h-12 flex items-center justify-center group-hover:scale-110 transition-transform overflow-hidden">
                            <img src="/logo.png" alt="Tattva-AI Logo" className="w-full h-full object-contain" />
                        </div>
                        <span className="text-2xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">
                            Tattva-AI
                        </span>
                    </Link>
                </div>

                <div className="flex items-center gap-4">
                    <Link to="/login">
                        <Button className="bg-[oklch(0.488_0.243_264.376)] hover:bg-[oklch(0.488_0.243_264.376)]/90 text-white shadow-lg shadow-blue-500/25 px-8 h-11 rounded-xl font-medium">
                            Login / Sign Up
                        </Button>
                    </Link>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="relative z-10 max-w-7xl mx-auto px-8 pt-20 pb-32 flex flex-col items-center text-center">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-8 animate-fade-in">
                    <Zap size={14} />
                    <span>Advanced AI Fact-Checking</span>
                </div>

                <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight mb-8 leading-tight">
                    Uncovering <span className="text-transparent bg-clip-text bg-gradient-to-r from-[oklch(0.488_0.243_264.376)] to-[oklch(0.645_0.246_16.439)]">Truth</span> in <br />
                    the Age of Information
                </h1>

                <p className="text-xl text-neutral-400 max-w-2xl mb-12 leading-relaxed">
                    Tattva-AI leverages cutting-edge misinformation detection to secure digital platforms.
                    Real-time analysis, linguistic criteria, and cross-platform verification.
                </p>

                <div className="flex flex-col sm:flex-row items-center gap-4">
                    <Link to="/login">
                        <Button size="lg" className="h-14 px-10 text-lg bg-[oklch(0.488_0.243_264.376)] hover:bg-[oklch(0.488_0.243_264.376)]/90 text-white shadow-xl shadow-blue-500/20 group">
                            Get Started Now
                            <Zap className="ml-2 group-hover:scale-125 transition-transform" size={18} />
                        </Button>
                    </Link>
                    <Button variant="outline" size="lg" className="h-14 px-10 text-lg border-white/10 text-white hover:bg-white/5 backdrop-blur-sm">
                        Watch Demo
                    </Button>
                </div>

                {/* Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-40 w-full">
                    <div className="p-8 rounded-2xl bg-white/[0.02] border border-white/[0.05] flex flex-col items-center group hover:bg-white/[0.04] transition-colors">
                        <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-400 mb-6 group-hover:scale-110 transition-transform">
                            <Zap size={24} />
                        </div>
                        <h3 className="text-xl font-bold mb-3">Real-time Analysis</h3>
                        <p className="text-neutral-500">
                            Detect misinformation as it spreads with our high-speed processing clusters.
                        </p>
                    </div>

                    <div className="p-8 rounded-2xl bg-white/[0.02] border border-white/[0.05] flex flex-col items-center group hover:bg-white/[0.04] transition-colors">
                        <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400 mb-6 group-hover:scale-110 transition-transform">
                            <Languages size={24} />
                        </div>
                        <h3 className="text-xl font-bold mb-3">Multilingual Support</h3>
                        <p className="text-neutral-500">
                            Breaking language barriers in fact-checking with support for 50+ languages.
                        </p>
                    </div>

                    <div className="p-8 rounded-2xl bg-white/[0.02] border border-white/[0.05] flex flex-col items-center group hover:bg-white/[0.04] transition-colors">
                        <div className="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center text-green-400 mb-6 group-hover:scale-110 transition-transform">
                            <Users size={24} />
                        </div>
                        <h3 className="text-xl font-bold mb-3">Partner Network</h3>
                        <p className="text-neutral-500">
                            Collaborative verification ecosystem with trusted news organizations.
                        </p>
                    </div>
                </div>
            </main>

            {/* Bottom Gradient Fade */}
            <div className="absolute bottom-0 left-0 right-0 h-96 bg-gradient-to-t from-[oklch(0.145_0_0)] to-transparent z-0 pointer-events-none" />

            <footer className="relative z-10 py-12 border-t border-white/[0.05] mt-20 text-center text-neutral-500 text-sm">
                <p>© 2026 Tattva-AI. All rights reserved.</p>
            </footer>
        </div>
    );
}
