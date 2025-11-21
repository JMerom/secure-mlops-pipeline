#!/usr/bin/env bash
set -euo pipefail

echo "Running Bandit security scan..."
bandit -r . -f txt -o reports/bandit_report.txt

echo "Bandit scan complete. Report written to reports/bandit_report.txt"
