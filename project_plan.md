# Project: Multi-Document RAG Legal Assistant

**Goal**: Build a production-quality Retrieval-Augmented Generation system that lets a user upload multiple legal documents (contracts, case files, statutes, briefs) and ask natural-language questions, getting accurate, citation-backed answers that reference specific documents, clauses, and page numbers.

**Timeline**: 6 weeks (buffer built into 8-week window)
**Team**: Solo
**Type**: Implementation project — stack is fixed upfront, no open-ended comparison/research tasks. Every task below builds something, not "evaluates options."

**Primary objectives**:
1. A working end-to-end app (ingest → retrieve → generate → cite) deployed and demoable via a live link.
2. A GitHub repo with clean architecture, tests, and a README that reads like a technical case study.
3. Real understanding of chunking, embeddings, hybrid retrieval, re-ranking, evaluation, and hallucination mitigation — gained by building each piece, not surveying alternatives.

---

## Fixed Tech Stack (locked — no swapping mid-project)

| Layer | Choice | Why it's fixed here |
|-------|--------|----------------------|
| PDF/DOCX parsing | **PyMuPDF (fitz)** | Fast, preserves page numbers, handles most legal PDFs |
| Chunking | **RecursiveCharacterTextSplitter + regex clause splitter** | One general-purpose splitter + one structure-aware splitter for legal sections ("Section 4.2", "WHEREAS") |
| Embeddings | **Gemini `text-embedding-004`** (Google SDK) | Free tier, solid quality, keeps you in one SDK ecosystem |
| Vector DB | **ChromaDB (local)** | Zero infra setup, metadata filtering built in |
| Sparse retrieval | **BM25 (`rank_bm25`)** | Standard keyword baseline, pairs with dense for hybrid search |
| Re-ranker | **`bge-reranker-base` (local, HuggingFace)** | Free, no extra API dependency |
| LLM (generation) | **Gemini 2.5 Pro/Flash API (Google SDK, `google-genai`)** | Same ecosystem as embeddings, generous free tier, strong long-context support (useful for multi-doc legal text) |
| Backend | **FastAPI** | Standard, resume-recognizable |
| Frontend | **Streamlit** | Fast to build, good enough for a demo |
| Evaluation | **RAGAS** | Single framework, standard metric names recruiters/interviewers recognize |
| Deployment | **Docker → Render (API) + Streamlit Community Cloud (UI)** | Free tier, simple |

No task below asks you to "compare" or "choose between" tools — those decisions are made. Every task is: build it, wire it in, verify it works.

---

## Milestones

| # | Milestone | Target | Success Criteria |
|---|-----------|--------|-------------------|
| 1 | Core RAG pipeline works end-to-end (naive) | End Week 2 | Upload 1 PDF, ask a question, get an answer with a source chunk |
| 2 | Multi-document + hybrid retrieval works | End Week 4 | Query across 5+ docs; hybrid + re-ranking pipeline live and wired in |
| 3 | Evaluation + hallucination guardrails | End Week 5 | RAGAS scores computed on a fixed test set; answers abstain when evidence is weak |
| 4 | Deployed app + polished repo | End Week 6 | Live demo link works, README + diagram done, resume bullets written |

---

## Phase 0: Setup (Week 1, Days 1–2)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| Write 1-page scope doc: doc types, question types, 10 example Q&A pairs | 2h | - | Scope doc saved to repo |
| Set up repo, virtualenv, folder structure (`ingestion/`, `retrieval/`, `generation/`, `eval/`, `api/`, `ui/`) | 2h | - | Scaffold pushed to GitHub |
| Get Gemini API key, install `google-genai` SDK, test a hello-world call (embedding + generation) | 2h | Scaffold | Both API calls return successfully in a script |
| Collect test corpus: 8–12 legal-style docs (public contracts, sample case law, SEC filings, EULAs) | 3h | - | Docs stored in `/data/raw`, license-clean |

**Total**: ~9h

---

