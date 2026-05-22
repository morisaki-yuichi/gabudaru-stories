#!/usr/bin/env python3
"""Generate audio for Another Stories with random narrator selection.

Voice pool: en-US, en-GB, en-CA adult voices.
Voice is seeded by date so assignment is reproducible per story.

Usage:
  python generate_another_audio.py          # January (default)
  python generate_another_audio.py 01 02    # specific months
  python generate_another_audio.py all      # all months
"""

import asyncio
import random
import sys
from pathlib import Path

import edge_tts

VOICES = [
    # en-US Female
    "en-US-AvaNeural", "en-US-AriaNeural", "en-US-EmmaNeural",
    "en-US-AvaMultilingualNeural", "en-US-EmmaMultilingualNeural",
    "en-US-JennyNeural", "en-US-MichelleNeural", "en-US-AnaNeural",
    # en-US Male
    "en-US-AndrewNeural", "en-US-BrianNeural",
    "en-US-AndrewMultilingualNeural", "en-US-BrianMultilingualNeural",
    "en-US-ChristopherNeural", "en-US-EricNeural",
    "en-US-GuyNeural", "en-US-RogerNeural", "en-US-SteffanNeural",
    # en-GB Female
    "en-GB-LibbyNeural", "en-GB-MaisieNeural", "en-GB-SoniaNeural",
    # en-GB Male
    "en-GB-RyanNeural", "en-GB-ThomasNeural",
    # en-CA Female
    "en-CA-ClaraNeural",
    # en-CA Male
    "en-CA-LiamNeural",
]

RATE = "-10%"
PITCH = "-2Hz"


def pick_voice(date: str) -> str:
    return random.Random(date).choice(VOICES)


async def generate_month(prefix: str, stories, out_dir: Path) -> None:
    month_stories = [s for s in stories if s["date"].startswith(prefix)]
    print(f"\n{prefix}: {len(month_stories)} stories")
    for s in month_stories:
        date = s["date"]
        voice = pick_voice(date)
        out = out_dir / f"{date}.mp3"
        communicate = edge_tts.Communicate(s["text"], voice, rate=RATE, pitch=PITCH)
        await communicate.save(str(out))
        size = out.stat().st_size // 1024
        print(f"  {date}  {voice.split('-')[2]:<28s}  {size} KB")


async def main() -> None:
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    from another_stories_data import STORIES

    args = sys.argv[1:]
    if not args:
        months = ["01"]
    elif args == ["all"]:
        months = [f"{m:02d}" for m in range(1, 13)]
    else:
        months = args

    out_dir = scripts_dir.parent / "audio" / "another-stories"
    out_dir.mkdir(parents=True, exist_ok=True)

    for m in months:
        await generate_month(m, STORIES, out_dir)

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
