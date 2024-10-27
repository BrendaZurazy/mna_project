from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
load_dotenv()


# Settings Env
AURA_INSTANCENAME = os.environ["AURA_INSTANCENAME"]
NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
NEO4J_DATABASE = os.environ["NEO4J_DATABASE"]
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH, database=NEO4J_DATABASE)

def connect_and_query():
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run("MATCH (n) RETURN count(n)")
            count = result.single().value()
            print(f"N. Nodes: {count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

def create_entities(tx):
    # Create single node
    tx.run("MERGE (a:Person {name: 'Alber Einstein'})")

    # Create other nodes
    tx.run("MERGE (p:Subject {name: 'Physics'})")
    tx.run("MERGE (n:NobelPrize {name: 'Nobel Prize in Physics'})")
    tx.run("MERGE (g:Country {name: 'Germany'})")
    tx.run("MERGE (u:Country {name: 'USA'})")

def create_relationships(tx):

    tx.run(
        """MATCH (a:Person {name: 'Alber Einstein'}), (p:Subject {name: 'Physics'})
        MERGE (a)-[:STUDIED]->(p);""")
    
    tx.run(
        """
        MATCH (a:Person {name: 'Alber Einstein'}), (n:NobelPrize {name: 'Nobel Prize in Physics'})
    MERGE (a)-[:WON]->(n);"""
        )
    
    tx.run(
        """
        MATCH (a:Person {name: 'Alber Einstein'}), (g:Country {name: 'Germany'})
    MERGE (a)-[:BORN_IN]->(g);"""
        )
    
    tx.run(
        """
        MATCH (a:Person {name: 'Alber Einstein'}), (u:Country {name: 'USA'})
    MERGE (a)-[:DIED_IN]->(u);"""
        )


def query_graph_simple(cypher_query):
    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(cypher_query)
            for record in result:
                print(record["name"])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

def build_knowledge_graph():

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            # Create entities
            #session.write_transaction(create_entities)
            # Create relationships
            session.write_transaction(create_relationships)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == '__main__':
    # build_knowledge_graph()
    query_graph_simple("MATCH (n) RETURN n.name AS name")