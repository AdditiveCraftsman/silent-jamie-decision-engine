# Deferred: live system (not Phase 0)

The long-term idea is an Android Samsung Galaxy A16 running a phone-first PWA as mic and display, with a Windows ASUS laptop doing any heavy ASR and retrieval. A browser served from a laptop LAN IP is generally **not a secure context** on Android; microphone APIs usually require HTTPS or localhost. Plan for a trusted HTTPS local endpoint or equivalent secure origin when Phase 2 begins. Avoid embedding API keys in client-side JavaScript.

Potential layers to re-evaluate with current hardware/latency tests: local Vosk or faster-whisper server; browser mic/HTTPS WebSocket transport; source retrieval using SearXNG or an API; source quality assessment; mobile cards; directed trigger.

The laptop has constrained RAM and older GPU hardware. Avoid building an always-running Docker/Kubernetes stack before measuring latency and memory pressure. No source-verification pipeline or Android PWA is claimed as implemented.
