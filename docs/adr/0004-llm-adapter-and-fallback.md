# ADR-0004: LLM and embeddings behind ports, with deterministic fallback
Status: Accepted
## Context
The demo must never fail; LLM APIs can error, rate-limit or cost money; free-tier RAM is small.
## Decision
`LLMPort` (default adapter: Anthropic API, model from env `LLM_MODEL`) and `EmbeddingPort`
(default: TF-IDF via scikit-learn, optional fastembed). If the LLM call fails or no key is set,
a template-based answer is composed from the retrieved runbook chunks.
## Consequences
+ testable with fakes, provider-agnostic, demo-safe, cheap. - fallback answers are less fluent.
