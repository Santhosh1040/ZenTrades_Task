# Clara AI – Automation Pipeline Assignment

This project implements a **zero-cost automation pipeline** that converts customer conversations into a structured AI voice agent configuration.

The system simulates Clara’s real onboarding workflow:

Demo Call → Account Memo (v1) → Agent Spec (v1) → Onboarding Update → Agent Spec (v2)

The pipeline extracts operational rules from transcripts and generates a structured configuration that can be used to deploy a Clara AI voice agent.

---

# Architecture Overview

The system is designed as a **modular pipeline**:

Demo Transcript
        ↓
Extraction Engine
        ↓
Account Memo (v1 JSON)
        ↓
Agent Spec Generator
        ↓
Retell Agent Draft (v1)
        ↓
Onboarding Update
        ↓
Account Memo (v2 JSON)
        ↓
Updated Agent Spec (v2)

Key design principles:

- Separation between **demo assumptions (v1)** and **confirmed onboarding configuration (v2)**
- **No hallucinated data**
- Missing information flagged under `questions_or_unknowns`
- Version-controlled outputs
- Fully repeatable automation pipeline

---

# Project Structure
