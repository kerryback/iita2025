import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 8)
ax.axis('off')

# Set light gray background
fig.patch.set_facecolor('lightgray')
ax.set_facecolor('lightgray')

# Node positions (remove DW)
nodes = {
    'User': (1, 4),
    'App': (5, 4),
    'LLM': (9, 4)
}

# Node colors
node_colors = {
    'User': 'lightyellow',
    'App': 'lightgreen',
    'LLM': 'lightyellow'
}

# Draw nodes as rounded rectangles
node_patches = {}
for name, (x, y) in nodes.items():
    # Single-line text for all nodes
    width = 1.5 if name == 'App' else 1.7
    height = 0.6
    rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.3",
                          facecolor=node_colors[name],
                          edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, name, ha='center', va='center', fontsize=18, fontweight='bold')
    node_patches[name] = rect

# Blue color for all arrows
color_blue = '#1E90FF'

# Helper function to create curved arrow with label
def draw_curved_arrow_with_label(ax, start, end, label, color, curve_height=0.5, above=True, stacked=False):
    x1, y1 = start
    x2, y2 = end

    # Create curved arrow using FancyArrowPatch with connectionstyle
    if abs(x1 - x2) > abs(y1 - y2):  # Horizontal arrow
        connectionstyle = f"arc3,rad={-0.3}"
    else:  # Vertical arrow
        connectionstyle = f"arc3,rad={0.3 if curve_height > 0 else -0.3}"

    arrow = FancyArrowPatch(start, end,
                           connectionstyle=connectionstyle,
                           arrowstyle='->',
                           color=color, linewidth=3.5,
                           mutation_scale=25,
                           zorder=1)
    ax.add_patch(arrow)

    # Add label
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    if abs(x1 - x2) > abs(y1 - y2):  # Horizontal
        label_x = mid_x
        # Increase vertical offset for better separation
        label_y = mid_y + (0.8 if above else -0.8)
    else:  # Vertical
        label_x = mid_x + (curve_height * 0.8 if curve_height > 0 else -curve_height * 0.8)
        label_y = mid_y

    if stacked and isinstance(label, list):
        # For stacked labels, increase spacing to prevent overlap
        # Stack from top to bottom: Prompt, System Prompt, Chat History, RAG Chunks
        for i, line in enumerate(label):
            if i == 0:  # First item (Prompt) - highest
                offset_y = 1.35
            elif i == 1:  # Second item (System Prompt) - second
                offset_y = 0.9
            elif i == 2:  # Third item (Chat History) - third
                offset_y = 0.45
            else:  # Fourth item (RAG Chunks) - lowest (at base position)
                offset_y = 0
            ax.text(label_x, label_y + offset_y, line, ha='center', va='center',
                    fontsize=14, color='black', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    else:
        ax.text(label_x, label_y, label, ha='center', va='center',
                fontsize=14, color='black', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Draw arrows with labels
# 1. User -> App (above) - "Prompt"
draw_curved_arrow_with_label(ax, (nodes['User'][0] + 1.1, nodes['User'][1] + 0.2),
                            (nodes['App'][0] - 1, nodes['App'][1] + 0.2),
                            'Prompt', color_blue, curve_height=0.6, above=True)

# 2. App -> LLM (above) - stacked labels
draw_curved_arrow_with_label(ax, (nodes['App'][0] + 1.0, nodes['App'][1] + 0.2),
                            (nodes['LLM'][0] - 1.1, nodes['LLM'][1] + 0.2),
                            ['Prompt', 'System Prompt', 'Chat History', 'RAG Chunks'], color_blue, curve_height=0.4, above=True, stacked=True)

# 3. LLM -> App (below) - "Response"
draw_curved_arrow_with_label(ax, (nodes['LLM'][0] - 1.1, nodes['LLM'][1] - 0.2),
                            (nodes['App'][0] + 1, nodes['App'][1] - 0.2),
                            'Response', color_blue, curve_height=0.6, above=False)

# 4. App -> User (below) - "Response"
draw_curved_arrow_with_label(ax, (nodes['App'][0] - 1, nodes['App'][1] - 0.2),
                            (nodes['User'][0] + 1.1, nodes['User'][1] - 0.2),
                            'Response', color_blue, curve_height=0.5, above=False)

# Save the figure
plt.tight_layout()
plt.savefig('chatbot.png', dpi=300, bbox_inches='tight',
            facecolor='lightgray', edgecolor='none')
print("Chatbot diagram created as chatbot.png")
plt.close()