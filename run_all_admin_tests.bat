@echo off
REM Script to run all admin flow tests
REM Usage: run_all_admin_tests.bat

echo ========================================
echo Running All Admin Flow Tests
echo ========================================
echo.

REM Check if backend and frontend are running
echo [INFO] Make sure backend (port 5000) and frontend (port 3000) are running
echo.

REM Run all tests with detailed output
pytest tests/test_admin_flow.py -v -s --tb=short --html=reports/admin_flow_report.html --self-contained-html

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo All tests PASSED!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Some tests FAILED. Check the report above.
    echo ========================================
)

echo.
echo Report saved to: reports/admin_flow_report.html
echo.
pause
