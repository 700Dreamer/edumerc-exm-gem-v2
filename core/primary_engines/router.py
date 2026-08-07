# Primary Engines Dispatcher Router
# Inspects subject & level and routes to dedicated class-subject engines

from typing import AsyncGenerator
from core.primary_engines.p7.p7_english_engine import P7EnglishEngine
from core.primary_engines.p7.p7_science_engine import P7ScienceEngine
from core.primary_beta_engine import stream_primary_beta_paper

class PrimaryEngineRouter:
    @staticmethod
    async def stream_paper(subject: str, level: str, brand_name: str = "EDUMERC") -> AsyncGenerator[str, None]:
        subj_clean = (subject or "").strip().lower()
        lvl_clean = (level or "").strip().lower()

        is_p7 = any(x in lvl_clean for x in ["primary 7", "p.7", "p7"])
        is_english = "english" in subj_clean
        is_science = any(x in subj_clean for x in ["science", "integrated science"])

        if is_p7 and is_english:
            async for chunk in P7EnglishEngine.stream_paper(brand_name=brand_name):
                yield chunk
        elif is_p7 and is_science:
            async for chunk in P7ScienceEngine.stream_paper(brand_name=brand_name):
                yield chunk
        else:
            # Fallback to general primary beta engine
            async for chunk in stream_primary_beta_paper(subject=subject, level=level, brand_name=brand_name):
                yield chunk
