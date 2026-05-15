@echo off
echo Running tests in 1 thread...
pytest -n 1 -v --tb=short
pause
