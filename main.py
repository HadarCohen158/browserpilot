from browserpilot.agents.test_runner import TestRunner
from dotenv import load_dotenv


def main():

    load_dotenv()

    # Initialize test runner
    test_runner = TestRunner(instructions_file="tests.txt", chromedriver_path="/path/to/chromedriver")

    # Clear previous logs
    test_runner.clear_logs_directory()

    # Read the instructions
    instructions = test_runner.read_instructions()

    # Initialize the test results as "OK"
    test_runner.initialize_test_results()

    # Run the agent
    test_runner.run_agent(instructions)

    # Parse results from instructions
    test_runner.parse_test_results_from_instructions()

    # Check for failed tests
    test_runner.check_for_failed_tests()

    # Write final test results
    test_runner.write_test_results()


if __name__ == "__main__":
    main()