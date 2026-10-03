"use client";

import { useCallback, useEffect, useState } from "react";

interface HealthCheck {
  healthy: boolean;
  model?: string | null;
  documents?: number | null;
  free_gb?: number | null;
}

interface HealthData {
  healthy: boolean;
  checks: Record<string, HealthCheck>;
}

interface HealthResponse {
  success: boolean;
  message?: string | null;
  data: HealthData;
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function HealthPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE_URL}/health`, {
        method: "GET",
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error(`Health API returned HTTP ${response.status}`);
      }

      const result: HealthResponse = await response.json();

      setHealth(result);
    } catch (err) {
      setHealth(null);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the backend.",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  return (
    <main className="min-h-screen bg-slate-100 p-6">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">
              System Health
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              Monitor AI Document Chat backend components
            </p>
          </div>

          <button
            type="button"
            onClick={checkHealth}
            disabled={loading}
            className="rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Checking..." : "Refresh"}
          </button>
        </div>

        {/* Overall Status */}
        <section className="mb-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">
                Overall Status
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Current backend availability
              </p>
            </div>

            {loading ? (
              <StatusBadge label="Checking..." />
            ) : error ? (
              <StatusBadge label="Unavailable" healthy={false} />
            ) : (
              <StatusBadge
                label={health?.data.healthy ? "Healthy" : "Degraded"}
                healthy={health?.data.healthy ?? false}
              />
            )}
          </div>
        </section>

        {/* Error */}
        {error && (
          <section className="mb-6 rounded-xl border border-red-200 bg-red-50 p-5">
            <h2 className="font-semibold text-red-800">
              Health Check Failed
            </h2>

            <p className="mt-1 text-sm text-red-700">{error}</p>

            <p className="mt-3 text-xs text-red-600">
              API: {API_BASE_URL}/health
            </p>
          </section>
        )}

        {/* Loading */}
        {loading && !health && !error && (
          <section className="rounded-xl border border-slate-200 bg-white p-8 text-center shadow-sm">
            <p className="text-sm text-slate-500">
              Checking system components...
            </p>
          </section>
        )}

        {/* Component Health */}
        {health?.data?.checks && (
          <section>
            <h2 className="mb-4 text-xl font-semibold text-slate-900">
              Component Health
            </h2>

            <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {Object.entries(health.data.checks).map(
                ([name, check]) => (
                  <HealthCard
                    key={name}
                    name={name}
                    check={check}
                  />
                ),
              )}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}

function HealthCard({
  name,
  check,
}: {
  name: string;
  check: HealthCheck;
}) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold capitalize text-slate-900">
          {name.replace(/_/g, " ")}
        </h3>

        <StatusBadge
          label={check.healthy ? "Healthy" : "Unhealthy"}
          healthy={check.healthy}
        />
      </div>

      {check.model && (
        <div className="mt-4">
          <p className="text-xs uppercase tracking-wide text-slate-400">
            Model
          </p>

          <p className="mt-1 text-sm font-medium text-slate-700">
            {check.model}
          </p>
        </div>
      )}

      {check.documents !== null &&
        check.documents !== undefined && (
          <div className="mt-4">
            <p className="text-xs uppercase tracking-wide text-slate-400">
              Documents
            </p>

            <p className="mt-1 text-2xl font-bold text-slate-900">
              {check.documents.toLocaleString()}
            </p>
          </div>
        )}

      {check.free_gb !== null &&
        check.free_gb !== undefined && (
          <div className="mt-4">
            <p className="text-xs uppercase tracking-wide text-slate-400">
              Free Disk
            </p>

            <p className="mt-1 text-sm font-medium text-slate-700">
              {check.free_gb} GB
            </p>
          </div>
        )}
    </article>
  );
}

function StatusBadge({
  label,
  healthy = true,
}: {
  label: string;
  healthy?: boolean;
}) {
  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${
        healthy
          ? "bg-emerald-100 text-emerald-700"
          : "bg-red-100 text-red-700"
      }`}
    >
      <span
        className={`h-2 w-2 rounded-full ${
          healthy ? "bg-emerald-500" : "bg-red-500"
        }`}
      />

      {label}
    </span>
  );
}