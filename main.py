import shutil
from dotenv import load_dotenv
import os

load_dotenv()
from browserpilot.agents.gpt_selenium_agent import GPTSeleniumAgent

# Check if the logs directory exists and delete it if it does
if os.path.exists("logs"):
    shutil.rmtree("logs")
os.makedirs("logs", exist_ok=True)

# Read instructions from the text file
with open("tests.txt", "r") as file:
    instructions = file.read()

# Initialize test results dictionary
test_results = {}
with open("tests.txt", "r") as file:
    for line in file:
        if line.startswith("Test"):
            test_number = line.strip().split(":")[0]
            test_results[test_number] = "OK"

agent = GPTSeleniumAgent(instructions, "/Users/eli.shemesh/PycharmProjects/llms/chromedriver")

try:
    agent.run()
except Exception as e:
    with open("logs/error.txt", "a") as error_file:
        error_file.write(f"Problem Instruction: {e}\n")

# Check if error.txt exists
if os.path.exists("logs/error.txt"):
    with open("logs/error.txt", "r") as error_file:
        error_lines = error_file.readlines()

    # Extract the line after "Failed on line:"
    failed_line = None
    for line in error_lines:
        if "Failed on line:" in line:
            failed_line = line.split("Failed on line:")[1].strip()
            break

    if failed_line:
        with open("logs/instructions.txt", "r") as instructions_file:
            instructions_lines = instructions_file.readlines()

        # Find the test number above the failed line
        for i, line in enumerate(instructions_lines):
            if failed_line in line:
                # Search backwards for the test number
                for j in range(i, -1, -1):
                    if instructions_lines[j].startswith("Test"):
                        test_number = instructions_lines[j].strip().split(":")[0]
                        test_results[test_number] = "FAILED"
                        break
                break

# Write test results to test_results.txt
with open("logs/test_results.txt", "w") as results_file:
    for test, result in test_results.items():
        results_file.write(f"{test}: {result}\n")