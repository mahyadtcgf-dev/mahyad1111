import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "@/pages/auth/Login";
import AdminDashboard from "@/pages/admin/Dashboard";
import UserDashboard from "@/pages/user/Dashboard";
import Layout from "@/components/layout/Layout";

const ProtectedRoute = ({ children, role }: { children: React.ReactNode, role?: string }) => {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  if (!user.username) return <Navigate to="/login" replace />;
  if (role && user.role !== role && user.role !== "SUPER_ADMIN") {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route path="/admin" element={
          <ProtectedRoute role="ADMIN">
            <Layout role="admin"><AdminDashboard /></Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Layout role="user"><UserDashboard /></Layout>
          </ProtectedRoute>
        } />

        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
