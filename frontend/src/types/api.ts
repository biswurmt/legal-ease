// Types that match backend models and API responses

export type MessageRole = "A" | "B" | "user" | "assistant" | "system"

export interface CaseData {
  id: number
  name: string
  party_a: string | null
  party_b: string | null
  context: string | null
  summary: string | null
  last_modified: string
}

export interface SimulationData {
  id: number
  headline: string
  brief: string
  created_at: string
  case_id: number
}

export interface MessageData {
  id: number
  content: string
  role: MessageRole
  selected: boolean
  simulation_id: number
  parent_id: number | null
}

export interface BookmarkData {
  id: number
  simulation_id: number
  message_id: number
  name: string
}

export interface DocumentData {
  id: number
  file_name: string
  file_data: ArrayBuffer
  case_id: number
}

// API Response types
export interface AudioResponse {
  message: string
  audio_data?: ArrayBuffer
}

export interface TranscriptionResponse {
  message: string
}

export interface CaseWithSimulationsResponse {
  id: number
  name: string
  summary: string
  background: {
    party_a: string
    party_b: string
    key_issues: string
    general_notes: string
  }
  simulations: Array<{
    id: number
    headline: string
    brief: string
    created_at: string
    node_count: number
  }>
}

export interface CaseWithTreeCountResponse {
  id: number
  name: string
  party_a: string
  party_b: string
  context: string
  summary: string
  last_modified: string
  scenario_count: number
}
