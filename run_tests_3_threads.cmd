@echo off
echo Running tests in 3 threads...
pytest -n 3 -v --tb=short
pause
