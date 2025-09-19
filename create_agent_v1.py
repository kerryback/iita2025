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

# Node positions
nodes = {
    'User': (1, 4),
    'Agent': (5, 4),
    'LLM': (9, 4),
    'DW': (5, 1)
}

# Node colors
node_colors = {
    'User': 'lightyellow',
    'Agent': 'lightgreen',
    'LLM': 'lightyellow',
    'DW': 'lightyellow'
}

# Draw nodes as rounded rectangles
node_patches = {}
for name, (x, y) in nodes.items():
    if name == 'DW':
        # Two-line text for Data Warehouse
        width, height = 2.0, 0.8
        rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                              boxstyle="round,pad=0.3",
                              facecolor=node_colors[name],
                              edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y + 0.15, 'Data', ha='center', va='center', fontsize=18, fontweight='bold')
        ax.text(x, y - 0.2, 'Warehouse', ha='center', va='center', fontsize=18, fontweight='bold')
    else:
        # Single-line text for other nodes
        width = 1.5 if name == 'Agent' else 1.7
        height = 0.6
        rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                              boxstyle="round,pad=0.3",
                              facecolor=node_colors[name],
                              edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, name, ha='center', va='center', fontsize=18, fontweight='bold')
    node_patches[name] = rect

# Three color scheme
color1 = '#1E90FF'  # Blue for steps 1 & 2
color2 = '#32CD32'  # Green for steps 3 & 4
color3 = '#FF6347'  # Red/Tomato for steps 5 & 6

# Add blue arrows only (User -> Agent and Agent -> LLM)
# User -> Agent (curved upward blue arrow - negative rad for upward curve)
arrow_user_app = FancyArrowPatch((nodes['User'][0] + 1, nodes['User'][1]+0.3),
                                 (nodes['Agent'][0] - 1.0, nodes['Agent'][1]+0.3),
                                 #connectionstyle="arc3,rad=-0.4",
                                 arrowstyle='->',
                                 color=color1, linewidth=3.5, mutation_scale=25, zorder=0, alpha=0.6)
ax.add_patch(arrow_user_app)

# Agent -> LLM (curved upward blue arrow - negative rad for upward curve)
arrow_app_llm = FancyArrowPatch((nodes['Agent'][0] + 1.0, nodes['Agent'][1]+0.3),
                                (nodes['LLM'][0] - 1.1, nodes['LLM'][1]+0.3),
                                #connectionstyle="arc3,rad=-0.4",
                                arrowstyle='->',
                                color=color1, linewidth=3.5, mutation_scale=25, zorder=0, alpha=0.6)
ax.add_patch(arrow_app_llm)

# Create legend
legend_elements = [
    mpatches.Patch(color=color1, label='Step 1: Prompt/System Prompt'),
    mpatches.Patch(color=color2, label='Step 2: SQL Query'),
    mpatches.Patch(color=color3, label='Step 3: Data Response')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=16, frameon=True, fancybox=True, shadow=True)

# Save the figure
plt.tight_layout()
plt.savefig('docs/images/agent_v1.png', dpi=300, bbox_inches='tight',
            facecolor='lightgray', edgecolor='none')
print("First version created as docs/images/agent_v1.png")
plt.close()