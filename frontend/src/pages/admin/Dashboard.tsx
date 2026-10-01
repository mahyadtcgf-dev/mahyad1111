import React from "react";
import { Users, Server, Activity, Key } from "lucide-react";

const StatCard = ({ title, value, icon: Icon, color }: any) => (
  <div className="p-6 bg-card border border-border rounded-xl space-y-2">
    <div className="flex items-center justify-between">
      <p className="text-sm font-medium text-muted-foreground">{title}</p>
      <Icon className={color} size={20} />
    </div>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

export default function AdminDashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <p className="text-muted-foreground">System overview and real-time statistics</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Users" value="1,284" icon={Users} color="text-blue-500" />
        <StatCard title="Active Nodes" value="12" icon={Server} color="text-green-500" />
        <StatCard title="Active Configs" value="4,512" icon={Key} color="text-purple-500" />
        <StatCard title="System Load" value="24%" icon={Activity} color="text-orange-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-6 bg-card border border-border rounded-xl">
          <h3 className="text-lg font-semibold mb-4">Node Health</h3>
          <div className="space-y-3">
            {["US-East-1", "EU-West-1", "Asia-South-1"].map(node => (
              <div key={node} className="flex items-center justify-between p-3 bg-input rounded-lg">
                <span>{node}</span>
                <span className="px-2 py-1 text-xs font-medium bg-green-500/20 text-green-500 rounded-full">Online</span>
              </div>
            ))}
          </div>
        </div>
        <div className="p-6 bg-card border border-border rounded-xl">
          <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
          <div className="text-sm text-muted-foreground space-y-2">
            <p>• Admin created user 'john_doe' - 2m ago</p>
            <p>• Node 'EU-West-1' reported health check - 5m ago</p>
            <p>• Config #4512 revoked - 12m ago</p>
          </div>
        </div>
      </div>
    </div>
  );
}
