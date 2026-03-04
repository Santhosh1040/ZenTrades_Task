import json
import re
from pathlib import Path


ACCOUNTS_FOLDER = Path("../outputs/accounts")
ONBOARDING_FOLDER = Path("../input/onboarding_calls")


def load_v1_memo(account_folder):

    v1_path = account_folder / "v1" / "account_memo.json"

    with open(v1_path, "r") as f:
        return json.load(f)


def save_v2_memo(account_folder, memo):

    v2_folder = account_folder / "v2"
    v2_folder.mkdir(exist_ok=True)

    output_path = v2_folder / "account_memo.json"

    with open(output_path, "w") as f:
        json.dump(memo, f, indent=4)


def extract_updates(chat_text):

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", chat_text)

    phones = re.findall(r"\d{3}[-]\d{3}[-]\d{4}", chat_text)

    names = []

    lines = chat_text.split("\n")

    for line in lines:

        if "From BP" in line:

            value = line.split(":")[-1].strip()

            if not re.search(r"@", value) and not re.search(r"\d", value):

                names.append(value)

    return {
        "emails": list(set(emails)),
        "phones": list(set(phones)),
        "names": list(set(names))
    }


def process_onboarding(account_folder, chat_file):

    memo = load_v1_memo(account_folder)

    with open(chat_file, "r") as f:
        chat_text = f.read()

    updates = extract_updates(chat_text)

    memo["notes"] = {
        "contact_emails": updates["emails"],
        "contact_phones": updates["phones"],
        "staff_names": updates["names"]
    }

    save_v2_memo(account_folder, memo)

    print(f"Updated account to v2: {memo['account_id']}")


if __name__ == "__main__":

    chat_files = list(ONBOARDING_FOLDER.glob("*.txt"))

    if not chat_files:
        print("No onboarding chat file found")
        exit()

    chat_file = chat_files[0]

    for account_folder in ACCOUNTS_FOLDER.iterdir():

        if account_folder.is_dir():

            process_onboarding(account_folder, chat_file)