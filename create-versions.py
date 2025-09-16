#!/usr/bin/env python3
"""
Script to create and render multiple presentation versions with different aspect ratios.
Reads index.qmd (3:2 ratio) and creates index-16x9.qmd (16:9 ratio), then renders both.
"""

import re
import subprocess
import sys
from pathlib import Path

def create_16x9_version():
    """Create 16:9 version from the original index.qmd"""

    # Read the original file
    original_file = Path("index.qmd")
    if not original_file.exists():
        print("Error: index.qmd not found!")
        return False

    print("Reading original index.qmd...")
    content = original_file.read_text(encoding='utf-8')

    # Replace the format section to use 16:9 dimensions
    # Look for the YAML front matter and update width/height
    yaml_pattern = r'(format:\s*\n\s*revealjs:.*?)\n---'

    def replace_format(match):
        yaml_content = match.group(1)

        # Add width and height settings (or replace if they exist)
        if 'width:' in yaml_content:
            yaml_content = re.sub(r'width:\s*\d+', 'width: 1280', yaml_content)
        else:
            yaml_content += '\n    width: 1280'

        if 'height:' in yaml_content:
            yaml_content = re.sub(r'height:\s*\d+', 'height: 720', yaml_content)
        else:
            yaml_content += '\n    height: 720'

        return yaml_content + '\n---'

    # Apply the replacement
    new_content = re.sub(yaml_pattern, replace_format, content, flags=re.DOTALL)

    # If no format section was found, we need to add the dimensions
    if new_content == content:
        # Insert width/height after the revealjs line
        revealjs_pattern = r'(\s*revealjs:\s*\n)'
        replacement = r'\1    width: 1280\n    height: 720\n'
        new_content = re.sub(revealjs_pattern, replacement, content)

    # Write the 16:9 version
    output_file = Path("index-16x9.qmd")
    output_file.write_text(new_content, encoding='utf-8')

    print(f"+ Created {output_file}")
    return True

def render_presentations():
    """Render both presentation versions"""
    files_to_render = ["index.qmd", "index-16x9.qmd"]

    for qmd_file in files_to_render:
        if not Path(qmd_file).exists():
            print(f"Warning: {qmd_file} not found, skipping...")
            continue

        print(f"\nRendering {qmd_file}...")
        try:
            result = subprocess.run(
                ["quarto", "render", qmd_file],
                capture_output=True,
                text=True,
                check=True
            )

            # Determine output HTML file name
            html_file = qmd_file.replace('.qmd', '.html')
            print(f"+ Successfully rendered {html_file}")

            # Show any warnings
            if result.stderr and "WARNING" in result.stderr:
                warnings = [line for line in result.stderr.split('\n') if 'WARNING' in line]
                for warning in warnings[:3]:  # Show first 3 warnings
                    print(f"  ! {warning}")

        except subprocess.CalledProcessError as e:
            print(f"- Error rendering {qmd_file}:")
            print(f"   {e.stderr}")
            return False
        except FileNotFoundError:
            print("- Error: 'quarto' command not found. Make sure Quarto is installed and in PATH.")
            return False

    return True

def main():
    """Main function to create versions and render both"""
    print("Creating multiple presentation versions...")
    print("=" * 50)

    # Create the 16:9 version
    if not create_16x9_version():
        return 1

    # Render both versions
    print("\nRendering presentations...")
    if not render_presentations():
        return 1

    print("\n" + "=" * 50)
    print("Success! Created two versions:")
    print("   * index.html      - Original 3:2 ratio (1050x700)")
    print("   * index-16x9.html - Widescreen 16:9 ratio (1280x720)")
    print("\nChoose the appropriate version for your projector!")

    return 0

if __name__ == "__main__":
    sys.exit(main())