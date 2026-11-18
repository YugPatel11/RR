import json
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.join(OUT_DIR, 'results.json')
template_path = os.path.join(OUT_DIR, 'index_template.html')
html_path = os.path.join(OUT_DIR, 'index.html')

with open(results_path, 'r', encoding='utf-8') as f:
    results_json = f.read()

# Also read the template
with open(template_path, 'r', encoding='utf-8') as f:
    template_content = f.read()

# Replace placeholder
if 'INJECTED_DATA_PLACEHOLDER' in template_content:
    final_html = template_content.replace('INJECTED_DATA_PLACEHOLDER', results_json)
else:
    print("Warning: INJECTED_DATA_PLACEHOLDER not found in template!")
    final_html = template_content

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Successfully generated {html_path} ({len(final_html)} bytes)")

