# Invocation

```
/subagent-prompt-foundry Create a reusable system prompt for a D&D dungeon master subagent that generates balanced encounter tables, loot drops, and NPC dialogue trees for a parent campaign manager agent.
```

## Routing decision

**ACTIVATE** — the user explicitly requests a reusable system prompt for a subagent that a parent campaign manager agent delegates to. All routing-checklist.md criteria pass:

1. The output should be a reusable system prompt ✓
2. The prompt defines a custom subagent (D&D dungeon master content generator) ✓
3. Direct task execution is not the goal ✓
4. A meta-agent prompt is not the goal ✓

## Research performed

- [D&D Beyond — Building Combat Encounters](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/building-combat-encounters) — XP Thresholds by Character Level table (Easy/Medium/Hard/Deadly), adjusted XP multipliers
- [DMG Loot Tables](https://dungeonmastertools.github.io/treasure.html) — Magic Item Tables A–I by CR tier, coin/gem/art object distributions
- [2024 DMG Encounter Math vs 2014](https://www.enworld.org/threads/new-dmg-encounter-building-math-vs-2014.707688/) — XP multiplier removed in 2024, difficulty threshold changes at levels 8+
- [ChallengeRated.com](https://www.challengerated.com/info) — XP budget calculations, party XP threshold methodology
