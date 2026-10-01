import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/lib/api";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post("/auth/login", new FormData(e.currentTarget as any));
      // Note: FastAPI OAuth2 expects form-data
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      // Mocking user info for simplicity; in real app, call /auth/me
      localStorage.setItem("user", JSON.stringify({ username: form.username, role: "ADMIN" }));
      navigate("/dashboard");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md p-8 space-y-6 bg-card border border-border rounded-xl shadow-lg">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-primary">Welcome Back</h1>
          <p className="text-muted-foreground mt-2">Login to manage your VPN</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Username</label>
            <input 
              className="w-full px-3 py-2 bg-input border border-border rounded-md focus:ring-2 focus:ring-primary outline-none"
              value={form.username}
              onChange={(e) => setForm({...form, username: e.target.value})}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input 
              type="password"
              className="w-full px-3 py-2 bg-input border border-border rounded-md focus:ring-2 focus:ring-primary outline-none"
              value={form.password}
              onChange={(e) => setForm({...form, password: e.target.value})}
              required
            />
          </div>
          <button className="w-full py-2 bg-primary text-primary-foreground rounded-md font-semibold hover:opacity-90 transition-opacity">
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}
