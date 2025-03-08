import streamlit as st
import networkx as nx
from pyvis.network import Network
import json
from pathlib import Path

# Set page config
st.set_page_config(page_title="Python Learning RPG Map", layout="wide")

# Define the learning path data structure with sub-nodes
PYTHON_TOPICS = {
    # Beginner's Valley (Foundation Zone)
    "basics_intro": {
        "title": "Welcome to Python",
        "description": "Your first steps into Python programming.",
        "topics": ["Installation", "Python REPL", "First Program", "Text Editor Setup"],
        "resources": ["Python.org Setup Guide", "VS Code Setup", "Hello World Tutorial"],
        "difficulty": "Beginner",
        "xp_reward": 100,
        "estimated_hours": 2,
        "color": "#4CAF50",
        "zone": "Beginner's Valley"
    },
    "basics_syntax": {
        "title": "Basic Syntax",
        "description": "Learn the fundamental syntax of Python.",
        "topics": ["Indentation", "Comments", "Print Statements", "Basic Operators"],
        "resources": ["Python Style Guide", "Basic Syntax Tutorial"],
        "difficulty": "Beginner",
        "xp_reward": 150,
        "estimated_hours": 3,
        "color": "#4CAF50",
        "zone": "Beginner's Valley"
    },
    "variables_basic": {
        "title": "Variables I",
        "description": "Understanding variables and basic data types.",
        "topics": ["Numbers", "Strings", "Basic Operations", "Type Checking"],
        "resources": ["Variable Tutorial", "Data Types Guide"],
        "difficulty": "Beginner",
        "xp_reward": 200,
        "estimated_hours": 4,
        "color": "#4CAF50",
        "zone": "Beginner's Valley"
    },
    "strings_basic": {
        "title": "Strings I",
        "description": "Working with text in Python.",
        "topics": ["String Creation", "Concatenation", "Basic Methods", "Formatting"],
        "resources": ["String Basics", "String Operations"],
        "difficulty": "Beginner",
        "xp_reward": 200,
        "estimated_hours": 4,
        "color": "#4CAF50",
        "zone": "Beginner's Valley"
    },
    "numbers_basic": {
        "title": "Numbers & Math",
        "description": "Mathematical operations and number types.",
        "topics": ["Integers", "Floats", "Math Operations", "Math Module"],
        "resources": ["Python Math Guide", "Number Operations"],
        "difficulty": "Beginner",
        "xp_reward": 200,
        "estimated_hours": 4,
        "color": "#4CAF50",
        "zone": "Beginner's Valley"
    },
    "variables_advanced": {
        "title": "Variables II",
        "description": "Advanced variable concepts and type conversion.",
        "topics": ["Type Conversion", "Complex Types", "Memory Management", "Scope"],
        "resources": ["Advanced Variables", "Type System Deep Dive"],
        "difficulty": "Beginner+",
        "xp_reward": 250,
        "estimated_hours": 5,
        "color": "#81C784",
        "zone": "Beginner's Valley"
    },

    # Control Flow Kingdom
    "conditionals_basic": {
        "title": "Conditionals I",
        "description": "Making decisions in your code.",
        "topics": ["if Statements", "else Clauses", "elif Statements", "Comparison Operators"],
        "resources": ["Control Flow Basics", "Conditional Logic"],
        "difficulty": "Beginner",
        "xp_reward": 250,
        "estimated_hours": 5,
        "color": "#7E57C2",
        "zone": "Control Flow Kingdom"
    },
    "loops_basic": {
        "title": "Loops I",
        "description": "Basic iteration and loops.",
        "topics": ["for Loops", "while Loops", "Loop Control", "range() Function"],
        "resources": ["Loop Basics", "Iteration Guide"],
        "difficulty": "Beginner",
        "xp_reward": 250,
        "estimated_hours": 5,
        "color": "#7E57C2",
        "zone": "Control Flow Kingdom"
    },
    "conditionals_advanced": {
        "title": "Conditionals II",
        "description": "Advanced conditional logic and boolean operations.",
        "topics": ["Boolean Logic", "Truth Tables", "Short-Circuit Evaluation", "Conditional Expressions"],
        "resources": ["Advanced Conditionals", "Boolean Operations"],
        "difficulty": "Beginner+",
        "xp_reward": 300,
        "estimated_hours": 6,
        "color": "#9575CD",
        "zone": "Control Flow Kingdom"
    },
    "loops_advanced": {
        "title": "Loops II",
        "description": "Advanced looping techniques.",
        "topics": ["Nested Loops", "Loop Else", "Comprehensions Intro", "Iteration Patterns"],
        "resources": ["Advanced Loops", "Loop Patterns"],
        "difficulty": "Beginner+",
        "xp_reward": 300,
        "estimated_hours": 6,
        "color": "#9575CD",
        "zone": "Control Flow Kingdom"
    },

    # Data Structure Plains
    "lists_basic": {
        "title": "Lists I",
        "description": "Introduction to Python lists.",
        "topics": ["Creating Lists", "Indexing", "Basic Methods", "List Operations"],
        "resources": ["List Tutorial", "List Operations Guide"],
        "difficulty": "Beginner",
        "xp_reward": 200,
        "estimated_hours": 4,
        "color": "#2196F3",
        "zone": "Data Structure Plains"
    },
    "lists_methods": {
        "title": "Lists II",
        "description": "Working with list methods and operations.",
        "topics": ["List Methods", "Sorting", "Copying", "Nested Lists"],
        "resources": ["List Methods Guide", "List Operations Advanced"],
        "difficulty": "Beginner+",
        "xp_reward": 250,
        "estimated_hours": 5,
        "color": "#2196F3",
        "zone": "Data Structure Plains"
    },
    "lists_advanced": {
        "title": "Lists III",
        "description": "Advanced list operations and comprehensions.",
        "topics": ["List Comprehensions", "Slicing", "Advanced Methods", "Memory Efficiency"],
        "resources": ["Advanced List Operations", "List Comprehension Guide"],
        "difficulty": "Intermediate",
        "xp_reward": 300,
        "estimated_hours": 6,
        "color": "#64B5F6",
        "zone": "Data Structure Plains"
    },
    "tuples_basic": {
        "title": "Tuples",
        "description": "Understanding immutable sequences.",
        "topics": ["Tuple Creation", "Tuple Methods", "Immutability", "Named Tuples"],
        "resources": ["Tuple Guide", "Immutable Sequences"],
        "difficulty": "Beginner+",
        "xp_reward": 250,
        "estimated_hours": 4,
        "color": "#2196F3",
        "zone": "Data Structure Plains"
    },
    "dict_basic": {
        "title": "Dictionaries I",
        "description": "Working with Python dictionaries.",
        "topics": ["Dict Creation", "Key-Value Pairs", "Basic Methods", "Dict Operations"],
        "resources": ["Dictionary Basics", "Dictionary Methods Guide"],
        "difficulty": "Beginner+",
        "xp_reward": 250,
        "estimated_hours": 5,
        "color": "#2196F3",
        "zone": "Data Structure Plains"
    },
    "dict_advanced": {
        "title": "Dictionaries II",
        "description": "Advanced dictionary concepts and patterns.",
        "topics": ["Dict Comprehensions", "DefaultDict", "Counter", "ChainMap"],
        "resources": ["Advanced Dict Operations", "Collections Module"],
        "difficulty": "Intermediate",
        "xp_reward": 300,
        "estimated_hours": 6,
        "color": "#64B5F6",
        "zone": "Data Structure Plains"
    },
    "sets_basic": {
        "title": "Sets",
        "description": "Understanding Python sets.",
        "topics": ["Set Creation", "Set Operations", "Set Methods", "Frozen Sets"],
        "resources": ["Set Tutorial", "Set Operations Guide"],
        "difficulty": "Beginner+",
        "xp_reward": 250,
        "estimated_hours": 4,
        "color": "#2196F3",
        "zone": "Data Structure Plains"
    },

    # Function Fields
    "functions_basic": {
        "title": "Functions I",
        "description": "Introduction to Python functions.",
        "topics": ["Function Definition", "Parameters", "Return Values", "Docstrings"],
        "resources": ["Function Tutorial", "Basic Functions Guide"],
        "difficulty": "Beginner+",
        "xp_reward": 250,
        "estimated_hours": 5,
        "color": "#FF9800",
        "zone": "Function Fields"
    },
    "functions_arguments": {
        "title": "Functions II",
        "description": "Working with function arguments.",
        "topics": ["Args", "Kwargs", "Default Values", "Keyword Arguments"],
        "resources": ["Function Arguments", "Parameter Guide"],
        "difficulty": "Intermediate",
        "xp_reward": 300,
        "estimated_hours": 6,
        "color": "#FFB74D",
        "zone": "Function Fields"
    },
    "functions_advanced": {
        "title": "Functions III",
        "description": "Advanced function concepts.",
        "topics": ["Lambda Functions", "Map/Filter/Reduce", "Decorators", "Generators"],
        "resources": ["Advanced Functions", "Functional Programming"],
        "difficulty": "Intermediate",
        "xp_reward": 350,
        "estimated_hours": 8,
        "color": "#FFB74D",
        "zone": "Function Fields"
    },
    "recursion_basic": {
        "title": "Recursion",
        "description": "Understanding recursive functions.",
        "topics": ["Recursive Patterns", "Base Cases", "Call Stack", "Optimization"],
        "resources": ["Recursion Guide", "Recursive Problems"],
        "difficulty": "Intermediate",
        "xp_reward": 350,
        "estimated_hours": 7,
        "color": "#FFB74D",
        "zone": "Function Fields"
    },

    # Error Handling Hills
    "exceptions_basic": {
        "title": "Exceptions I",
        "description": "Basic error handling in Python.",
        "topics": ["Try/Except", "Common Exceptions", "Raising Exceptions", "Finally Clause"],
        "resources": ["Exception Handling", "Error Guide"],
        "difficulty": "Beginner+",
        "xp_reward": 250,
        "estimated_hours": 5,
        "color": "#F44336",
        "zone": "Error Handling Hills"
    },
    "exceptions_advanced": {
        "title": "Exceptions II",
        "description": "Advanced exception handling.",
        "topics": ["Custom Exceptions", "Exception Hierarchy", "Context Managers", "with Statement"],
        "resources": ["Advanced Exceptions", "Context Management"],
        "difficulty": "Intermediate",
        "xp_reward": 300,
        "estimated_hours": 6,
        "color": "#EF5350",
        "zone": "Error Handling Hills"
    },
    "debugging_basic": {
        "title": "Debugging",
        "description": "Tools and techniques for debugging Python code.",
        "topics": ["Print Debugging", "Debugger Basics", "pdb", "Logging"],
        "resources": ["Debugging Guide", "pdb Tutorial"],
        "difficulty": "Intermediate",
        "xp_reward": 300,
        "estimated_hours": 6,
        "color": "#EF5350",
        "zone": "Error Handling Hills"
    },

    # Project Peaks (Side Quests)
    "quest_calculator": {
        "title": "Quest: Calculator",
        "description": "Build a simple calculator application.",
        "topics": ["Functions", "User Input", "Basic Operations", "Error Handling"],
        "resources": ["Calculator Tutorial", "Project Guide"],
        "difficulty": "Beginner",
        "xp_reward": 300,
        "estimated_hours": 4,
        "color": "#9C27B0",
        "zone": "Project Peaks"
    },
    "quest_todo": {
        "title": "Quest: Todo List",
        "description": "Create a command-line todo list.",
        "topics": ["Lists", "File I/O", "User Input", "Data Persistence"],
        "resources": ["Todo App Tutorial", "CLI App Guide"],
        "difficulty": "Beginner+",
        "xp_reward": 400,
        "estimated_hours": 6,
        "color": "#9C27B0",
        "zone": "Project Peaks"
    },
    "quest_hangman": {
        "title": "Quest: Hangman Game",
        "description": "Create a text-based Hangman game.",
        "topics": ["Strings", "Lists", "Random Module", "User Interface"],
        "resources": ["Game Tutorial", "Text Games Guide"],
        "difficulty": "Beginner+",
        "xp_reward": 400,
        "estimated_hours": 5,
        "color": "#9C27B0",
        "zone": "Project Peaks"
    },
    "quest_quiz": {
        "title": "Quest: Quiz Game",
        "description": "Build a multiple-choice quiz application.",
        "topics": ["Dictionaries", "Random", "Score Tracking", "File I/O"],
        "resources": ["Quiz App Tutorial", "JSON with Python"],
        "difficulty": "Intermediate",
        "xp_reward": 450,
        "estimated_hours": 7,
        "color": "#9C27B0",
        "zone": "Project Peaks"
    }
}

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()
    
    # Add nodes and edges for the learning path
    for topic_id, topic_data in PYTHON_TOPICS.items():
        st.session_state.graph.add_node(topic_id, **topic_data)
    
    # Define the learning path connections with multiple paths
    edges = [
        # Beginner's Valley Core Path
        ("basics_intro", "basics_syntax"),
        ("basics_syntax", "variables_basic"),
        ("variables_basic", "strings_basic"),
        ("variables_basic", "numbers_basic"),
        ("strings_basic", "variables_advanced"),
        ("numbers_basic", "variables_advanced"),

        # Control Flow Kingdom Connections
        ("variables_basic", "conditionals_basic"),
        ("conditionals_basic", "loops_basic"),
        ("conditionals_basic", "conditionals_advanced"),
        ("loops_basic", "loops_advanced"),
        ("conditionals_advanced", "loops_advanced"),

        # Data Structures Connections
        ("variables_advanced", "lists_basic"),
        ("loops_basic", "lists_basic"),
        ("lists_basic", "lists_methods"),
        ("lists_methods", "lists_advanced"),
        ("lists_basic", "tuples_basic"),
        ("lists_methods", "dict_basic"),
        ("tuples_basic", "dict_basic"),
        ("dict_basic", "dict_advanced"),
        ("dict_basic", "sets_basic"),
        
        # Functions Connections
        ("variables_advanced", "functions_basic"),
        ("loops_basic", "functions_basic"),
        ("functions_basic", "functions_arguments"),
        ("functions_arguments", "functions_advanced"),
        ("functions_arguments", "recursion_basic"),
        ("loops_advanced", "recursion_basic"),

        # Error Handling Connections
        ("functions_basic", "exceptions_basic"),
        ("exceptions_basic", "exceptions_advanced"),
        ("exceptions_basic", "debugging_basic"),
        
        # Project Connections (Multiple Prerequisites)
        ("variables_basic", "quest_calculator"),
        ("functions_basic", "quest_calculator"),
        ("lists_basic", "quest_todo"),
        ("dict_basic", "quest_todo"),
        ("strings_basic", "quest_hangman"),
        ("lists_basic", "quest_hangman"),
        ("dict_basic", "quest_quiz"),
        ("exceptions_basic", "quest_quiz")
    ]
    st.session_state.graph.add_edges_from(edges)

