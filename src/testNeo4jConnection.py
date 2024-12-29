"""
Function to test if Neo4j connection is established.
"""

from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def test_neo4j_connection():
    with driver.session() as session:
        result = session.run("RETURN 1")
        print("Test result from Neo4j:", result.single()[0])

if __name__ == "__main__":
    test_neo4j_connection()