#!/usr/bin/env python3
"""Generate another-stories/ — 365 daily bedtime stories about Gabu."""

from pathlib import Path
from another_stories_data import STORIES

OUT = Path(__file__).parent.parent / "another-stories"

MONTH_DAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
MONTH_SHORT = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

SEASON_GRADIENT = {
    "winter": "135deg, #2c5f8a, #7ab8d4",
    "spring": "135deg, #3a7a4a, #e8a8c0",
    "summer": "135deg, #c87820, #4a9850",
    "autumn": "135deg, #b85a20, #d4a030",
}

def season(month):
    if month in (12, 1, 2): return "winter"
    if month in (3, 4, 5): return "spring"
    if month in (6, 7, 8): return "summer"
    return "autumn"

def characters(month, day):
    chars = [("🐢", "Gabu")]
    if (month, day) >= (4, 10):  chars.append(("🐢", "Daru"))
    if (month, day) >= (7, 8):   chars.append(("🐕", "Dango"))
    if (month, day) >= (10, 15): chars.append(("🐱", "Suke-san"))
    return chars

def day_number(month, day):
    return sum(MONTH_DAYS[1:month]) + day

def adjacent(month, day):
    prev = next_ = None
    if day > 1:
        prev = (month, day - 1)
    elif month > 1:
        prev = (month - 1, MONTH_DAYS[month - 1])
    if day < MONTH_DAYS[month]:
        next_ = (month, day + 1)
    elif month < 12:
        next_ = (month + 1, 1)
    return prev, next_

def paras_html(text):
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    return "\n".join(f"      <p>{b}</p>" for b in blocks)

PLAYER_TEMPLATE = """\
    <div class="player">
      <button class="play-btn" id="playBtn" aria-label="Play">▶</button>
      <div class="play-wrap" id="playWrap">
        <div class="play-bar" id="playBar"></div>
      </div>
      <span class="play-time" id="playTime">0:00</span>
      <audio id="playAudio" src="../audio/another-stories/__DATE__.mp3" preload="none"></audio>
    </div>
    <script>
    (function() {
      var audio = document.getElementById('playAudio');
      var btn = document.getElementById('playBtn');
      var bar = document.getElementById('playBar');
      var wrap = document.getElementById('playWrap');
      var lbl = document.getElementById('playTime');
      function fmt(s) {
        var m = Math.floor(s / 60), sec = Math.floor(s % 60);
        return m + ':' + (sec < 10 ? '0' : '') + sec;
      }
      btn.addEventListener('click', function() {
        if (audio.paused) { audio.play(); btn.textContent = '⏸'; }
        else { audio.pause(); btn.textContent = '▶'; }
      });
      audio.addEventListener('timeupdate', function() {
        if (audio.duration) {
          bar.style.width = (audio.currentTime / audio.duration * 100) + '%';
          lbl.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration);
        }
      });
      audio.addEventListener('ended', function() {
        btn.textContent = '▶';
        bar.style.width = '0';
        lbl.textContent = '0:00 / ' + fmt(audio.duration);
      });
      wrap.addEventListener('click', function(e) {
        if (!audio.duration) return;
        var r = wrap.getBoundingClientRect();
        audio.currentTime = ((e.clientX - r.left) / r.width) * audio.duration;
      });
    })();
    </script>"""


TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — {mname} {day}</title>
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Nunito', sans-serif; background: #fdf6e3; color: #3d2b1f; min-height: 100vh; padding: 1.5rem 1rem 4rem; }}
    .book {{ max-width: 620px; margin: 0 auto; background: #fffdf5; border-radius: 24px; box-shadow: 0 8px 40px rgba(100,60,20,0.12); overflow: hidden; }}
    .cover {{ background: linear-gradient({gradient}); padding: 2.5rem 2rem 1.75rem; text-align: center; }}
    .date-label {{ font-size: 0.78rem; font-weight: 700; color: rgba(255,255,255,0.85); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }}
    .cover h1 {{ font-size: 1.5rem; font-weight: 800; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,0.2); line-height: 1.3; margin-bottom: 0.75rem; }}
    .friends {{ display: flex; gap: 0.4rem; justify-content: center; flex-wrap: wrap; }}
    .fbadge {{ background: rgba(255,255,255,0.22); border-radius: 20px; padding: 0.2rem 0.65rem; font-size: 0.82rem; color: #fff; font-weight: 700; }}
    .story {{ padding: 2rem 2.25rem 2.5rem; }}
    .story p {{ font-size: 1.125rem; line-height: 2.1; margin-bottom: 0.9rem; }}
    .story p:last-child {{ margin-bottom: 0; }}
    .player {{ display: flex; align-items: center; gap: 0.75rem; padding: 1rem 2.25rem; border-bottom: 2px dashed #e8d0b8; }}
    .play-btn {{ width: 2.25rem; height: 2.25rem; border-radius: 50%; border: none; background: #9a7a5a; color: #fff; font-size: 0.85rem; cursor: pointer; flex-shrink: 0; }}
    .play-btn:hover {{ background: #7a5a3a; }}
    .play-wrap {{ flex: 1; height: 5px; background: #e8d0b8; border-radius: 3px; cursor: pointer; }}
    .play-bar {{ height: 100%; background: #9a7a5a; border-radius: 3px; width: 0; }}
    .play-time {{ font-size: 0.72rem; font-weight: 700; color: #b8987a; white-space: nowrap; }}
    .nav {{ display: flex; justify-content: space-between; align-items: center; padding: 0.85rem 2rem; border-top: 2px dashed #e8d0b8; gap: 0.5rem; }}
    .nav a {{ font-size: 0.88rem; font-weight: 700; color: #9a7a5a; text-decoration: none; padding: 0.35rem 0.75rem; border-radius: 8px; background: #f5ede0; white-space: nowrap; }}
    .nav a:hover {{ background: #e8d0b8; }}
    .dc {{ font-size: 0.78rem; color: #b8987a; font-weight: 700; white-space: nowrap; }}
    @media (max-width: 480px) {{ .cover h1 {{ font-size: 1.25rem; }} .story p {{ font-size: 1rem; }} .story {{ padding: 1.5rem 1.5rem 2rem; }} .nav {{ padding: 0.75rem 1.25rem; }} .player {{ padding: 0.85rem 1.5rem; }} }}
  </style>
</head>
<body>
  <article class="book">
    <header class="cover">
      <div class="date-label">{mname} {day}</div>
      <h1>{title}</h1>
      <div class="friends">{badges}</div>
    </header>
{player}
    <section class="story">
{paragraphs}
    </section>
    <nav class="nav">
      {prev_link}
      <span class="dc">Day {daynum} / 365</span>
      {next_link}
    </nav>
  </article>
</body>
</html>"""


AUDIO_DIR = Path(__file__).parent.parent / "audio" / "another-stories"

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Another Stories</title>
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Nunito', sans-serif; background: #fdf6e3; color: #3d2b1f; min-height: 100vh; padding: 1.5rem 1rem 4rem; }
    .page { max-width: 860px; margin: 0 auto; }
    .hd { text-align: center; padding: 2rem 1rem 2.5rem; }
    .hd h1 { font-size: 1.5rem; font-weight: 800; color: #5a3a1a; margin-bottom: 0.3rem; }
    .hd p { font-size: 0.88rem; color: #9a7a5a; }
    .back { display: inline-block; margin-bottom: 1.5rem; font-size: 0.82rem; font-weight: 700; color: #9a7a5a; text-decoration: none; padding: 0.3rem 0.75rem; background: #f5ede0; border-radius: 8px; }
    .back:hover { background: #e8d0b8; }
    .months { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
    .mc { background: #fffdf5; border-radius: 14px; box-shadow: 0 3px 14px rgba(100,60,20,0.1); overflow: hidden; }
    .mh { padding: 0.55rem 0.75rem; font-size: 0.82rem; font-weight: 800; color: #fff; letter-spacing: 0.04em; }
    .days { display: grid; grid-template-columns: repeat(7, 1fr); padding: 0.6rem 0.5rem 0.7rem; gap: 1px; }
    .days a { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 2rem; font-size: 0.8rem; font-weight: 700; color: #7a5a3a; text-decoration: none; border-radius: 5px; }
    .days a:hover { background: #f5ede0; }
    .days a.au::after { content: ''; width: 4px; height: 4px; background: #9a7a5a; border-radius: 50%; margin-top: 1px; }
    .days .em { height: 2rem; }
    @media (max-width: 640px) { .months { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 360px) { .months { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="page">
    <a class="back" href="../index.html">← Home</a>
    <div class="hd">
      <h1>Another Stories</h1>
      <p>365 bedtime stories — one for each night of the year</p>
    </div>
    <div class="months">
__MONTHS__
    </div>
  </div>
</body>
</html>"""


def generate_index():
    audio_dates = {p.stem for p in AUDIO_DIR.glob("??-??.mp3")}
    blocks = []
    for month in range(1, 13):
        grad = SEASON_GRADIENT[season(month)]
        days = MONTH_DAYS[month]
        cells = []
        for day in range(1, days + 1):
            date = f"{month:02d}-{day:02d}"
            cls = " au" if date in audio_dates else ""
            cells.append(f'<a href="{date}.html" class="{cls.strip()}">{day}</a>' if cls
                         else f'<a href="{date}.html">{day}</a>')
        pad = (7 - days % 7) % 7
        cells.extend(['<div class="em"></div>'] * pad)
        blocks.append(
            f'      <div class="mc">\n'
            f'        <div class="mh" style="background:linear-gradient({grad})">{MONTH_NAMES[month]}</div>\n'
            f'        <div class="days">{"".join(cells)}</div>\n'
            f'      </div>'
        )
    html = INDEX_TEMPLATE.replace("__MONTHS__", "\n".join(blocks))
    (OUT / "index.html").write_text(html, encoding="utf-8")
    print("  wrote: another-stories/index.html")


def render(story, has_audio=False):
    mm, dd = story["date"].split("-")
    month, day = int(mm), int(dd)
    date = story["date"]
    chars = characters(month, day)
    grad = SEASON_GRADIENT[season(month)]
    badges = "".join(f'<span class="fbadge">{e} {n}</span>' for e, n in chars)
    daynum = day_number(month, day)
    prev, next_ = adjacent(month, day)
    def link(md, label):
        if md is None:
            return f'<span style="visibility:hidden">{label}</span>'
        m, d = md
        return f'<a href="{m:02d}-{d:02d}.html">{label}</a>'
    prev_link = link(prev, "← Previous")
    next_link = link(next_, "Next →")
    player = PLAYER_TEMPLATE.replace("__DATE__", date) if has_audio else ""
    return TEMPLATE.format(
        title=story["title"],
        mname=MONTH_NAMES[month],
        day=day,
        gradient=grad,
        badges=badges,
        paragraphs=paras_html(story["text"]),
        daynum=daynum,
        prev_link=prev_link,
        next_link=next_link,
        player=player,
    )


def generate():
    OUT.mkdir(exist_ok=True)
    for story in STORIES:
        date = story["date"]
        has_audio = (AUDIO_DIR / f"{date}.mp3").exists()
        html = render(story, has_audio=has_audio)
        fname = OUT / f"{date}.html"
        fname.write_text(html, encoding="utf-8")
        flag = " [audio]" if has_audio else ""
        print(f"  wrote: another-stories/{date}.html{flag}")
    generate_index()
    print(f"\nDone. {len(STORIES)} files written.")


if __name__ == "__main__":
    generate()
