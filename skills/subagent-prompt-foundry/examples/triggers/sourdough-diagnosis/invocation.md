# Invocation

```
/subagent-prompt-foundry Turn this into a reusable subagent prompt: "Look at this photo of my sourdough and tell me what went wrong." I want my baking assistant agent to delegate crumb analysis to a specialist subagent.
```

## Routing decision

**ACTIVATE** — the user wants to generalize a one-off prompt into a reusable subagent prompt; a baking assistant parent agent delegates visual crumb diagnosis. All routing-checklist.md criteria pass:

1. The output should be a reusable system prompt ✓
2. The prompt defines a custom subagent (sourdough crumb diagnosis specialist) ✓
3. Direct task execution is not the goal ✓
4. A meta-agent prompt is not the goal ✓

## Research performed

- [Pauline Manor — Underproofed vs. Overproofed](https://paulinemanor.com/how-to-tell-if-your-sourdough-is-underproofed-or-overproofed/) — underproofed: tight/gummy crumb, random large holes, side splits, fast poke-test springback; overproofed: flat loaf, collapsed alveoli, no oven spring, no springback
- [The Sourdough Journey — Open Crumb FAQ](https://thesourdoughjourney.com/faq-open-crumb-and-crust/) — hydration guide: 65–70% closed crumb, 75–80% (Tartine style) open crumb; bulk fermentation as primary driver
- [Simply Bread — Reading Crumb Structure](https://www.simply-bread.co/post/how-to-read-your-crumb-like-a-seasoned-baker) — alveoli size/distribution, tunneling, compressed crumb, loaf shape as fermentation indicators
- [Cereal & Grains/King Arthur Scoring Rubric PDF](https://www.cerealsgrains.org/publications/plexus/cfw/pastissues/2018/protectedpdfs/CFW-63-2-0074.pdf) — professional evaluation: aspect (lift/spring), crust color, crumb texture, flavor/aroma, sound/touch
- Instagram diagnostic guide — Scenario mapping: flat dough + dense bake = under-fermentation; flat dough + light bake = over-fermentation; flat dough + good oven spring = tension failure
