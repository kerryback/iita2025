import graphviz

# Create a new directed graph using neato for precise positioning
dot = graphviz.Digraph(comment='AI Learning Progression', format='png', engine='neato')

# Set graph attributes - increased width for more white background
dot.attr(size='18,12', dpi='300', splines='ortho')
dot.attr('node', shape='oval', style='filled', fontname='Arial', fontsize='32',
         width='6', height='1.5', fixedsize='true')
dot.attr('edge', fontname='Arial')


# Define positions for main nodes (x,y coordinates)
# New node above Vibe Coding
dot.node('PE', 'Prompt Engineering', fillcolor='white', pos='3,12!')
# Vibe Coding and Financial Analysis horizontally aligned
dot.node('VC', 'Vibe Coding', fillcolor='lightblue', pos='3,10!')
dot.node('FA', 'Financial Analysis', fillcolor='lightgreen', pos='10,10!')

# Other nodes below Vibe Coding
dot.node('Apps', 'Apps', fillcolor='lightyellow', pos='3,8!')
dot.node('CC', 'Custom Chatbots', fillcolor='lightcoral', pos='3,6!')
dot.node('AA', 'AI Agents', fillcolor='lightpink', pos='3,4!')


# Main progression arrows
# New arrow from Prompt Engineering to Vibe Coding
dot.edge('PE', 'VC', color='blue', penwidth='2.5')
# Horizontal arrow from Vibe Coding to Financial Analysis
dot.edge('VC', 'FA', color='black', penwidth='4')
# Vertical arrow from Vibe Coding to Apps
dot.edge('VC', 'Apps', color='blue', penwidth='2.5')
# Continue vertical progression
dot.edge('Apps', 'CC', color='blue', penwidth='2.5')
dot.edge('CC', 'AA', color='blue', penwidth='2.5')

# Create invisible nodes for the return path
# All right nodes at exactly x=10 (center of Financial Analysis) for perfect vertical alignment
dot.attr('node', shape='point', width='0.01', height='0.01', style='invis')

dot.node('Apps_right', '', pos='10,8!')
dot.node('CC_right', '', pos='10,6!')
dot.node('AA_right', '', pos='10,4!')

# Horizontal lines extending right from each oval to center of Financial Analysis
dot.edge('Apps', 'Apps_right', color='black', penwidth='4', dir='none')
dot.edge('CC', 'CC_right', color='black', penwidth='4', dir='none')
dot.edge('AA', 'AA_right', color='black', penwidth='4', dir='none')

# Single vertical line from AI Agents level up to Financial Analysis (with arrow)
dot.edge('AA_right', 'CC_right', color='black', penwidth='4', dir='none')
dot.edge('CC_right', 'Apps_right', color='black', penwidth='4', dir='none')
dot.edge('Apps_right', 'FA', color='black', penwidth='4')

# Save the diagram under a new name
dot.render('ai_learning_progression_with_prompt', directory='.', cleanup=True)
print("Diagram created as ai_learning_progression_with_prompt.png")