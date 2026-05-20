import asyncio
import re
import sys
from pathlib import Path

import edge_tts

VOICES = [
    "en-US-AvaNeural",
    "en-US-AnaNeural",
    "en-US-BrianNeural",
    "en-US-JennyNeural",
    "en-GB-LibbyNeural",
    "en-GB-MaisieNeural",
    "en-GB-RyanNeural",
    "en-GB-SoniaNeural",
    "en-GB-ThomasNeural",
]

PARTS = [
    ("part1", "part1-v2.md"),
    ("part2", "part2-v2.md"),
    ("part3", "part3-v2.md"),
    ("part4", "part4-v1.md"),
    ("a2-part1", "a2-part1.md"),
    ("a2-part2", "a2-part2.md"),
    ("a2-part3", "a2-part3.md"),
    ("a2-part4", "a2-part4.md"),
    ("b1-part1", "b1-part1.md"),
    ("b1-part2", "b1-part2.md"),
    ("b1-part3", "b1-part3.md"),
    ("b1-part4", "b1-part4.md"),
    ("b2-part1", "b2-part1.md"),
    ("b2-part2", "b2-part2.md"),
    ("b2-part3", "b2-part3.md"),
    ("b2-part4", "b2-part4.md"),
]


def md_to_text(md: str) -> str:
    lines = []
    for line in md.splitlines():
        # skip headings
        if re.match(r"^#{1,6}\s", line):
            continue
        # skip scene breaks / dividers
        if re.match(r"^[-—*✦\s]+$", line):
            continue
        # strip inline bold/italic markers
        line = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", line)
        # strip italic using _
        line = re.sub(r"_(.+?)_", r"\1", line)
        lines.append(line)
    # collapse multiple blank lines into one
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


async def generate(part_name: str, text: str, voice: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))
    print(f"  saved: {out_path.relative_to(Path.cwd())}")


async def main() -> None:
    base = Path(__file__).parent.parent  # project root
    audio_dir = base / "audio"

    tasks = []
    for part_name, md_file in PARTS:
        md_path = base / "src" / md_file
        if not md_path.exists():
            print(f"[skip] {md_file} not found")
            continue
        text = md_to_text(md_path.read_text())
        for voice in VOICES:
            out_path = audio_dir / voice / f"{part_name}.mp3"
            tasks.append((part_name, text, voice, out_path))

    total = len(tasks)
    for i, (part_name, text, voice, out_path) in enumerate(tasks, 1):
        if out_path.exists():
            print(f"[{i}/{total}] skip (exists): {out_path.name} / {voice}")
            continue
        print(f"[{i}/{total}] generating {part_name} / {voice} ...")
        try:
            await generate(part_name, text, voice, out_path)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
