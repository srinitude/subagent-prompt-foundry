# Invocation

```
/subagent-prompt-foundry Design a production-grade subagent prompt for mix/master critique. A producer's DAW assistant delegates with a stereo bounce and reference track. Analyze frequency balance, dynamic range, stereo width, loudness (LUFS), and return actionable EQ/compression suggestions with specific frequency ranges and dB values.
```

## Routing decision

**ACTIVATE** — the user explicitly requests a production-grade subagent prompt; a DAW assistant parent agent delegates the audio critique task. All routing-checklist.md criteria pass:

1. The output should be a reusable system prompt ✓
2. The prompt defines a custom subagent (mix/master critique specialist) ✓
3. Direct task execution is not the goal ✓
4. A meta-agent prompt is not the goal ✓

## Research performed

- [iZotope — Mastering for Streaming Platforms](https://www.izotope.com/en/learn/mastering-for-streaming-platforms) — AES AESTD1008 recommendation: −16 LUFS music, −14 LUFS album normalization; Spotify target −14 LUFS (default); −1 dBTP true peak
- [Youlean — Loudness Standards Comparison Table](https://youlean.co/loudness-standards-full-comparison-table/) — AES Streaming: −16 to −20 LUFS integrated, −1 dBTP
- [K-system — MeterPlugs](https://www.meterplugs.com/blog/2016/10/14/k-system-metering-101.html) — K-12 (broadcast), K-14 (pop/rock), K-20 (film/classical); 83 dBSPL reference at 0 dB RMS
- [iZotope — Fletcher-Munson Curves](https://www.izotope.com/en/learn/what-is-fletcher-munson-curve-equal-loudness-curves) — ear sensitivity peaks 2–5 kHz; 100 Hz requires ~10 dB more SPL than 1 kHz to sound equally loud; drives low-end management decisions
- [RTW — Worldwide Loudness Delivery Standards](https://www.rtw.com/blog/rtw-knowledge-base-1/worldwide-loudness-delivery-standards-4) — global streaming and broadcast targets
