#!/bin/bash
# Script to run all admin flow tests
# Usage: ./run_all_admin_tests.sh

echo "========================================"
echo "Running All Admin Flow Tests"
echo "========================================"
echo ""

# Check if backend and frontend are running
echo "[INFO] Make sure backend (port 5000) and frontend (port 3000) are running"
echo ""

# Run all tests with detailed output
pytest tests/test_admin_flow.py -v -s --tb=short --html=reports/admin_flow_report.html --self-contained-html

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "All tests PASSED!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Some tests FAILED. Check the report above."
    echo "========================================"
fi

echo ""
echo "Report saved to: reports/admin_flow_report.html"
echo ""
