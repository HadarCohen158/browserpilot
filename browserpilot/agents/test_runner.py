import shutil
import os
from browserpilot.agents.gpt_selenium_agent import GPTSeleniumAgent
from dotenv import load_dotenv

class TestRunner:
    def __init__(self, instructions_file, chromedriver_path):
        self.instructions_file = instructions_file
        self.chromedriver_path = chromedriver_path
        self.test_results = {}
        load_dotenv()

    def clear_logs_directory(self):
        """Clear existing logs directory."""
        if os.path.exists("logs"):
            shutil.rmtree("logs")
        os.makedirs("logs", exist_ok=True)

    def read_instructions(self):
        """Read test instructions from a file."""
        with open(self.instructions_file, "r") as file:
            return file.read()

    def initialize_test_results(self):
        """Initialize test results from the instructions file."""
        with open(self.instructions_file, "r") as file:
            for line in file:
                if line.startswith('print("Test'):
                    test_number = self.extract_test_number(line)
                    self.test_results[test_number] = "OK"

    @staticmethod
    def extract_test_number(line):
        """Extract the test number from a line."""
        return line.strip().split('("')[1].split('")')[0]

    def run_agent(self, instructions):
        """Run the Selenium agent with the provided instructions."""
        agent = GPTSeleniumAgent(instructions, self.chromedriver_path)
        try:
            agent.run()
        except Exception as e:
            self.log_error(e)

    @staticmethod
    def log_error(exception):
        """Log errors to the error.txt file."""
        with open("logs/error.txt", "a") as error_file:
            error_file.write(f"Problem Instruction: {exception}\n")

    def parse_test_results_from_instructions(self):
        """Parse test results from instructions file."""
        with open("logs/instructions.txt", "r") as instructions_file:
            instructions_lines = instructions_file.readlines()

        for line in instructions_lines:
            if 'print("Test' in line:
                test_number = self.extract_test_number(line)
                self.test_results[test_number] = "PASSED"

    def check_for_failed_tests(self):
        """Check if any tests failed and update their status."""
        if os.path.exists("logs/error.txt"):
            with open("logs/error.txt", "r") as error_file:
                error_lines = error_file.readlines()

            failed_line = self.extract_failed_line(error_lines)
            if failed_line:
                self.update_failed_test_status(failed_line)

    @staticmethod
    def extract_failed_line(error_lines):
        """Extract the failed line from the error file."""
        for line in error_lines:
            if "Failed on line:" in line:
                return line.split("Failed on line:")[1].strip()
        return None

    def update_failed_test_status(self, failed_line):
        """Update the test status to 'FAILED'."""
        with open("logs/instructions.txt", "r") as instructions_file:
            instructions_lines = instructions_file.readlines()

        for i, line in enumerate(instructions_lines):
            if failed_line in line:
                for j in range(i, -1, -1):
                    if 'print("Test' in instructions_lines[j]:
                        test_number = self.extract_test_number(instructions_lines[j])
                        self.test_results[test_number] = "FAILED"
                        break
                break

    def write_test_results(self):
        """Write the test results to a file."""
        with open("logs/test_results.txt", "w") as results_file:
            with open("logs/instructions.txt", "r") as instructions_file:
                instructions_lines = instructions_file.readlines()
                for line in instructions_lines:
                    if 'print("Test' in line:
                        test_number = self.extract_test_number(line)
                        results_file.write(f"{test_number}: {self.test_results[test_number]}\n")
