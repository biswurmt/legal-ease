// Types for Scenario Explorer / Simulation Page
import type { MessageRole } from "./api"

// Frontend DialogueNode structure (existing in scenario.tsx)
export type Party = "A" | "B"

export interface DialogueNode {
  readonly id: string
  statement: string
  readonly party: Party
  children: DialogueNode[]
  readonly role?: MessageRole // Backend role (user, assistant, system)
  selected?: boolean // Track if this node is on the selected path
}

// Derive ResponseOption from DialogueNode instead of duplicating
export type ResponseOption = Pick<DialogueNode, "id" | "party"> & {
  text: string
}

// Backend TreeNode structure (from TreeResponse)
export interface BackendTreeNode {
  speaker: string
  line: string
  level: number
  reflects_personality: string
  responses: BackendTreeNode[]
}

// API response types
export interface TreeMessagesResponse {
  id: number
  role: MessageRole
  content: string
  selected: boolean
  children: TreeMessagesResponse[]
}

export interface TreeResponse {
  tree_id: number
  case_id: number
  simulation_goal: string
  scenarios_tree: BackendTreeNode
  error?: string
  raw_response?: string
}

export interface MessageCreateResponse {
  id: number
  content: string
  role: MessageRole
  selected: boolean
  simulation_id: number
  parent_id: number | null
}