# Initialize session state for progress tracking
if 'completed_quests' not in st.session_state:
    st.session_state.completed_quests = {"basics_intro"}  # Start with first quest unlocked

if 'current_level' not in st.session_state:
    st.session_state.current_level = 1

if 'total_xp' not in st.session_state:
    st.session_state.total_xp = 0

# Function to check if a quest is available
def is_quest_available(quest_id, graph):
    if quest_id in st.session_state.completed_quests:
        return False  # Already completed
    
    # Get prerequisites (incoming edges)
    predecessors = list(graph.predecessors(quest_id))
    
    # If no prerequisites, or all prerequisites are completed, quest is available
    return not predecessors or all(pred in st.session_state.completed_quests for pred in predecessors)

# Function to check if a quest is locked
def is_quest_locked(quest_id, graph):
    if quest_id in st.session_state.completed_quests:
        return False
    return not is_quest_available(quest_id, graph)

# Function to get quest status color
def get_quest_status_color(quest_id, base_color):
    if quest_id in st.session_state.completed_quests:
        return "#808080"  # Completed (gray)
    elif is_quest_available(quest_id, st.session_state.graph):
        return base_color  # Available (original color)
    else:
        return "#D3D3D3"  # Locked (light gray)

# Function to create quest details UI
def show_quest_details(quest_id):
    topic_data = PYTHON_TOPICS[quest_id]
    
    st.subheader(f"⚔️ {topic_data['title']}")
    
    # Create columns for layout
    main_col, side_col = st.columns([2, 1])
    
    with main_col:
        st.markdown(f"**Description:** {topic_data['description']}")
        
        # Show prerequisites first
        prerequisites = list(st.session_state.graph.predecessors(quest_id))
        if prerequisites:
            st.markdown("#### 📋 Prerequisites")
            for prereq in prerequisites:
                status = "✅" if prereq in st.session_state.completed_quests else "❌"
                st.markdown(f"- {PYTHON_TOPICS[prereq]['title']} {status}")
        
        st.markdown("#### 🎯 Quest Objectives")
        for topic in topic_data['topics']:
            st.markdown(f"- {topic}")
        
        st.markdown("#### 📚 Learning Resources")
        for resource in topic_data['resources']:
            st.markdown(f"- {resource}")
    
    with side_col:
        st.markdown("#### ℹ️ Quest Info")
        st.markdown(f"**Zone:** {topic_data['zone']}")
        st.markdown(f"**Difficulty:** {topic_data['difficulty']}")
        st.markdown(f"**XP Reward:** {topic_data['xp_reward']} XP")
        st.markdown(f"**Est. Time:** {topic_data['estimated_hours']} hours")
        
        # Quest status and completion
        if quest_id in st.session_state.completed_quests:
            st.success("✅ Quest Completed!")
        elif is_quest_available(quest_id, st.session_state.graph):
            if st.button("Complete Quest", key=f"complete_{quest_id}"):
                st.session_state.completed_quests.add(quest_id)
                st.session_state.total_xp += topic_data['xp_reward']
                
                # Level up system
                new_level = (st.session_state.total_xp // 1000) + 1
                if new_level > st.session_state.current_level:
                    st.session_state.current_level = new_level
                    st.balloons()
                    st.success(f"🎉 Level Up! You are now level {new_level}!")
                
                st.success("Quest completed! 🎉")
                st.rerun()
        else:
            st.error("🔒 Complete prerequisites first!")

# Title and description
st.title("🐍 Python Learning RPG Map")
st.markdown("""
This interactive map shows your journey to Python mastery. Each node represents a quest or challenge to complete.

### Map Legend
- 🟢 **Green nodes**: Beginner quests (Beginner's Valley)
- 🔵 **Blue nodes**: Data structure quests (Data Structure Plains)
- 🟠 **Orange nodes**: Function quests (Function Fields)
- 🟣 **Purple nodes**: Side projects (Project Peaks)

### Quest Status
- ⬜ **Gray nodes**: Locked quests (prerequisites not met)
- 🔳 **Colored nodes**: Available quests
- ⬛ **Dark gray nodes**: Completed quests
""")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["World Map", "Quest Details", "Adventure Progress"])

