import { Search, Bell, Globe } from "lucide-react";
import { Input } from "../ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { useAuth } from "../../../features/auth/AuthContext";

interface TopNavProps {
  title: string;
}

export default function TopNav({ title }: TopNavProps) {
  const { user } = useAuth();

  return (
    <header className="h-16 bg-[oklch(0.205_0_0)] border-b border-[oklch(0.269_0_0)] flex items-center justify-between px-8">
      <div className="flex items-center gap-4 flex-1">
        <h2 className="text-xl text-white font-semibold">{title}</h2>
      </div>

      <div className="flex items-center gap-6">
        {/* Search Bar */}
        <div className="relative w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[oklch(0.708_0_0)]" size={18} />
          <Input
            type="text"
            placeholder="Search previous claims..."
            className="pl-10 bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white placeholder:text-[oklch(0.708_0_0)] h-10"
          />
        </div>

        {/* Language Selector */}
        <Select defaultValue="en">
          <SelectTrigger className="w-32 bg-[oklch(0.269_0_0)] border-[oklch(0.269_0_0)] text-white h-10">
            <Globe size={16} className="mr-2" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="en">English</SelectItem>
            <SelectItem value="ta">Tamil</SelectItem>
            <SelectItem value="hi">Hindi</SelectItem>
            <SelectItem value="te">Telugu</SelectItem>
            <SelectItem value="bn">Bengali</SelectItem>
          </SelectContent>
        </Select>

        {/* Notification Icon */}
        <button className="relative p-2 rounded-lg hover:bg-[oklch(0.269_0_0)] transition-colors">
          <Bell size={20} className="text-[oklch(0.708_0_0)]" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-[oklch(0.645_0.246_16.439)] rounded-full"></span>
        </button>

        {/* User Avatar */}
        <Avatar className="h-9 w-9 cursor-pointer border border-[oklch(0.269_0_0)]">
          {user?.photoURL && <AvatarImage src={user.photoURL} alt={user.name || "User"} />}
          <AvatarFallback className="bg-[oklch(0.488_0.243_264.376)] text-white text-sm">
            {user?.name ? user.name.substring(0, 2).toUpperCase() : "US"}
          </AvatarFallback>
        </Avatar>
      </div>
    </header>
  );
}
