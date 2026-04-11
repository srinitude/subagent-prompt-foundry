# Invocation

```
/subagent-prompt-foundry Create a reusable subagent prompt for sample clearance research. My beat-making agent needs to delegate to a specialist that identifies the original song, publisher, master owner, and clearance difficulty for any sample a producer wants to flip.
```

## Routing decision

**ACTIVATE** — the user explicitly requests a reusable subagent prompt; a beat-making parent agent delegates sample clearance research to a specialist subagent. All routing-checklist.md criteria pass:

1. The output should be a reusable system prompt ✓
2. The prompt defines a custom subagent (sample clearance research specialist) ✓
3. Direct task execution is not the goal ✓
4. A meta-agent prompt is not the goal ✓

## Research performed

- [Tracklib — Sample Clearance Guide](https://www.tracklib.com/blog/music-clearance) — master use license vs. composition license; two-sided clearance requirement
- [Musicians Institute — Master vs. Publishing Rights](https://www.mi.edu/in-the-know/music-copyright-law-publishing-rights-masters-rights-royalties/) — master rights (sound recording) vs. publishing rights (melody/lyrics); interpolation vs. direct sample
- [Harry Fox Agency](https://exploration.io/what-is-the-harry-fox-agency/) — HFA administers mechanical licenses (non-digital phonorecords); MLC handles U.S. streaming mechanicals post-Music Modernization Act
- [Horn Wright LLP — Sampling Law](https://www.hornwright.com/blog/2025/march/music-sampling-play-it-smart-or-pay-the-price/) — no fair use defense for commercial sampling; master use + composition license required
- [WhoSampled](https://www.whosampled.com) — largest database of sample/cover/remix connections; crowd-verified data
- [Good Morn Music — HFA vs. MLC](https://goodmornmusic.com/what-do-hfa-harry-fox-agency-and-the-mlc-mechanical-licensing-collective-do/) — HFA vs. MLC responsibilities post-MMA
