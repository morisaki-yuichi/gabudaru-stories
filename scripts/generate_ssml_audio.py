#!/usr/bin/env python3
"""Generate prosody-tuned audio for Another Stories using edge-tts.

The free Edge TTS endpoint supports rate/pitch/volume via the <prosody>
element but does not support <break>, <p>, or mstts:express-as extensions.
We generate the best available quality using voice selection + prosody params.
"""

import asyncio
import sys
from pathlib import Path

import edge_tts

# Voice and prosody settings tuned for bedtime narration:
#   AriaNeural  – warm, clear US narrator
#   rate -10%   – deliberate, unhurried pace
#   pitch -2Hz  – slightly lower, calmer tone
VOICE = "en-US-AriaNeural"
RATE = "-10%"
PITCH = "-2Hz"


async def generate(text: str, voice: str, rate: str, pitch: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(str(out_path))
    size_kb = out_path.stat().st_size // 1024
    print(f"  saved: {out_path.name} ({size_kb} KB)")


async def main() -> None:
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    from another_stories_data import STORIES

    story = next(s for s in STORIES if s["date"] == "01-01")
    text = story["text"]

    out_dir = scripts_dir.parent / "audio" / "another-stories"

    print(f"Voice: {VOICE}  rate: {RATE}  pitch: {PITCH}")
    print(f"Text length: {len(text)} chars")

    await generate(text, VOICE, RATE, PITCH, out_dir / "01-01-improved.mp3")
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
