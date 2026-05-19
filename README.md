# Gabu & Daru Stories

A series of original read-aloud stories for young English learners (CEFR A1 level).

## Stories

| # | Title | Characters |
|---|-------|------------|
| Part 1 | The Great Tomato Adventure | Gabu, Daru |
| Part 2 | The Secret Garden and the Big Storm | Gabu, Daru |
| Part 3 | The Giant in the Garden and the Missing Stone | Gabu, Daru, Dango |
| Part 4 | Suke-san Does Not Need Anyone | Gabu, Daru, Dango, Suke-san |

**Characters**
- **Gabu** — A tortoise. Big and slow, but careful and observant.
- **Daru** — A tortoise. Quick and curious, always looking for something new.
- **Dango** — A Corgi boy with a fluffy tail. Grew from an energetic puppy into a loyal garden guardian.
- **Suke-san** — A Shiba Inu puppy. Proud and independent, but slowly warming up to friendship.

## Site

Published on GitHub Pages: **https://morisaki-yuichi.github.io/gabudaru-stories/**

The site includes an audio player with 9 voice options (US English × 4, UK English × 5), generated using [edge-tts](https://github.com/rany2/edge-tts).

## Repository Structure

```
├── index.html          # Audio player page (GitHub Pages root)
├── stories/            # Story HTML pages
│   ├── part1.html
│   ├── part2.html
│   ├── part3.html
│   └── part4.html
├── audio/              # MP3 files organized by voice
│   ├── en-US-AvaNeural/
│   ├── en-US-AnaNeural/
│   ├── en-US-BrianNeural/
│   ├── en-US-JennyNeural/
│   ├── en-GB-LibbyNeural/
│   ├── en-GB-MaisieNeural/
│   ├── en-GB-RyanNeural/
│   ├── en-GB-SoniaNeural/
│   └── en-GB-ThomasNeural/
├── src/                # Markdown source files
└── scripts/
    └── generate_audio.py   # Audio generation script (requires edge-tts)
```

## Generating Audio

```bash
uv run --with edge-tts python3 scripts/generate_audio.py
```

## License

© 2026 morisaki-yuichi. All rights reserved.

The story texts and HTML content in this repository are original works and may not be reproduced, distributed, or used without permission.

Audio files are generated using Microsoft's Neural TTS voices via [edge-tts](https://github.com/rany2/edge-tts) and are subject to [Microsoft's Terms of Service](https://www.microsoft.com/en-us/servicesagreement).
