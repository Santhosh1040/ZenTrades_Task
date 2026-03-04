import os

print("Running demo extraction...")
os.system("python extract_demo.py")

print("Applying onboarding updates...")
os.system("python apply_onboarding_updates.py")

print("Generating agent specs...")
os.system("python generate_agent_spec.py")

print("Pipeline completed.")