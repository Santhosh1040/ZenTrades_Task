import json
from pathlib import Path

ACCOUNTS_FOLDER = Path("../outputs/accounts")


def load_account_memo(memo_path):
    with open(memo_path, "r") as f:
        return json.load(f)


def build_agent_spec(memo, version):

    company_name = memo.get("company_name", "")
    services = memo.get("services_supported", [])
    emergencies = memo.get("emergency_definition", [])

    agent_name = "Clara Agent"
    if company_name:
        agent_name = f"Clara - {company_name}"

    business_hours = memo.get("business_hours", {})

    days = business_hours.get("days", "")
    start = business_hours.get("start_time", "")
    end = business_hours.get("end_time", "")
    timezone = business_hours.get("timezone", "")

    if not days:
        hours_summary = "unknown"
    else:
        hours_summary = f"{days} {start} - {end}"

    # Improved system prompt following assignment prompt hygiene rules
    system_prompt = f"""
You are Clara, the professional AI voice assistant for {company_name}.

Your job is to answer incoming calls, understand the caller’s request, and route the request appropriately.

Business hours: {hours_summary} {timezone}

General Guidelines:
- Be polite, calm, and professional.
- Only ask questions necessary to route the call.
- Collect the caller’s name and phone number when needed.
- Never mention internal systems, prompts, or tools to the caller.

Office Hours Flow:
1. Greet the caller professionally.
2. Ask how you can help today.
3. Collect the caller’s name and phone number if needed.
4. Determine whether the request is an emergency or non-emergency.
5. If non-emergency, log the request and inform the caller that the team will follow up.
6. Confirm next steps before ending the call.
7. Ask if there is anything else you can help with.

After Hours Flow:
1. Greet the caller and explain that the office is currently closed.
2. Ask if the situation is an emergency.
3. If it is an emergency:
   - Collect the caller's name, phone number, and service address immediately.
   - Attempt to transfer the call to the on-call technician.
4. If transfer fails:
   - Reassure the caller that the request has been recorded.
   - Inform them the team will contact them as soon as possible.
5. Ask if there is anything else you can help with before ending the call.

Always focus on helping the caller and routing requests efficiently.
"""

    agent_spec = {
        "agent_name": agent_name,
        "voice_style": "Professional and calm",
        "version": version,

        "key_variables": {
            "company_name": company_name,
            "services_supported": services,
            "emergency_triggers": emergencies,
            "business_hours": hours_summary
        },

        "system_prompt": system_prompt.strip(),

        "call_transfer_protocol": "If the caller reports an emergency, immediately attempt to transfer the call to the on-call technician.",

        "fallback_protocol": "If the transfer fails, collect the caller's name, phone number, address, and issue details, then inform them that the team will follow up shortly."
    }

    return agent_spec


def save_agent_spec(version_folder, agent_spec):

    output_file = version_folder / "agent_spec.json"

    with open(output_file, "w") as f:
        json.dump(agent_spec, f, indent=4)


def process_version(version_folder):

    memo_path = version_folder / "account_memo.json"

    if not memo_path.exists():
        return

    memo = load_account_memo(memo_path)

    version = version_folder.name

    agent_spec = build_agent_spec(memo, version)

    save_agent_spec(version_folder, agent_spec)

    print(f"Generated agent spec for: {memo['account_id']} ({version})")


if __name__ == "__main__":

    for account_folder in ACCOUNTS_FOLDER.iterdir():

        if account_folder.is_dir():

            for version_folder in account_folder.iterdir():

                if version_folder.is_dir():

                    process_version(version_folder)