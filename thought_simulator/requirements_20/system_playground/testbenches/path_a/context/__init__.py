"""
Context subsystem package for system_playground testbenches.

Holds dual-mode progressive testbenches for:
- COB (Conversation Object Basin)
- CIL
- CST-Core / CST-MS / CST-Mux

Do not eager-import testbench modules here; progressive runner imports
concrete modules by full path (e.g. ...context.cob_testbench).
"""
