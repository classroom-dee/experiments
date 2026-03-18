- Use redis instead of file sensors or use 

- the relation between the three is gkg *-* mentions *-1 events

1. Parse query into structured constraints vs semantic constraints.
Structured: year, date range, actor names, locations, event types, known organizations.
Semantic: “relevance,” “impact,” “fear,” “tension,” “broad terms,” “how connected,” “narrative around.”
Map structured constraints first to Event/GKG filters, then use embeddings on the semantic side. This is an inference from the table roles, but it follows directly from what each table stores.

2. Retrieve candidate articles from GKG for semantic matching.
Build embeddings primarily from GKG text-derived fields such as themes, entities, tone/emotion signals, and possibly linked document metadata. GKG is article-level, so it is the natural layer for “what does this query mean?” retrieval.

3. Map candidate articles to events through Mentions.
This is the bridge from article semantics to event records. GDELT’s own “Combining Events, EventMentions, and GKG” example does exactly this: GKG DocumentIdentifier → EventMentions MentionIdentifier → Events GLOBALEVENTID.

4. Rank final results at the event level using Events.
Use Events as the deduplicated output layer. Then enrich the score with mention count, confidence, and article-level semantic similarity from GKG. This gives you event-centric answers instead of a pile of article hits.

### Sorting
- final_score = event_match + semantic_match + mention_salience + temporal_fit
- event_match comes from Events fields like actors, CAMEO type, geography, date.
- semantic_match comes from GKG embedding similarity, themes, entities, tone/GCAM.
- mention_salience comes from Mentions count, confidence, sentence prominence, and maybe source diversity.
- temporal_fit rewards the requested year/range.
- Resolve explicit items: event X, event A, year Y, year B.

### Query
Pull candidate event nodes from Events for both periods.

Pull contextual articles from GKG around those events or their actors/themes.

Join through Mentions to connect article context to event IDs.

Compute “relevance” using a hybrid of:

actor overlap / actor network distance from Events

theme/entity overlap from GKG

embedding similarity on GKG context

mention intensity and confidence from Mentions.

### Price testing
If your infra is mostly Terraform/OpenTofu, I’d start with Infracost + CI policy tests.
If your spend is mostly Kubernetes runtime, I’d look at OpenCost.
If you’re building your own simulator/allocator, I’d use pytest for the engine and treat cloud pricing catalogs as test fixtures.

### Backend
API & request handling

Validate input at the boundary.

Make endpoints idempotent where possible.

Keep API contracts stable; version breaking changes.

Use pagination for any list that can grow.

Put rate limits on expensive or abuse-prone paths.

Reliability & failure handling

Treat timeouts, retries, and backoff as default.

Design for partial failure, not perfect uptime.

Build for safe deploys and easy rollback.

Use feature flags for risky changes.

Performance & scalability

Optimize database access before app micro-optimizations.

Avoid N+1 queries.

Add the right indexes and verify with query plans.

Use caching only with a clear invalidation strategy.

Offload slow, non-urgent work to background jobs.

Use queues to absorb spikes and decouple components.

Keep app servers stateless when possible.

Measure first; don’t optimize blind.

Data & consistency

Make writes atomic when consistency matters.

Minimize shared mutable state.

Be explicit about invariants, edge cases, and failure modes.

Assume distributed systems eventually become consistency problems.

Observability

Use structured logs with request IDs.

Expose metrics and alerts for latency, errors, throughput, and saturation.

Make systems observable before trying to scale them.

Security & configuration

Keep config out of code.

Store secrets in a proper secret manager.

Enforce least privilege.

Sanitize inputs and parameterize DB queries; trust nothing by default.

Architecture mindset

Prefer simple architecture over clever architecture.