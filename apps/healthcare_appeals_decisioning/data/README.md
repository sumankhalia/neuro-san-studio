# Data Overview

This directory contains all inputs used by the Healthcare Appeals
Decisioning app.

## Structure
- cases/: Entry-point JSON files consumed by LangGraph
- documents/: PDFs used as supporting evidence
- images/: Medical images and scanned documents
- annotations/: Structured signals extracted from multimodal inputs
- synthetic/: Documentation on synthetic data generation

## Design Principles
- No raw text embedded in code
- No real patient data
- Deterministic, auditable inputs
