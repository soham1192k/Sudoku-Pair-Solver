#!/bin/bash
python3 generate_encoding.py 
minisat encoding_CNF.txt solution.txt>/dev/null 2>/dev/null
python3 generate_output.py