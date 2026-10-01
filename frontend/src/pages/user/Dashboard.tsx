import React from "react";
import { Shield, Globe, Download, RefreshCw } from "lucide-react";

export default function UserDashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Welcome, User</h1>
        <p className="text-muted-foreground">Your VPN connection and subscription status</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-card border border-border rounded-xl space-y-4">
          <div className="flex items-center gap-3 text-primary">
            <Shield size={24} />
            <h3 className="font-semibold">Subscription</h3>
          </div>
          <p className="text-2xl font-bold">Premium Plan</p>
          <p className="text-sm text-muted-foreground">Expires in 14 days</p>
        </div>

        <div className="p-6 bg-card border border-border rounded-xl space-y-4">
          <div className="flex items-center gap-3 text-primary">
            <Globe size={24} />
            <h3 className="font-semibold">Current Node</h3>
          </div>
          <p className="text-2xl font-bold">Singapore - SG-1</p>
          <p className="text-sm text-muted-foreground">Latency: 42ms</p>
        </div>

        <div className="p-6 bg-card border border-border rounded-xl space-y-4">
          <div className="flex items-center gap-3 text-primary">
            <Download size={24} />
            <h3 className="font-semibold">Traffic Used</h3>
          </div>
          <p className="text-2xl font-bold">42.5 GB / 100 GB</p>
          <div className="w-full bg-input h-2 rounded-full overflow-hidden">
            <div className="bg-primary h-full" style={{ width: "42.5%" }}></div>
          </div>
        </div>
      </div>

      <div className="p-6 bg-card border border-border rounded-xl">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold">Your Active Configuration</h3>
          <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:opacity-90 transition-opacity text-sm font-medium">
            <RefreshCw size={16} />
            Regenerate
          </button>
        </div>
        <div className="p-4 bg-input rounded-lg font-mono text-xs break-all border border-border">
          vless://uuid-here@sg-1.vpn-panel.com:443?security=tls&encryption=none&type=ws#PremiumUser
        </div>
      </div>
    </div>
  );
}
