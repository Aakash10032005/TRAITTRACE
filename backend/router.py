import sys
from pathlib import Path

# Add project root to sys.path to allow absolute imports of the 'backend' package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import groq

from backend.config import settings
from backend.graph_engine import TraitGraphManager

logger = logging.getLogger("trait-trace")
router = APIRouter()
graph_manager = TraitGraphManager()

# Map common interaction values to categories for semantic correctness in graph mapping
VALUE_CATEGORIES = {
    # Aesthetic choices
    "Minimalist": "aesthetic",
    "Bold & Vibrant": "aesthetic",
    # Lifestyle choices
    "Eco-Friendly": "lifestyle",
    "Luxe & Premium": "lifestyle",
    # Pricing tier selections
    "Budget": "pricing",
    "Standard": "pricing",
    "Premium": "pricing",
    # Hobbies/Interests
    "Active Outdoor": "hobby",
    "Tech Enthusiast": "hobby",
}

DEFAULT_PERSONA = {
    "persona": "Curious Explorer",
    "hero_title": "Tailored Just For You",
    "hero_subtitle": "Discover experiences crafted to align with your personal traits.",
    "recommended_product_id": "prod_classic_standard"
}

class InteractionRequest(BaseModel):
    session_id: str = Field(..., description="Unique ephemeral UUID for the current visitor session")
    interaction_type: str = Field(..., description="The action taken (e.g. swipe, select)")
    value: str = Field(..., description="The specific choice or trait value selected")

class InteractionResponse(BaseModel):
    session_id: str
    persona: str
    hero_title: str
    hero_subtitle: str
    recommended_product_id: str
    graph_snapshot: dict

@router.post("/interact", response_model=InteractionResponse)
async def process_interaction(request: InteractionRequest):
    # 1. Determine category for this trait
    category = VALUE_CATEGORIES.get(request.value, "preference")

    # 2. Add trait to graph
    try:
        graph_manager.add_session_trait(
            session_id=request.session_id,
            trait_name=request.value,
            relationship_type=request.interaction_type,
            category=category
        )
    except Exception as e:
        logger.error(f"Failed to update knowledge graph: {e}")
        # Graph updates should not crash the request, we continue

    # 3. Retrieve formatted graph paths
    graph_summary = graph_manager.get_session_path_as_string(request.session_id)

    # 4. Invoke LLM via Groq API within a robust, wide try-except block
    persona_data = DEFAULT_PERSONA.copy()

    try:
        # Ensure key is configured before making API requests
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY in ("placeholder_key", "gsk_your_free_groq_api_key_goes_here"):
            raise ValueError("GROQ_API_KEY is unset or is a placeholder.")

        # Construct Groq client
        client = groq.Groq(api_key=settings.GROQ_API_KEY)
        
        # Build strict prompt enforcing raw JSON response
        system_instruction = "You are an elite Epsilon MarTech Core Brain."
        prompt = (
            f"Analyze this active consumer's interaction graph paths: {graph_summary}. "
            "Return a valid, minified, unescaped JSON object matching this exact schema: "
            '{ "persona": "String", "hero_title": "String", "hero_subtitle": "String", "recommended_product_id": "String" }. '
            "Do not wrap inside codeblocks. Do not include markdown formatting."
        )

        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.6,
            max_tokens=256
        )

        response_text = completion.choices[0].message.content.strip()

        # Defensive sanitization to strip any markdown code blocks (```json ... ```)
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()

        # Parse output JSON
        parsed_json = json.loads(response_text)
        
        # Validate schema completeness
        required_keys = ["persona", "hero_title", "hero_subtitle", "recommended_product_id"]
        if all(k in parsed_json for k in required_keys):
            persona_data = parsed_json
        else:
            logger.warning(f"Groq output missing schema keys: {parsed_json}. Using default.")
            
    except Exception as e:
        # Any API key failure, rate limits, connection errors, or JSON parsing failures are caught here
        logger.error(f"Groq API call or parsing failed: {e}. Falling back to default persona.")

    # 5. Extract values and return alongside graph snapshot
    return InteractionResponse(
        session_id=request.session_id,
        persona=persona_data.get("persona", DEFAULT_PERSONA["persona"]),
        hero_title=persona_data.get("hero_title", DEFAULT_PERSONA["hero_title"]),
        hero_subtitle=persona_data.get("hero_subtitle", DEFAULT_PERSONA["hero_subtitle"]),
        recommended_product_id=persona_data.get("recommended_product_id", DEFAULT_PERSONA["recommended_product_id"]),
        graph_snapshot=graph_manager.get_graph_snapshot()
    )
