#!/usr/bin/env python3
"""Kept for convenience: runs the current generator (generate.py)."""
import os, runpy
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generate.py'), run_name='__main__')
