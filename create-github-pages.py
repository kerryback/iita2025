#!/usr/bin/env python3
"""
Script to create GitHub Pages deployment from presentation files.
Creates both 3:2 and 16:9 versions and renders everything to docs/ folder.
"""

import re
import subprocess
import sys
import shutil
from pathlib import Path

def create_16x9_version():
    """Create 16:9 version from the 3:2 presentation"""

    # Source and target files
    source_file = Path("docs/slides3x2.qmd")
    target_file = Path("docs/slides16x9.qmd")

    if not source_file.exists():
        print(f"Error: {source_file} not found!")
        return False

    print(f"Creating 16:9 version from {source_file}...")
    content = source_file.read_text(encoding='utf-8')

    # Replace the format section to use 16:9 dimensions
    # Look for existing width/height settings and update them
    if 'width:' in content and 'height:' in content:
        # Replace existing dimensions
        content = re.sub(r'width:\s*\d+', 'width: 1280', content)
        content = re.sub(r'height:\s*\d+', 'height: 720', content)
    else:
        # Add dimensions after revealjs: line
        content = re.sub(
            r'(format:\s*\n\s*revealjs:\s*\n)',
            r'\1    width: 1280\n    height: 720\n',
            content
        )

    # Write the 16:9 version
    target_file.write_text(content, encoding='utf-8')
    print(f"+ Created {target_file}")
    return True

def render_presentations():
    """Render all presentation files"""

    files_to_render = [
        ("index.qmd", "Landing page"),
        ("docs/slides3x2.qmd", "3:2 presentation"),
        ("docs/slides16x9.qmd", "16:9 presentation")
    ]

    for qmd_file, description in files_to_render:
        if not Path(qmd_file).exists():
            print(f"Warning: {qmd_file} not found, skipping...")
            continue

        print(f"\nRendering {description} ({qmd_file})...")
        try:
            result = subprocess.run(
                ["quarto", "render", qmd_file],
                capture_output=True,
                text=True,
                check=True
            )

            print(f"+ Successfully rendered {qmd_file}")

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

def create_cname_file():
    """Create CNAME file for custom domain"""

    cname_path = Path("docs/CNAME")
    cname_path.write_text("fma2025.kerryback.com\n", encoding='utf-8')
    print("+ Created CNAME file for fma2025.kerryback.com")
    return True

def commit_and_push():
    """Commit all changes and push to GitHub"""

    print("\nCommitting changes...")
    try:
        # Add all files
        result = subprocess.run(
            ["git", "add", "."],
            capture_output=True,
            text=True,
            check=True
        )

        # Commit
        commit_message = """Create clean GitHub Pages structure with proper landing page

- Move presentation to docs/slides3x2.qmd
- Create index.qmd as landing page that renders to docs/
- Add _quarto.yml for project configuration
- Generate slides16x9.qmd with 16:9 dimensions
- Render all files properly with correct dependency paths
- Add CNAME for custom domain

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""

        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True,
            check=True
        )

        print("+ Committed changes")

        # Push
        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True,
            check=True
        )

        print("+ Pushed to GitHub")
        return True

    except subprocess.CalledProcessError as e:
        print(f"- Git error: {e.stderr}")
        return False

def main():
    """Main function to create GitHub Pages deployment"""

    print("Creating GitHub Pages deployment with clean structure...")
    print("=" * 60)

    # Ensure docs folder exists
    Path("docs").mkdir(exist_ok=True)

    # Create the 16:9 version
    if not create_16x9_version():
        return 1

    # Create CNAME file
    if not create_cname_file():
        return 1

    # Render all presentations
    if not render_presentations():
        return 1

    # Commit and push
    if not commit_and_push():
        return 1

    print("\n" + "=" * 60)
    print("Success! GitHub Pages deployment ready:")
    print("   * docs/index.html         - Landing page")
    print("   * docs/slides3x2.html     - Standard 3:2 ratio")
    print("   * docs/slides16x9.html    - Widescreen 16:9 ratio")
    print("   * docs/CNAME              - Custom domain configuration")
    print("\nStructure:")
    print("   * index.qmd               - Landing page source")
    print("   * docs/slides3x2.qmd      - 3:2 presentation source")
    print("   * docs/slides16x9.qmd     - 16:9 presentation source")
    print("   * _quarto.yml             - Project configuration")
    print("\nYour site should be live at: https://fma2025.kerryback.com")

    return 0

if __name__ == "__main__":
    sys.exit(main())