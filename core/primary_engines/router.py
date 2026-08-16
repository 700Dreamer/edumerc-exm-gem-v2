# Primary Engines Dispatcher Router
# Inspects subject & level and routes to dedicated class-subject engines

from typing import AsyncGenerator
from core.primary_engines.p7.p7_english_engine import P7EnglishEngine
from core.primary_engines.p7.p7_science_engine import P7ScienceEngine
from core.primary_engines.p7.p7_sst_engine import P7SSTEngine
from core.primary_beta_engine import stream_primary_beta_paper

class PrimaryEngineRouter:
    @staticmethod
    async def stream_paper(subject: str, level: str, brand_name: str = "EDUMERC") -> AsyncGenerator[str, None]:
        subj_clean = (subject or "").strip().lower()
        lvl_clean = (level or "").strip().lower()

        # Send all primary traffic to the unified primary beta engine
        async for chunk in stream_primary_beta_paper(subject=subject, level=level, brand_name=brand_name):
            yield chunk
