# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/sosissausage35-collab/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/sosissausage35-collab/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world news of Sunday 22 November 2026 — a
one-page newspaper front page, 35 stories across 6 regions, drawn in code
(`draw.py`, Pillow + DejaVu fonts), every story verified against wire
reporting of that day and named with its outlet:

- **COP31** — the climate talks in Antalya close in on a final deal: a new
  package with no mention of fossil fuels, delegations have until 03:00 GMT
  to object; electricity to 35% of final energy by 2035, 1bn tonnes of
  carbon capture, and the first COP admission that 1.5°C will be overshot.
- **IRAN–BAHRAIN** — IRGC missiles and drones hit two US Patriot radars at
  the Al-Riffa and Awali bases in Bahrain; an industrial site burns, no
  injuries; tankers are hit in the Strait of Hormuz.
- **UKRAINE** — Russia fires 186 drones in one night; Kyiv downs or jams
  161, strikes at 18 sites; a triple-tap on Kryvyi Rih kills a boy of 7
  and a paramedic; a Russian cargo ship burns in the Baltic.
- **Plus 32 more**: the ICJ's genocide ruling on Myanmar, 'El Chapo Isidro'
  captured in Mexico, Hong Kong votes, India's record 720/9 in Wellington,
  the AI sell-off, the EU–Indonesia trade deal, Gaza, Riyadh, and 22 more
  in the numbered list — with a world map, a stat strip and a date check
  that names what was left out as other days' news.

The program (`main.ts`, Node 22, standard library only) copies `entry.png`
to `/output/entry.png`. No network, no randomness — every run writes the same
bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=f4pc3mbd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
