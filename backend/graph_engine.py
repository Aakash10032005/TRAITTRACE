import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
import networkx as nx


class TraitGraphManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._init_graph()
        return cls._instance

    def _init_graph(self):
        self.G = nx.DiGraph()

    def add_session_trait(
        self,
        session_id: str,
        trait_name: str,
        relationship_type: str,
        category: str = None,
    ) -> None:
        if not self.G.has_node(session_id):
            self.G.add_node(session_id, type="user", created_at=time.time())

        if not self.G.has_node(trait_name):
            self.G.add_node(trait_name, type="trait", category=category or "uncategorized")
        elif category:
            self.G.nodes[trait_name]["category"] = category

        if self.G.has_edge(session_id, trait_name):
            self.G[session_id][trait_name]["weight"] += 1.0
            self.G[session_id][trait_name]["timestamp"] = time.time()
        else:
            self.G.add_edge(
                session_id,
                trait_name,
                weight=1.0,
                timestamp=time.time(),
                relationship=relationship_type,
            )

    def get_session_path_as_string(self, session_id: str) -> str:
        if not self.G.has_node(session_id):
            return "No interaction path found for this session."

        out_edges = self.G.out_edges(session_id, data=True)
        if not out_edges:
            return "Session has no connected traits."

        parts = []
        for _, trait, data in out_edges:
            category = self.G.nodes[trait].get("category", "uncategorized")
            weight = data.get("weight", 1.0)
            relationship = data.get("relationship", "chosen")
            parts.append(
                f"trait '{trait}' (category: {category}, interaction: {relationship}, intensity: {weight})"
            )

        return f"User {session_id} has paths: " + ", ".join(parts)

    def get_graph_snapshot(self) -> dict:
        nodes = [
            {
                "id": str(node),
                "type": self.G.nodes[node].get("type", "unknown"),
                "category": self.G.nodes[node].get("category", ""),
            }
            for node in self.G.nodes
        ]
        links = [
            {
                "source": str(u),
                "target": str(v),
                "weight": self.G[u][v].get("weight", 1.0),
                "relationship": self.G[u][v].get("relationship", ""),
            }
            for u, v in self.G.edges
        ]
        return {"nodes": nodes, "links": links}

    def clear(self) -> None:
        self.G.clear()
