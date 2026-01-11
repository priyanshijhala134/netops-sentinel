import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from core.incident_graph import incident_graph

if __name__ == "__main__":
    incident_graph.invoke({})