with tab1:
    # Create and configure the network
    net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")
    net.toggle_physics(False)
    
    # Configure network options for better visualization
    net.set_options("""
    {
        "nodes": {
            "shape": "hexagon",
            "shadow": true,
            "font": {
                "size": 14,
                "face": "Roboto"
            },
            "scaling": {
                "label": {
                    "enabled": true,
                    "min": 8,
                    "max": 20
                }
            }
        },
        "edges": {
            "color": {
                "inherit": false
            },
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            },
            "smooth": {
                "type": "continuous",
                "roundness": 0.5
            }
        },
        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "UD",
                "sortMethod": "directed",
                "nodeSpacing": 150,
                "levelSeparation": 100,
                "treeSpacing": 200
            }
        },
        "interaction": {
            "dragNodes": true,
            "dragView": true,
            "zoomView": true,
            "hover": true,
            "multiselect": false,
            "navigationButtons": true
        },
        "physics": {
            "enabled": false,
            "hierarchicalRepulsion": {
                "centralGravity": 0.0,
                "springLength": 100,
                "springConstant": 0.01,
                "nodeDistance": 120
            },
            "minVelocity": 0.75
        }
    }
    """)

    # Add nodes and edges with improved visibility
    for node_id in st.session_state.graph.nodes():
        node_data = st.session_state.graph.nodes[node_id]
        
        # Determine node status
        is_completed = node_id in st.session_state.completed_quests
        is_available = is_quest_available(node_id, st.session_state.graph)
        
        # Create status indicator
        status_icon = "✅ " if is_completed else "🔓 " if is_available else "🔒 "
        
        # Create tooltip with more info
        tooltip = f"""
        {status_icon}{node_data['title']}
        
        Difficulty: {node_data['difficulty']}
        XP Reward: {node_data['xp_reward']}
        Time: ~{node_data['estimated_hours']} hours
        
        Click to view in Quest Details tab!
        """
        
        # Add node with modified appearance
        net.add_node(
            node_id,
            label=f"{node_data['title']}",
            title=tooltip,
            color=get_quest_status_color(node_id, node_data['color']),
            borderWidth=3 if is_available else 1,
            borderWidthSelected=4,
            size=30 if is_completed or is_available else 25
        )

    # Add edges with improved visibility
    for edge in st.session_state.graph.edges():
        source, target = edge
        is_active = (source in st.session_state.completed_quests and 
                    is_quest_available(target, st.session_state.graph))
        
        net.add_edge(
            source, 
            target, 
            color="#2E7D32" if is_active else "#D3D3D3",
            width=2 if is_active else 1,
            smooth={'type': 'curvedCW', 'roundness': 0.2}
        )

    # Save and display the network
    html_path = "network.html"
    net.save_graph(html_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=750)

