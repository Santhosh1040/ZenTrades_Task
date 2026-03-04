# Clara AI Onboarding Automation Pipeline

## Overview

This project implements an automation pipeline that converts **human onboarding conversations into structured AI voice agent configurations**.

The system simulates Clara AI's onboarding workflow:

Human conversation → structured operational rules → AI agent configuration → deployable voice agent prompt.

The pipeline extracts operational details from demo and onboarding transcripts and produces version-controlled agent configurations.

---

# Problem This Solves

Service businesses receive many customer calls. Clara AI deploys voice agents that:

• answer incoming calls  
• detect emergencies  
• route calls to technicians  
• collect caller information  
• handle after-hours requests  

However, every company has **different rules, services, and routing logic**.

This system automates the process of converting messy onboarding conversations into **structured agent configurations**.

---

# System Architecture

The pipeline processes conversations in two stages.

## Stage 1 — Demo Call (v1)

The system extracts assumptions from demo conversations and generates the **initial agent configuration**.

Demo Transcript  
↓  
Extraction Engine  
↓  
Account Memo (v1)  
↓  
Agent Spec Generator  
↓  
Voice Agent Prompt  

## Stage 2 — Onboarding Call (v2)

Once the customer signs up, onboarding conversations provide confirmed operational rules.

Onboarding Transcript  
↓  
Update Engine  
↓  
Account Memo (v2)  
↓  
Updated Agent Spec  
↓  
Changelog  

---

# Project Structure

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
│   └ accounts
│       └ <account_id>
│           ├ v1
│           └ v2
│
├ changelog
│
└ README.md
```

---

# Pipeline Components

## 1. Demo Extraction

`scripts/extract_demo.py`

Extracts key information from demo transcripts such as:

- company name  
- services supported  
- emergency triggers  
- integrations  
- missing information  

Output generated:

```
outputs/accounts/<account_id>/v1/account_memo.json
```

---

## 2. Onboarding Updates

`scripts/apply_onboarding_updates.py`

Processes onboarding conversations and updates the configuration.

Output generated:

```
outputs/accounts/<account_id>/v2/account_memo.json
```

A **changelog** describing configuration changes is also generated.

---

## 3. Agent Spec Generator

`scripts/generate_agent_spec.py`

Generates the **AI voice agent configuration** including:

- system prompt  
- routing rules  
- business hours behavior  
- after-hours emergency logic  
- transfer and fallback protocols  

Output:

```
agent_spec.json
```

---

## 4. Pipeline Runner

`scripts/run_pipeline.py`

Runs the entire pipeline end-to-end.

```
Demo Extraction
→ Onboarding Updates
→ Agent Spec Generation
```

---

# Output Artifacts

Each account produces the following:

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

# Agent Prompt Behavior

The generated agent prompt defines how the voice agent handles calls.

## Office Hours Flow

- greet the caller
- ask the purpose of the call
- collect caller name and phone number
- detect emergency vs non-emergency
- route or transfer the call
- fallback if transfer fails
- confirm next steps
- ask if anything else is needed
- close the call

## After Hours Flow

- greet the caller
- confirm if the issue is an emergency
- collect name, phone number, and service address
- attempt technician transfer
- fallback if transfer fails
- log request for follow-up
- close the call politely

---

# Handling Missing Data

The system avoids hallucinating information.

If information is missing, it is stored under:

```
questions_or_unknowns
```

This ensures only **verified operational rules** are used in the final agent configuration.

---

# Versioning

The system maintains version-controlled configurations.

| Version | Source |
|------|------|
| v1 | Demo transcript |
| v2 | Onboarding transcript |

Changes between versions are logged in:

```
changelog/
```

---

# Running the Pipeline

Run the full system with:

```bash
python scripts/run_pipeline.py
```

The pipeline will:

1. Extract demo information
2. Apply onboarding updates
3. Generate agent specifications

---

# Requirements

Python 3.9+

Install dependencies:

```bash
pip install jsonschema
```

No paid APIs or external services are required.

---

# Limitations

This implementation uses **rule-based extraction instead of a large language model**.

Possible limitations include:

- limited entity extraction
- simple emergency detection
- rule-based routing logic

---

# Future Improvements

With production access, the system could be expanded with:

- LLM-based conversation understanding
- automatic audio transcription
- CRM integrations
- real-time agent deployment
- monitoring dashboards
- automated prompt QA

---

# Summary

This project demonstrates a system that converts **unstructured onboarding conversations into structured AI agent configurations**.

Key engineering goals achieved:

- schema-based configuration
- version-controlled agent definitions
- safe automation with missing data handling
- reproducible pipelines
- structured prompt generation