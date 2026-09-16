"use client";

import { useState } from "react";
import { useAuth } from "./use-auth";

interface Report {
  id: string;
  title: string;
  content: string;
  summary: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export function useReports() {
  const { token } = useAuth();
  const [reports, setReports] = useState<Report[]>([]);
  const [currentReport, setCurrentReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  // Load all compiled reports
  const loadReports = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/reports/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setReports(data);
      }
    } catch (err) {
      console.error("Failed to load reports list: ", err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch full details of a specific report
  const loadReportDetails = async (id: string) => {
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/v1/reports/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setCurrentReport(data);
      }
    } catch (err) {
      console.error(`Failed to load report ${id}: `, err);
    } finally {
      setLoading(false);
    }
  };

  // Dispatch background task to compile a new research report
  const generateReport = async (topic: string, sessionId?: string) => {
    if (!token) return;
    setGenerating(true);
    try {
      let url = `http://localhost:8000/api/v1/reports/generate?topic=${encodeURIComponent(topic)}`;
      if (sessionId) {
        url += `&session_id=${sessionId}`;
      }

      const res = await fetch(url, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        throw new Error("Server rejected background scheduling task.");
      }
      return true;
    } catch (err) {
      console.error("Failed to trigger report compilation: ", err);
      alert("Could not compile report: " + err);
      return false;
    } finally {
      setGenerating(false);
    }
  };

  return {
    reports,
    currentReport,
    loading,
    generating,
    loadReports,
    loadReportDetails,
    generateReport
  };
}
