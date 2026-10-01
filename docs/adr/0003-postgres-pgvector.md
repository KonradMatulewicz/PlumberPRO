# ADR-0003: PostgreSQL with pgvector for both relational data and embeddings
Status: Accepted
## Context
Need ACID relational storage (runs, alerts, audit) and a vector store for RAG; free tier allows
one managed database.
## Decision
Postgres 16 + pgvector (locally `pgvector/pgvector` image; hosted e.g. Neon). Relational schema
in 3NF with constraints; embeddings table with vector column.
## Consequences
+ one database, transactional consistency, SQL read models. - vector search scale limited;
fine for hundreds/thousands of chunks.
