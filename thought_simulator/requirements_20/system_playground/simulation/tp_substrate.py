type TP = {
  // Intake
  raw_text: string
  tokens: string[]
  normalized_text: string

  // Defects & correction
  defects: string[]
  corrections: string[]
  correction_score: number

  // OB-set / structural geometry
  struct_segments: string[]        // e.g. ["NP","VP","PP","NP"]
  struct_roles: string[]           // e.g. ["agent","action","relation","patient"]
  constraints: string[]            // e.g. ["agent-action","action-patient"]
  smoothed_geometry: boolean
  structural_vector_frozen: boolean

  // Routing
  routing_metadata: Record<string, any>
  routing_decision: string         // e.g. "semantic"
  routing_committed: boolean

  // Semantics & truth
  semantic_core: Record<string, any>
  truth_relation: string           // e.g. "descriptive", "hypothetical"

  // Meta / commit
  commit_flags: Record<string, boolean>
}
