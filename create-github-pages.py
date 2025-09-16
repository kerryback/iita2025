#!/usr/bin/env python3
"""
Script to create GitHub Pages deployment from presentation files.
Builds both 3:2 and 16:9 versions and deploys to docs/ folder with custom filenames.
"""

import re
import subprocess
import sys
import shutil
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
    """Render both presentation versions with custom output names directly in docs folder"""

    # Ensure docs folder exists
    Path("docs").mkdir(exist_ok=True)

    # Define source files and their target names (without .html extension for quarto)
    render_configs = [
        ("index.qmd", "slides3x2"),
        ("index-16x9.qmd", "slides16x9")
    ]

    for qmd_file, target_name in render_configs:
        if not Path(qmd_file).exists():
            print(f"Warning: {qmd_file} not found, skipping...")
            continue

        print(f"\nRendering {qmd_file} -> docs/{target_name}.html...")
        try:
            # Create a temporary qmd file with the target name in docs folder
            temp_qmd = Path("docs") / f"{target_name}.qmd"
            shutil.copy2(qmd_file, temp_qmd)

            # Change to docs directory and render there
            original_cwd = Path.cwd()

            try:
                import os
                os.chdir("docs")

                result = subprocess.run(
                    ["quarto", "render", f"{target_name}.qmd"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                print(f"+ Successfully created docs/{target_name}.html")

                # Show any warnings
                if result.stderr and "WARNING" in result.stderr:
                    warnings = [line for line in result.stderr.split('\n') if 'WARNING' in line]
                    for warning in warnings[:3]:  # Show first 3 warnings
                        print(f"  ! {warning}")

            finally:
                # Always change back to original directory
                os.chdir(str(original_cwd))

                # Clean up temporary qmd file
                if temp_qmd.exists():
                    temp_qmd.unlink()

        except subprocess.CalledProcessError as e:
            print(f"- Error rendering {qmd_file}:")
            print(f"   {e.stderr}")
            return False
        except FileNotFoundError:
            print("- Error: 'quarto' command not found. Make sure Quarto is installed and in PATH.")
            return False

    return True

def copy_assets():
    """Copy all necessary assets to docs folder"""

    print("\nCopying assets to docs folder...")

    # List of file patterns to copy
    asset_patterns = [
        "*.css",
        "*.html",  # theme-toggle.html, fireworks-setup.html
        "*.js",
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.gif",
        "*.svg"
    ]

    copied_files = []

    for pattern in asset_patterns:
        for file_path in Path(".").glob(pattern):
            # Skip the main HTML files as they're handled separately
            if file_path.name in ["index.html", "index-16x9.html"]:
                continue

            target_path = Path("docs") / file_path.name
            try:
                shutil.copy2(file_path, target_path)
                copied_files.append(file_path.name)
            except Exception as e:
                print(f"  ! Warning: Could not copy {file_path.name}: {e}")

    if copied_files:
        print(f"+ Copied {len(copied_files)} asset files")
    else:
        print("  No additional assets found to copy")

    # Note: reveal.js dependencies will be created automatically when rendering in docs/

    return True

def create_landing_page():
    """Create a landing page with links to both presentation versions"""

    landing_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incorporating AI into Teaching and Teaching about AI - FMA 2025</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }

        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.2em;
            font-weight: 300;
        }

        .subtitle {
            text-align: center;
            margin-bottom: 40px;
            font-size: 1.2em;
            opacity: 0.9;
        }

        .version-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 40px 0;
        }

        .version-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }

        .version-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }

        .version-card.default {
            border-color: #ffd700;
            background: rgba(255, 215, 0, 0.1);
        }

        .version-title {
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 15px;
        }

        .version-desc {
            margin-bottom: 25px;
            opacity: 0.9;
            line-height: 1.5;
        }

        .btn {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .btn:hover {
            background: linear-gradient(45deg, #ee5a24, #ff6b6b);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
            text-decoration: none;
            color: white;
        }

        .btn.default {
            background: linear-gradient(45deg, #ffd700, #ffb700);
            color: #333;
        }

        .btn.default:hover {
            background: linear-gradient(45deg, #ffb700, #ffd700);
            color: #333;
        }

        .default-badge {
            background: #ffd700;
            color: #333;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            margin-bottom: 15px;
            display: inline-block;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            opacity: 0.7;
            font-size: 0.9em;
        }

        @media (max-width: 600px) {
            .version-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Incorporating AI into Teaching and Teaching about AI</h1>
        <div class="subtitle">Kerry Back • Rice University • FMA 2025</div>

        <div class="version-grid">
            <div class="version-card">
                <div class="version-title">Standard Version (3:2)</div>
                <div class="version-desc">
                    Optimized for traditional projectors and most conference rooms.
                    Best compatibility with older projection systems.
                </div>
                <a href="slides3x2.html" class="btn">View Presentation</a>
            </div>

            <div class="version-card">
                <div class="version-title">Widescreen Version (16:9)</div>
                <div class="version-desc">
                    Perfect for modern widescreen projectors and displays.
                    Enhanced viewing experience on newer systems.
                </div>
                <a href="slides16x9.html" class="btn">View Presentation</a>
            </div>
        </div>

        <div class="footer">
            Choose the version that matches your projector's aspect ratio for the best viewing experience.
        </div>
    </div>
</body>
</html>"""

    landing_path = Path("docs") / "index.html"
    landing_path.write_text(landing_html, encoding='utf-8')
    print("+ Created landing page at docs/index.html")

    return True

def create_cname_file():
    """Create CNAME file for custom domain"""

    cname_path = Path("docs") / "CNAME"
    cname_path.write_text("fma2025.kerryback.com\n", encoding='utf-8')
    print("+ Created CNAME file for fma2025.kerryback.com")

    return True

def main():
    """Main function to create GitHub Pages deployment"""

    print("Creating GitHub Pages deployment...")
    print("=" * 50)

    # Ensure docs folder exists
    docs_path = Path("docs")
    docs_path.mkdir(exist_ok=True)

    # Create the 16:9 version
    if not create_16x9_version():
        return 1

    # Render both versions
    if not render_presentations():
        return 1

    # Copy assets
    if not copy_assets():
        return 1

    # Create landing page
    if not create_landing_page():
        return 1

    # Create CNAME file
    if not create_cname_file():
        return 1

    print("\n" + "=" * 50)
    print("Success! GitHub Pages deployment ready:")
    print("   * docs/index.html         - Landing page with both versions")
    print("   * docs/slides3x2.html     - Standard 3:2 ratio (default)")
    print("   * docs/slides16x9.html    - Widescreen 16:9 ratio")
    print("   * docs/CNAME              - Custom domain configuration")
    print(f"   * docs/                   - All assets copied")
    print("\nNext steps:")
    print("   1. Commit and push to GitHub")
    print("   2. Enable GitHub Pages from docs/ folder in repo settings")
    print("   3. Configure DNS for fma2025.kerryback.com to point to GitHub Pages")

    return 0

if __name__ == "__main__":
    sys.exit(main())