import json
import os
import re
from pathlib import Path
from jsonschema import validate


SCHEMA_PATH = Path("../schemas/account_schema.json")
OUTPUT_BASE = Path("../outputs/accounts")


# -------------------------
# Load base schema template
# -------------------------
def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


# -------------------------
# Normalize transcript text
# -------------------------
def normalize_text(text):
    return text.lower()


# -------------------------
# Extract company name
# -------------------------
def extract_company_name(text):
    patterns = [
        r"company name is ([a-zA-Z0-9\s&']+)",
        r"from ([a-zA-Z0-9\s&']+) company",
        r"([a-zA-Z0-9\s&']+) electrical"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    return ""


# -------------------------
# Extract services
# -------------------------
def extract_services(text):
    service_keywords = [
        "electrical",
        "residential",
        "commercial",
        "service call",
        "projects",
        "maintenance",
        "installation",
        "inspection",
        "repair",
        "troubleshooting"
    ]

    found = []

    for keyword in service_keywords:
        if keyword in text:
            found.append(keyword)

    return list(set(found))


# -------------------------
# Extract emergency triggers
# -------------------------
def extract_emergency_definitions(text):
    triggers = []

    emergency_phrases = [
        "emergency",
        "urgent",
        "after hours",
        "immediate help",
        "critical issue",
        "power outage",
        "electrical failure"
    ]

    for phrase in emergency_phrases:
        if phrase in text:
            triggers.append(phrase)

    return list(set(triggers))


# -------------------------
# Detect integrations
# -------------------------
def extract_integrations(text):
    integrations = []

    integration_keywords = [
        "jobber",
        "quickbooks",
        "crm",
        "dispatch system",
        "scheduling software"
    ]

    for keyword in integration_keywords:
        if keyword in text:
            integrations.append(keyword)

    return list(set(integrations))


# -------------------------
# Generate account id
# -------------------------
def generate_account_id(company_name, filename):

    # Always use filename for stable account_id
    return Path(filename).stem.lower().replace(" ", "_")


# -------------------------
# Save v1 output
# -------------------------
def save_v1(account_id, memo):

    account_folder = OUTPUT_BASE / account_id / "v1"
    os.makedirs(account_folder, exist_ok=True)

    output_file = account_folder / "account_memo.json"

    # Validate memo against schema before saving
    schema = load_schema()
    validate(instance=memo, schema=schema)

    with open(output_file, "w") as f:
        json.dump(memo, f, indent=4)


# -------------------------
# Process demo transcript
# -------------------------
def process_demo_file(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()

    text = normalize_text(raw_text)

    schema = load_schema()

    company_name = extract_company_name(text)
    services = extract_services(text)
    emergency_triggers = extract_emergency_definitions(text)
    integrations = extract_integrations(text)

    schema["company_name"] = company_name
    schema["services_supported"] = services
    schema["emergency_definition"] = emergency_triggers
    schema["integration_constraints"] = integrations

    if not company_name:
        schema["questions_or_unknowns"].append(
            "Company name not explicitly stated in demo."
        )

    if not schema["business_hours"]["days"]:
        schema["questions_or_unknowns"].append(
            "Business hours not specified in demo."
        )

    account_id = generate_account_id(company_name, filepath)
    schema["account_id"] = account_id

    save_v1(account_id, schema)

    print(f"Processed demo for account: {account_id}")


# -------------------------
# Main runner
# -------------------------
if __name__ == "__main__":

    demo_folder = Path("../input/demo_calls")

    for file in demo_folder.glob("*.txt"):
        process_demo_file(file)