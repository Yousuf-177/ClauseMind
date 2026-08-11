# Multi-Document RAG Legal Assistant — Scope Document

## Project Summary

A production-quality Retrieval-Augmented Generation (RAG) system that allows users to upload multiple legal documents and ask natural-language questions, receiving accurate, citation-backed answers that reference specific documents, clauses, and page numbers.

---

## Supported Document Types

| Document Type | Examples | Format |
|---------------|----------|--------|
| **Contracts** | NDAs, service agreements, employment contracts, lease agreements | PDF |
| **Case Law / Court Opinions** | Federal and state court decisions, appellate rulings | PDF |
| **SEC Filings** | 10-K annual reports, 10-Q quarterly reports, 8-K filings | PDF |
| **EULAs / Terms of Service** | Software license agreements, website terms, privacy policies | PDF |
| **Statutes / Legislative Text** | Federal and state statutes, regulations, code sections | PDF |
| **Legal Briefs / Memoranda** | Trial briefs, appellate briefs, legal memoranda | PDF |

---

## Supported Question Types

1. **Factual Extraction** — Retrieve specific facts, dates, names, or values from a document.
2. **Cross-Document Comparison** — Compare clauses, terms, or provisions across two or more documents.
3. **Summarization** — Provide concise summaries of sections, clauses, or entire documents.
4. **Clause / Section Location** — Identify which section or page addresses a specific topic.
5. **Yes/No Legal Interpretation** — Determine whether a document contains a specific provision or clause.
6. **Definition Lookup** — Find how a specific term is defined within a document.
7. **Obligation / Right Identification** — Identify what each party is obligated to do or entitled to.
8. **Risk / Liability Questions** — Identify liability caps, indemnification terms, or risk allocation.

---

## 10 Example Q&A Pairs

These pairs will serve as the initial evaluation baseline for the retrieval and generation pipeline.

### 1. Factual Extraction (Single Document)
- **Q**: What is the termination notice period specified in the NDA?
- **Expected A**: The NDA requires 30 days' written notice for termination by either party.
- **Source**: `contract_nda_sample.pdf`, Section 5 (Term and Termination), Page 3

### 2. Clause Location (Single Document)
- **Q**: Which section of the service agreement covers dispute resolution?
- **Expected A**: Dispute resolution is covered in Section 12 — Governing Law and Dispute Resolution.
- **Source**: `contract_service_agreement.pdf`, Section 12, Page 8

### 3. Yes/No Legal Interpretation (Single Document)
- **Q**: Does the employment contract contain a non-compete clause?
- **Expected A**: Yes, the employment contract includes a non-compete clause in Section 7, restricting the employee from working with competitors for 12 months after termination within a 50-mile radius.
- **Source**: `contract_employment.pdf`, Section 7 (Non-Competition), Page 4

### 4. Cross-Document Comparison
- **Q**: Compare the indemnification clauses in the NDA and the service agreement.
- **Expected A**: The NDA limits indemnification to breaches of confidentiality obligations (Section 6), while the service agreement provides broader mutual indemnification covering IP infringement, negligence, and breach of warranty (Section 9). The service agreement also caps indemnification at the total fees paid in the preceding 12 months, whereas the NDA has no monetary cap.
- **Source**: `contract_nda_sample.pdf`, Section 6, Page 3; `contract_service_agreement.pdf`, Section 9, Page 6

### 5. Summarization
- **Q**: Summarize the key obligations of the licensee in the software EULA.
- **Expected A**: The licensee must: (1) use the software only for internal business purposes, (2) not reverse-engineer, decompile, or modify the software, (3) maintain confidentiality of the license key, (4) comply with all applicable export control laws, and (5) not sublicense or transfer the license without prior written consent.
- **Source**: `eula_software_license.pdf`, Sections 2–4, Pages 2–4

### 6. Definition Lookup
- **Q**: How is "Confidential Information" defined in the NDA?
- **Expected A**: "Confidential Information" means all non-public information disclosed by either party, including but not limited to trade secrets, business plans, financial data, technical specifications, customer lists, and proprietary software, whether disclosed orally, in writing, or electronically.
- **Source**: `contract_nda_sample.pdf`, Section 1 (Definitions), Page 1

### 7. Obligation Identification
- **Q**: What are the reporting obligations of the company in the SEC 10-K filing?
- **Expected A**: The company is required to disclose: financial statements audited by an independent CPA, management's discussion and analysis (MD&A) of financial condition, risk factors, legal proceedings, and executive compensation details.
- **Source**: `sec_filing_10k_sample.pdf`, Items 7, 8, and 11, Pages 15–45

### 8. Risk / Liability Question
- **Q**: What is the limitation of liability in the service agreement?
- **Expected A**: The service agreement limits liability to direct damages not exceeding the total fees paid by the client in the 12 months preceding the claim. It excludes liability for indirect, consequential, incidental, or punitive damages.
- **Source**: `contract_service_agreement.pdf`, Section 10 (Limitation of Liability), Page 7

### 9. Cross-Document Comparison (Statute vs Contract)
- **Q**: Does the software EULA's data collection practice comply with the GDPR excerpt's requirements for user consent?
- **Expected A**: The EULA states that the software collects usage analytics automatically upon installation (Section 5). The GDPR excerpt requires explicit, informed, freely given consent before processing personal data (Article 6/7). The EULA's automatic collection without explicit opt-in consent appears non-compliant with GDPR requirements.
- **Source**: `eula_software_license.pdf`, Section 5, Page 5; `statute_gdpr_excerpt.pdf`, Articles 6–7, Pages 3–4

### 10. Out-of-Scope Question (Abstention Expected)
- **Q**: What was the judge's personal opinion about the defendant's character?
- **Expected A**: Insufficient evidence — the uploaded documents do not contain subjective judicial commentary about the defendant's character. The system can only answer based on the text present in the uploaded documents.
- **Source**: N/A (expected abstention)

---

## Out of Scope

The following are explicitly **not** supported in this project:

- **OCR / Scanned Documents**: Only digitally-created PDFs with selectable text are supported. Scanned image-only PDFs are out of scope.
- **Audio / Video**: No processing of audio recordings, video depositions, or multimedia content.
- **Non-English Text**: Only English-language documents are supported.
- **Real-Time Legal Advice**: The system provides information retrieval and text-based analysis, not legal counsel. Outputs should not be treated as legal advice.
- **Document Drafting / Editing**: The system answers questions about existing documents; it does not generate or modify legal documents.
- **Handwritten Notes**: Handwritten annotations or documents are not supported.
- **Real-Time Data**: No integration with live legal databases, court docket systems, or news feeds.
- **Multi-Language Translation**: No translation of documents between languages.

---

## Document Volume Constraints

- **Maximum documents per session**: 20
- **Maximum pages per document**: 200
- **Maximum total corpus size**: ~2,000 pages
- **Supported format**: PDF only (DOCX support is future work)

---

## Quality Targets

| Metric | Target | Measured Via |
|--------|--------|--------------|
| Retrieval Precision@5 | ≥ 0.70 | RAGAS context precision |
| Retrieval Recall@5 | ≥ 0.75 | RAGAS context recall |
| Faithfulness | ≥ 0.85 | RAGAS faithfulness |
| Answer Relevance | ≥ 0.80 | RAGAS answer relevance |
| Abstention on out-of-scope | ≥ 80% | Manual evaluation on 10 OOS questions |
| Hybrid vs Naive retrieval improvement | +15–25% | Precision/recall delta |
