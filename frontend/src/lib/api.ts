export interface InteractionRequest {
  session_id: string;
  interaction_type: string;
  value: string;
}

export interface GraphNode {
  id: string;
  type: string;       // "user" or "trait"
  category: string;   // "aesthetic", "lifestyle", "pricing", "hobby", "preference"
}

export interface GraphLink {
  source: string;
  target: string;
  weight: number;
  relationship: string;
}

export interface GraphSnapshot {
  nodes: GraphNode[];
  links: GraphLink[];
}

export interface InteractionResponse {
  session_id: string;
  persona: string;
  hero_title: string;
  hero_subtitle: string;
  recommended_product_id: string;
  graph_snapshot: GraphSnapshot;
}

/**
 * Sends a visitor choice to the FastAPI graph personalization endpoint
 */
export async function submitInteraction(payload: InteractionRequest): Promise<InteractionResponse> {
  const response = await fetch("http://localhost:8000/api/interact", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorMsg = await response.text();
    throw new Error(`Failed to submit interaction: ${response.status} - ${errorMsg || response.statusText}`);
  }

  return response.json();
}
