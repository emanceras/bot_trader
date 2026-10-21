export type Json = null | boolean | number | string | Json[] | { [key: string]: Json };
export type Role = 'admin' | 'researcher' | 'viewer' | 'agent';
export interface Session {
  principal: { id: string; role: Role };
  csrf: string;
}
export interface DocumentRecord {
  kind: string;
  id: string;
  version: number;
  body: Record<string, Json>;
  content_hash: string;
  created_at: string;
}
export type RunState = 'queued' | 'running' | 'succeeded' | 'failed' | 'interrupted' | 'cancelled';
export interface RunRecord {
  id: string;
  state: RunState;
  config: Record<string, Json>;
  config_hash: string;
  manifest: Record<string, Json>;
  manifest_hash: string;
  result: Record<string, Json> | null;
  error: Record<string, Json> | null;
  owner: string | null;
  created_by: string;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
}
export interface PlatformStatus {
  mode: 'technical';
  phase: string;
  account_currency: string;
  financial_experiments: number;
  live_execution: boolean;
  hypotheses: number;
  datasets: number;
  runs: number;
  counts_limit: number;
  worker: string;
}
export interface ModuleManifest {
  id: string;
  version: string;
  dependencies: string[];
  capabilities: string[];
  status: 'operational' | 'prepared' | 'planned';
  description: string;
}
export interface AuditRecord {
  id: string;
  actor: string;
  action: string;
  resource: string;
  outcome: string;
  details: Record<string, Json>;
  created_at: string;
}
export interface ChartSeries {
  dataset_id: string;
  dataset_version: number;
  synthetic: true;
  quote_currency: string;
  candles: { time: number; open: number; high: number; low: number; close: number }[];
  volume: { time: number; value: number }[];
  overlay: { time: number; value: number; available_at: string }[];
  transform: { name: string; version: string; window: number; input_content_hash: string };
  display_only: string;
}
