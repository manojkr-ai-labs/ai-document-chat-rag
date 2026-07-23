# ADR-001: RAG Architecture

## Status
Accepted

## Context

The application needs to answer questions from PDFs.

## Decision

Use Retrieval-Augmented Generation (RAG):

PDF
 ↓
Chunking
 ↓
Embedding
 ↓
ChromaDB
 ↓
Retriever
 ↓
LLM

## Consequences

Pros
- Fast retrieval
- Scalable
- Multiple PDFs supported

Cons
- Requires embedding step
- Index rebuild after document changes