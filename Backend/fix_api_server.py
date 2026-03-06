#!/usr/bin/env python3
"""Script to fix api_server.py - remove duplicate API call code"""
import re
import os

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
api_server_path = os.path.join(script_dir, 'api_server.py')

with open(api_server_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the lines we need to fix
output_lines = []
skip_until_except = False
citations_line_found = False

for i, line in enumerate(lines):
    if 'Citations: {result.citations}' in line:
        citations_line_found = True
        output_lines.append(line)
        # Add the return statement after this line
        output_lines.append('\n')
        output_lines.append('        # Return structured response with proper domain and citations\n')
        output_lines.append('        return ChatResponse(\n')
        output_lines.append('            answer=result.answer,\n')
        output_lines.append('            confidence=result.confidence,\n')
        output_lines.append('            sources=result.sources,\n')
        output_lines.append('            methodology=result.methodology,\n')
        output_lines.append('            domain=result.domain.value,\n')
        output_lines.append('            citations=result.citations,\n')
        output_lines.append('            reasoning_steps=result.reasoning_steps,\n')
        output_lines.append('            disclaimer=result.disclaimer\n')
        output_lines.append('        )\n')
        output_lines.append('            \n')
        skip_until_except = True
        continue
    
    if skip_until_except:
        # Skip lines until we hit except Exception
        if 'except Exception as e:' in line:
            skip_until_except = False
            output_lines.append(line)
        continue
    
    output_lines.append(line)

# Write back
with open(api_server_path, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)
    
print(f'✅ Fixed {api_server_path} - removed duplicate API call code')