## Phase 1: Document Ingestion Pipeline (Week 1, Days 3–5)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| Build PyMuPDF parser: extract text with page numbers preserved | 4h | Corpus | Parser outputs (text, page_num) pairs for all test docs |
| Implement RecursiveCharacterTextSplitter with overlap | 2h | Parser | Chunks generated with configurable size/overlap |
| Implement regex-based clause splitter (splits on "Section X.X", "Article X", "WHEREAS", numbered clauses) | 5h | Parser | Correctly segments 90%+ of test docs by clause |
| Define and apply metadata schema (doc_id, doc title, doc type, page, section heading, char_offset) | 2h | Both splitters | Schema applied to every chunk, stored as JSON |
| Write parser/chunker tests on 3 tricky docs (tables, multi-column, scanned) | 3h | All above | Tests pass or documented as out-of-scope |

**Total**: ~16h

---

## Phase 2: Embedding & Vector Store (Week 2, Days 1–3)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| Build embedding function using Gemini `text-embedding-004` (batched calls) | 4h | Chunks ready | All chunks embedded successfully, rate limits handled |
| Set up ChromaDB collection with metadata fields (doc_id, page, section) | 3h | - | Can insert and filter by metadata |
| Build ingestion → embed → upsert pipeline (idempotent — re-running doesn't duplicate) | 5h | Both above | Re-ingesting same doc is a no-op |
| Wire up basic top-k similarity search | 3h | Pipeline | Query returns relevant chunks + scores for 5 test questions |

**Total**: ~15h

---

## Phase 3: Retrieval Pipeline (Week 2 Day 4 – Week 3)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| **Milestone 1 checkpoint**: wire naive retrieval → Gemini generation, single doc | 4h | Basic search | Ask 1 question on 1 doc, get answer + source chunk shown |
| Build BM25 index over all chunks | 3h | Milestone 1 | BM25 search returns results independently |
| Combine dense (Chroma) + sparse (BM25) into hybrid scoring (weighted merge) | 5h | BM25 index | Hybrid search returns merged, deduped, ranked results |
| Integrate `bge-reranker-base` on top-k hybrid candidates | 5h | Hybrid search | Re-ranked top-5 returned for every query |
| Build multi-document routing: metadata-based filtering + cross-doc search when no single doc specified | 5h | Re-ranking | Comparison query ("compare termination clauses in doc A and B") retrieves from both docs |
| Retrieval smoke-test script on the 10 example Q&A pairs from scope doc | 3h | All above | Script confirms correct chunks retrieved for each |

**Total**: ~25h

---

## Phase 4: Answer Generation, Citations & Guardrails (Week 4)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| Build Gemini prompt template that forces inline citations (doc/section/page) per claim | 4h | Retrieval done | Every answer includes citations mapped to real chunk IDs |
| Build citation verification step (check cited chunk text actually supports the claim) | 5h | Prompt template | Mismatched citations flagged automatically |
| Build abstention logic: if top retrieval score is below threshold, respond "insufficient evidence" | 4h | Verification | On 10 out-of-scope test questions, correctly abstains 8+/10 |
| Build multi-doc synthesis prompt (structured comparison/summarization across docs) | 5h | Abstention | Comparison queries return structured, per-doc-cited answers |
| Add conversational follow-up handling (pass prior turn + retrieved context) | 4h | Synthesis prompt | Follow-up question ("what about the other party?") resolves correctly |

**Total**: ~22h

---

## Phase 5: Evaluation Harness (Week 5, Days 1–3)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| Build labeled eval set: 40–50 Q&A pairs (single-doc, multi-doc, comparison, out-of-scope) with expected answers + source chunks | 5h | Phase 4 done | Eval set saved as JSON in `/eval` |
| Integrate RAGAS: faithfulness, answer relevance, context precision/recall | 5h | Eval set | Metrics computed and logged for a full run |
| Run full pipeline (naive vs. hybrid+rerank+guardrails) and log both metric sets | 3h | RAGAS integrated | Comparison table generated — this is your resume proof point |
| Categorize failures by stage (chunking miss, retrieval miss, generation error) | 3h | Comparison run | Written failure taxonomy with examples |
| Fix top 2–3 failure modes found | 4h | Failure taxonomy | Re-run confirms metric improvement |

**Total**: ~20h

---

## Phase 6: API, UI & Deployment (Week 5 Day 4 – Week 6)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| Build FastAPI endpoints: upload doc, ask question, get answer+citations | 6h | Eval fixes done | Endpoints tested via Swagger |
| Build Streamlit frontend: upload PDFs, chat interface | 8h | API | Upload + chat works in browser |
| Show citations in UI (clickable, jumps to source snippet/page) | 4h | Frontend | Clicking a citation highlights the exact source text |
| Containerize with Docker | 3h | UI working | `docker-compose up` runs full stack locally |
| Deploy: FastAPI → Render, Streamlit → Streamlit Community Cloud | 4h | Docker | Public URL works end-to-end |
| Add basic API key auth / rate limiting | 2h | Deployed | Unauthenticated requests blocked or rate-limited |

**Total**: ~27h

---

## Phase 7: Polish, Docs & Resume Packaging (Week 6, final days)

| Task | Effort | Depends On | Done Criteria |
|------|--------|------------|----------------|
| Architecture diagram (ingestion → retrieval → generation → eval flow) | 2h | Deployment done | Diagram in README |
| README as technical case study: problem, approach, tradeoffs, metrics, future work | 4h | Diagram | Reads like a case study, not a tutorial README |
| Record 2–3 min demo video/GIF | 2h | Deployed app | Shows upload → ask → cited answer → comparison query |
| Write resume bullets (quantified from Phase 5 metrics) | 1h | Eval numbers | 2–3 bullets ready to paste into resume |
| Prep interview talking points: chunking approach, hybrid search rationale, citation verification, RAGAS metrics | 3h | Everything | Can explain the system unscripted in 3 minutes |

**Total**: ~12h

---

## Dependencies Map

```
Setup ──> Ingestion ──> Chunking ──> Embedding/VectorDB ──> Naive Retrieval (Milestone 1)
                                                                  │
                                                                  ▼
                                              BM25 ──> Hybrid Search ──> Re-ranking ──> Multi-Doc Routing
                                                                                                │
                                                                                                ▼
                                                          Grounded Generation ──> Citation Verification ──> Abstention
                                                                                                │
                                                                                                ▼
                                                                            Eval Harness (RAGAS) ──> Error Fixes
                                                                                                │
                                                                                                ▼
                                                                        API + UI ──> Deployment ──> Docs & Resume Packaging
```

---

## Weekly Breakdown Summary

| Week | Focus | Hours (approx) |
|------|-------|------------------|
| 1 | Setup + ingestion + chunking | ~25h |
| 2 | Embedding, vector store, retrieval start | ~25h |
| 3 | Hybrid search, re-ranking, multi-doc routing | ~15h |
| 4 | Generation, citations, guardrails | ~22h |
| 5 | Evaluation harness + error fixes | ~24h |
| 6 | API, UI, deployment, polish, resume packaging | ~27h |

**Total effort**: ~138 hours over 6 weeks (~23h/week, with 2 weeks of your 8-week window as buffer for debugging and interview prep)

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Gemini API rate limits slow down batch embedding/eval runs | Medium | Medium | Batch requests, cache embeddings locally, throttle during eval runs |
| PDF parsing pain (scanned docs, weird tables) | Medium | Medium | Curate a clean test corpus upfront; explicitly scope out OCR |
| Regex clause splitter doesn't generalize across all doc formats | Medium | Medium | Fall back to fixed-size splitter per doc-type if regex fails, log which was used |
| Scope creep (adding features not in the fixed-stack plan) | High | Medium | Any new idea goes into a "Future Work" README section, not the codebase |
| Running out of time before deployment | High | Medium | Phase 6 deployment is scoped minimal on purpose (Render + Streamlit Cloud, no custom infra) |

---

## Success Metrics (What Makes This Resume-Worthy)

- **Quantified retrieval improvement**: precision@5 / recall@5, naive vs. hybrid+rerank (target: +15–25%)
- **Faithfulness score** (RAGAS) above a defined threshold, with documented failure analysis
- **Working multi-doc reasoning**: correct comparison answers spanning 2+ documents with per-doc citations
- **Deployed, publicly demoable** — a live link, not just a repo
- **You can explain every architectural decision** without notes

---

## Suggested Daily Cadence (Solo)

- **Weekdays**: 2–3 hours focused work (1 task from the current phase)
- **Weekends**: 4–6 hours for integration work (retrieval pipeline, deployment — things needing uninterrupted focus)
- **End of each week**: 30-min review — update README as you go, don't leave docs for Week 6