with tab2:
    # Quest selection and details
    st.header("Quest Details")
    
    # Filter by zone
    selected_zone = st.selectbox(
        "Select Zone:",
        options=sorted(set(topic['zone'] for topic in PYTHON_TOPICS.values()))
    )
    
    # Filter topics by selected zone and availability
    zone_topics = {k: v for k, v in PYTHON_TOPICS.items() 
                  if v['zone'] == selected_zone and 
                  (k in st.session_state.completed_quests or is_quest_available(k, st.session_state.graph))}
    
    if not zone_topics:
        st.warning("No quests available in this zone yet! Complete prerequisites to unlock more quests.")
    else:
        selected_topic = st.selectbox(
            "Select Quest:",
            options=list(zone_topics.keys()),
            format_func=lambda x: f"{zone_topics[x]['title']} {'✅' if x in st.session_state.completed_quests else '🔓'}"
        )
        
        # Show quest details
        show_quest_details(selected_topic)

with tab3:
    # Adventure Progress Overview
    st.header("Your Adventure Progress")
    
    # Player Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Level", st.session_state.current_level)
    with col2:
        st.metric("Total XP", st.session_state.total_xp)
    with col3:
        completion_rate = len(st.session_state.completed_quests) / len(PYTHON_TOPICS) * 100
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Progress bars for each zone
    st.subheader("Zone Progress")
    
    for zone in sorted(set(topic['zone'] for topic in PYTHON_TOPICS.values())):
        zone_quests = {k: v for k, v in PYTHON_TOPICS.items() if v['zone'] == zone}
        completed_in_zone = len([q for q in zone_quests if q in st.session_state.completed_quests])
        total_in_zone = len(zone_quests)
        
        progress = completed_in_zone / total_in_zone
        st.markdown(f"**{zone}** ({completed_in_zone}/{total_in_zone} quests)")
        st.progress(progress)
        
        # Show available quests in zone
        available_quests = [q for q in zone_quests if is_quest_available(q, st.session_state.graph)]
        if available_quests:
            st.markdown("Available Quests:")
            for quest in available_quests:
                st.markdown(f"- {PYTHON_TOPICS[quest]['title']}")
        st.markdown("---")

# Sidebar stats and controls
with st.sidebar:
    st.header("🎮 Adventure Controls")
    
    # Quick stats
    st.markdown("### 📈 Quick Stats")
    st.markdown(f"**Quests Completed:** {len(st.session_state.completed_quests)}/{len(PYTHON_TOPICS)}")
    st.markdown(f"**Current Level:** {st.session_state.current_level}")
    st.markdown(f"**Total XP:** {st.session_state.total_xp}")
    
    # XP Progress bar
    next_level_xp = (st.session_state.current_level * 1000)
    current_level_progress = (st.session_state.total_xp % 1000) / 1000
    st.markdown(f"**Progress to Level {st.session_state.current_level + 1}**")
    st.progress(current_level_progress)
    st.text(f"XP to next level: {next_level_xp - (st.session_state.total_xp % 1000)}")
    
    st.markdown("---")
    
    # Reset button (for testing)
    if st.button("🔄 Reset Progress"):
        st.session_state.completed_quests = {"basics_intro"}
        st.session_state.current_level = 1
        st.session_state.total_xp = 0
        st.rerun() 