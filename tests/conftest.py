import sys
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
sys.path.insert(0, str(EXAMPLES))


import subprocess  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture
def run_example():
    def run(script, *args):
        result = subprocess.run([sys.executable, script, *args], cwd=EXAMPLES,
                                capture_output=True, text=True, check=True)
        return result.stdout
    return run
