"""
Test runner script for the Cartouche Bot Service.
Runs all tests and generates a comprehensive report.
"""

import os
import sys
import asyncio
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()


def run_test_script(script_path):
    """Run a test script and return the result."""
    logger.info(f"Running test script: {script_path}")

    try:
        result = subprocess.run(
            [sys.executable, script_path], capture_output=True, text=True, check=False
        )

        # Log output
        if result.stdout:
            logger.info(f"Test output: {result.stdout}")
        if result.stderr:
            logger.error(f"Test errors: {result.stderr}")

        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to run test script {script_path}: {str(e)}")
        return False


def run_all_tests():
    """Run all test scripts and generate a report."""
    logger.info("Starting all tests...")

    # Create test results directory
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)

    # Define test scripts
    test_scripts = ["tests/test_core.py", "tests/test_api.py", "tests/test_e2e.py"]

    # Run tests
    results = {}
    for script in test_scripts:
        script_name = os.path.basename(script)
        results[script_name] = run_test_script(script)

    # Log results
    logger.info("Test results:")
    for script_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        logger.info(f"  {script_name}: {status}")

    # Generate report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = results_dir / f"test_report_{timestamp}.txt"

    with open(report_path, "w") as f:
        f.write(f"Cartouche Bot Service Test Report - {datetime.now().isoformat()}\n")
        f.write("=" * 70 + "\n\n")

        f.write("Test Results Summary:\n")
        f.write("-" * 30 + "\n")

        all_passed = True
        for script_name, result in results.items():
            status = "PASSED" if result else "FAILED"
            f.write(f"{script_name}: {status}\n")
            all_passed = all_passed and result

        f.write("\n")
        f.write(f"Overall Status: {'PASSED' if all_passed else 'FAILED'}\n")
        f.write("\n")

        # Add individual test results
        f.write("Detailed Test Results:\n")
        f.write("-" * 30 + "\n")

        for result_file in results_dir.glob("*_results_*.txt"):
            f.write(f"\n--- {result_file.name} ---\n\n")
            with open(result_file, "r") as rf:
                f.write(rf.read())
            f.write("\n")

    logger.info(f"Test report generated: {report_path}")

    return all_passed, report_path


if __name__ == "__main__":
    # Run all tests
    success, report_path = run_all_tests()

    # Print report path
    print(f"Test report: {report_path}")

    # Exit with appropriate code
    sys.exit(0 if success else 1)
