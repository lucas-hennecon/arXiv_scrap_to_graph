"""
This file contains functions that save paper ids and its references to a Neo4j graph database.
"""
from typing import List, Dict
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "XXXX")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "XXXX")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "")  

print(NEO4J_USER)

driver = GraphDatabase.driver(
    NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)    
)

def add_graph_to_db(graph: Dict[str, List[str]]) -> None:
    """
    Write the whole graph to the database.
    :param graph: The graph to write to the database.
    """
    db_setup_query = "CREATE CONSTRAINT FOR (p:Paper) REQUIRE p.id IS UNIQUE"
    add_paper_query = "MERGE (p:Paper {id: $paper_id})"
    add_relationship_query = """
        MATCH (p1:Paper {id: $paper_id}), (p2:Paper {id: $reference_id})
        MERGE (p1)-[:REFERENCES]->(p2)
    """

    with driver.session(database=NEO4J_DATABASE) as session:
        # Ensure paper_id is unique
        session.execute_write(lambda tx: tx.run(db_setup_query))

        # Create a node for each paper
        for paper_id in graph.keys():
            session.execute_write(
                lambda tx: tx.run(
                    add_paper_query,
                    paper_id=paper_id
                )
            )
        # Add the relationships
        for paper_id, references in graph.items():
            for reference_id in references:
                session.execute_write(
                    lambda tx: tx.run(
                        add_relationship_query,
                        paper_id=paper_id,
                        reference_id=reference_id
                    )
                )
    
        

def count_papers() -> int:
    """
    Count the number of papers in the graph database.

    :return: The number of papers in the database.
    """
    query = """
    MATCH (p:Paper)
    RETURN count(p) as count
    """

    with driver.session(database=NEO4J_DATABASE) as session:
       return session.execute_read(
            lambda tx: tx.run(query).single()["count"]
        )
        

if __name__ == "__main__":
    graph = {
    '2405.18952v2': ['2403.17710v3', '2406.20060v1'],
    '2403.17710v3': ['2408.17072v1'],
    '2408.17072v1': ['2402.12366v1', '2403.08309v2', '2410.13785v1'],
    '2410.04112v1': ['2407.09551v1'],
    '2403.08309v2': ['2402.03746v3', '2402.10986v3'],
    '2403.09032v2': ['2402.11907v2'],
    '2402.12366v1': [],
    '2402.10986v3': ['2410.12832v1', '2406.07295v2'],
    '2410.13785v1': ['2402.03746v3', '2405.18952v2'],
    '2406.20060v1': [],
    '2402.03746v3': ['2406.20060v1'],
    '2407.09551v1': ['2402.12366v1', '2408.17072v1'],
    '2410.12832v1': ['2403.09032v2', '2405.18952v2', '2402.11907v2'],
    '2402.11907v2': [],
    '2406.07295v2': ['2403.17710v3']
    }
    add_graph_to_db(graph)