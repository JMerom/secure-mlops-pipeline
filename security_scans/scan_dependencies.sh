#!/usr/bin/env bash
set -euo pipefail

echo "Running dependency vulnerability scan with pip-audit..."
pip-audit -r requirements.txt -f markdown > reports/dependency_report.md

echo "Dependency scan complete. Report written to reports/dependency_report.md"
