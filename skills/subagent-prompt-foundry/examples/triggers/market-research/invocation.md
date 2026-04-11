# Invocation

```
/subagent-prompt-foundry Design a subagent prompt for competitive market research that my parent agent delegates to when evaluating whether to enter a new market.
```

## Routing decision

**ACTIVATE** — the user requests a subagent prompt design; the parent agent explicitly delegates market entry evaluation to a specialist subagent. All routing-checklist.md criteria pass:

1. The output should be a reusable system prompt ✓
2. The prompt defines a custom subagent (competitive market research specialist) ✓
3. Direct task execution is not the goal ✓
4. A meta-agent prompt is not the goal ✓

## Research performed

- [Porter's Five Forces](https://www.cascade.app/blog/porters-5-forces) — Threat of new entrants, bargaining power of buyers/suppliers, threat of substitutes, competitive rivalry
- [TAM/SAM/SOM](https://www.antler.co/blog/tam-sam-som) — Top-down (market share), bottom-up (customers × ACV), and value-theory approaches
- [Gartner Magic Quadrant](https://www.americaneagle.com/insights/blog/post/what-is-gartner-magic-quadrant-and-why-does-it-matter) — Leaders, Challengers, Visionaries, Niche Players; Ability to Execute vs. Completeness of Vision axes
- IBISWorld, Antler, HG Insights market sizing methodology — segment-level SAM filtering, competitive win-rate SOM
