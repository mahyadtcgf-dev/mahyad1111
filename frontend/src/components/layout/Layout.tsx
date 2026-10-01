import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { LayoutDashboard, Users, Server, Key, LogOut, User as UserIcon } from "lucide-react";

export default function Layout({ children, role }: { children: React.ReactNode, role: "admin" | "user" }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const menuItems = role === "admin" ? [
    { name: "Dashboard", icon: LayoutDashboard, path: "/admin" },
    { name: "Users", icon: Users, path: "/admin/users" },
    { name: "Nodes", icon: Server, path: "/admin/nodes" },
    { name: "Configs", icon: Key, path: "/admin/configs" },
  ] : [
    { name: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
    { name: "My Configs", icon: Key, path: "/dashboard/configs" },
    { name: "Profile", icon: UserIcon, path: "/dashboard/profile" },
  ];

  return (
    <div className="flex h-screen bg-background text-foreground">
      <aside className="w-64 border-r border-border bg-card flex flex-col">
        <div className="p-6 text-xl font-bold text-primary">VPN Panel</div>
        <nav className="flex-1 px-4 space-y-2">
          {menuItems.map((item) => (
            <Link 
              key={item.path} 
              to={item.path} 
              className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-accent hover:text-accent-foreground transition-colors"
            >
              <item.icon size={20} />
              <span>{item.name}</span>
            </Link>
          ))}
        </nav>
        <div className="p-4 border-t border-border">
          <button 
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-3 py-2 rounded-md text-destructive hover:bg-destructive/10 transition-colors"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto p-8">
        {children}
      </main>
    </div>
  );
}
