# Clara AI Onboarding Automation Pipeline

## Overview

This project implements an automation pipeline that converts onboarding conversations into structured AI voice agent configurations.

The system extracts operational rules from demo and onboarding transcripts and generates versioned agent specifications that define how Clara AI should handle customer calls.

---

## Architecture

The pipeline processes conversations in two stages.

### Stage 1 — Demo Call (v1)

Demo transcript → Extract operational data → Generate account memo → Generate agent configuration.

### Stage 2 — Onboarding Call (v2)

Onboarding transcript → Apply updates → Regenerate configuration → Create changelog.

```
Demo Transcript
      ↓
Extraction
      ↓
Account Memo (v1)
      ↓
Agent Spec
```

```
Onboarding Transcript
      ↓
Update Engine
      ↓
Account Memo (v2)
      ↓
Updated Agent Spec
      ↓
Changelog
```

---

## Project Structure

```
ZenTrades_Task
│
├ scripts
│   ├ extract_demo.py
│   ├ apply_onboarding_updates.py
│   ├ generate_agent_spec.py
│   └ run_pipeline.py
│
├ schemas
│   └ account_schema.json
│
├ workflows
│   └ voice_agent_workflow.json
│
├ input
│   ├ demo_calls
│   └ onboarding_calls
│
├ outputs
│   └ accounts/<account_id>/
│       ├ v1
│       └ v2
│
├ changelog
└ README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repo_url>
cd ZenTrades_Task
```

### 2. Install dependencies

```bash
pip install jsonschema
```

Python 3.9+ recommended.

### 3. Add transcripts

Place demo transcripts in:

```
input/demo_calls/
```

Place onboarding transcripts in:

```
input/onboarding_calls/
```

---

## Running the Pipeline

Run the pipeline using:

```bash
python scripts/run_pipeline.py
```

The pipeline will automatically:

1. Extract demo information
2. Generate v1 configuration
3. Apply onboarding updates
4. Generate v2 configuration
5. Produce changelog

---

## Outputs

For each account the system generates:

```
outputs/accounts/<account_id>/

v1/
  account_memo.json
  agent_spec.json

v2/
  account_memo.json
  agent_spec.json
```

---

## Prompt Behavior

The generated agent prompt includes structured handling for:

### Business Hours Flow

- greet caller
- ask purpose
- collect name and phone number
- detect emergency vs non-emergency
- route or transfer call
- fallback if transfer fails
- confirm next steps
- close call

### After Hours Flow

- greet caller
- confirm emergency
- collect name, phone, address
- attempt technician transfer
- fallback if transfer fails
- log request for follow-up
- close call politely

---

## Handling Missing Data

The system avoids hallucinating information.

If information is missing, it is recorded under:

```
questions_or_unknowns
```

---

## Limitations

This implementation uses rule-based extraction rather than an LLM, which may miss complex conversational signals.

---

## Future Improvements

With production access this system could include:

- LLM-based extraction
- automatic speech transcription
- CRM integrations
- monitoring dashboards
- automated prompt evaluation
