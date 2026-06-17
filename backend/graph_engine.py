import sys
from pathlib import Path

# Add project root to sys.path to allow absolute imports of the 'backend' package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
import networkx as nx

class TraitGraphManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TraitGraphManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_graph()
        return cls._instance

    def _init_graph(self):
        # Initialize the directed graph
        self.G = nx.DiGraph()

    def add_session_trait(self, session_id: str, trait_name: str, relationship_type: str, category: str = None) -> None:
        """
        Adds or updates a trait node connected to the user's session ID node.
        """
        # Ensure user node exists
        if not self.G.has_node(session_id):
            self.G.add_node(session_id, type="user", created_at=time.time())

        # Ensure trait node exists, and update its attributes if provided
        if not self.G.has_node(trait_name):
            self.G.add_node(trait_name, type="trait", category=category or "uncategorized")
        elif category:
            self.G.nodes[trait_name]["category"] = category

        # Add or update edge weight and timestamp
        if self.G.has_edge(session_id, trait_name):
            self.G[session_id][trait_name]["weight"] += 1.0
            self.G[session_id][trait_name]["timestamp"] = time.time()
        else:
            self.G.add_edge(
                session_id,
                trait_name,
                weight=1.0,
                timestamp=time.time(),
                relationship=relationship_type
            )

    def get_session_path_as_string(self, session_id: str) -> str:
        """
        Walks the graph from the root session_id, formats targets and weights into a clean summary.
        """
        if not self.G.has_node(session_id):
            return "No interaction path found for this session."

        out_edges = self.G.out_edges(session_id, data=True)
        if not out_edges:
            return "Session has no connected traits."

        traits_summaries = []
        for _, trait, data in out_edges:
            category = self.G.nodes[trait].get("category", "uncategorized")
            weight = data.get("weight", 1.0)
            relationship = data.get("relationship", "chosen")
            traits_summaries.append(
                f"trait '{trait}' (category: {category}, interaction: {relationship}, intensity: {weight})"
            )

        return f"User {session_id} has paths: " + ", ".join(traits_summaries)

    def get_graph_snapshot(self) -> dict:
        """
        Exports the current graph structured for react-force-graph-2d.
        """
        nodes = []
        for node in self.G.nodes:
            node_type = self.G.nodes[node].get("type", "unknown")
            category = self.G.nodes[node].get("category", "")
            nodes.append({
                "id": str(node),
                "type": node_type,
                "category": category
            })

        links = []
        for u, v in self.G.edges:
            edge_data = self.G[u][v]
            links.append({
                "source": str(u),
                "target": str(v),
                "weight": edge_data.get("weight", 1.0),
                "relationship": edge_data.get("relationship", "")
            })

        return {"nodes": nodes, "links": links}

    def clear(self) -> None:
        """
        Clears the graph state (mainly for unit tests).
        """
        self.G.clear()
