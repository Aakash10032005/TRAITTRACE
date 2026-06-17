import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import logging
from fastapi import APIRouter
from pydantic import BaseModel, Field
import groq

from backend.config import settings
from backend.graph_engine import TraitGraphManager

logger = logging.getLogger("trait-trace")
router = APIRouter()
graph_manager = TraitGraphManager()

VALUE_CATEGORIES = {
    "Minimalist": "aesthetic",
    "Bold & Vibrant": "aesthetic",
    "Eco-Friendly": "lifestyle",
    "Luxe & Premium": "lifestyle",
    "Budget": "pricing",
    "Standard": "pricing",
    "Premium": "pricing",
    "Active Outdoor": "hobby",
    "Tech Enthusiast": "hobby",
}

DEFAULT_PERSONA = {
    "persona": "Curious Explorer",
    "hero_title": "Tailored Just For You",
    "hero_subtitle": "Discover experiences crafted to align with your personal traits.",
    "recommended_product_id": "prod_classic_standard",
}


class InteractionRequest(BaseModel):
    session_id: str = Field(..., description="Ephemeral UUID for the current visitor session")
    interaction_type: str = Field(..., description="Action taken, e.g. swipe")
    value: str = Field(..., description="Trait value selected")


class InteractionResponse(BaseModel):
    session_id: str
    persona: str
    hero_title: str
    hero_subtitle: str
    recommended_product_id: str
    graph_snapshot: dict


@router.post("/interact", response_model=InteractionResponse)
async def process_interaction(request: InteractionRequest):
    category = VALUE_CATEGORIES.get(request.value, "preference")

    try:
        graph_manager.add_session_trait(
            session_id=request.session_id,
            trait_name=request.value,
            relationship_type=request.interaction_type,
            category=category,
        )
    except Exception as e:
        logger.error(f"Graph update failed: {e}")

    graph_summary = graph_manager.get_session_path_as_string(request.session_id)
    persona_data = DEFAULT_PERSONA.copy()

    try:
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY in (
            "placeholder_key",
            "gsk_your_free_groq_api_key_goes_here",
        ):
            raise ValueError("GROQ_API_KEY is not configured.")

        client = groq.Groq(api_key=settings.GROQ_API_KEY)

        prompt = (
            f"Analyze this consumer's interaction graph: {graph_summary}. "
            "Return a valid JSON object with this exact schema: "
            '{ "persona": "String", "hero_title": "String", "hero_subtitle": "String", "recommended_product_id": "String" }. '
            "No markdown, no codeblocks."
        )

        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a MarTech personalization engine."},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.6,
            max_tokens=256,
        )

        response_text = completion.choices[0].message.content.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        parsed = json.loads(response_text.strip())
        required = ["persona", "hero_title", "hero_subtitle", "recommended_product_id"]

        if all(k in parsed for k in required):
            persona_data = parsed
        else:
            logger.warning(f"Groq response missing keys: {parsed}")

    except Exception as e:
        logger.error(f"Groq inference failed: {e}. Using default persona.")

    return InteractionResponse(
        session_id=request.session_id,
        persona=persona_data.get("persona", DEFAULT_PERSONA["persona"]),
        hero_title=persona_data.get("hero_title", DEFAULT_PERSONA["hero_title"]),
        hero_subtitle=persona_data.get("hero_subtitle", DEFAULT_PERSONA["hero_subtitle"]),
        recommended_product_id=persona_data.get(
            "recommended_product_id", DEFAULT_PERSONA["recommended_product_id"]
        ),
        graph_snapshot=graph_manager.get_graph_snapshot(),
    )
