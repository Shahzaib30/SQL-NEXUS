import psycopg2
from psycopg2.extras import RealDictCursor
from langchain_core.tools import tool
from core.config import settings
import sqlparse
import logging
import time


logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - [AI-DB-AUDIT] - %(levelname)s - %(message)s',
    filename = 'agent_database_audit.log'
        
)

logger = logging.getLogger(__name__)

RESTRICTED_TABLES = {'auth-tokens', 'passwords', 'internal-logs'}

def is_query_safe(query: str) -> bool:
    """Uses AST parsing to guarentee the query is only a SELECT statement and does not access restricted tables."""

    try: 
        parsed_statements = sqlparse.parse(query)
        if not parsed_statements:
            logger.warning("Empty query provided.")
            return False
        for statement in parsed_statements:
            if statement.get_type() != 'SELECT':
                logger.warning(f"Query is not a SELECT statement: {query}")
                return False
            for token in statement.tokens:
                if token.ttype is None and token.value.lower() in RESTRICTED_TABLES:
                    logger.warning(f"Query accesses restricted table: {token.value}")
                    return False
    except Exception as e:
        logger.error(f"Error occurred while parsing query: {e}")
        return False
    return True

@tool()
def get_all_tables() -> list:
    """Returns a list of all allowed tables in the database. Use this to understand the database structure."""
    try:
        with psycopg2.connect(settings.DATABASE_URL) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public';
                """)
                tables = [t['table_name'] for t in cursor.fetchall() if t['table_name'] not in RESTRICTED_TABLES]
        logger.info(f"Fetched tables: {tables}")
        return f"Database contains the following tables: {', '.join(tables)}"
    except Exception as e:
        logger.error(f"Error fetching tables:{str(e)}")
        return f"Error fetching tables: {str(e)}"


@tool()
def get_table_schema(table_name: str) -> str:
    """Returns the schema of a specific table. Use this to understand the structure of a table before querying it."""
    if table_name in RESTRICTED_TABLES:
        logger.warning(f"Attempted to access restricted table schema: {table_name}")
        return f"Access to the schema of '{table_name}' is restricted."
    try:
        with psycopg2.connect(settings.DATABASE_URL) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        c.column_name, 
                        c.data_type,
                        tc.constraint_type
                    FROM information_schema.columns c
                    LEFT JOIN information_schema.key_column_usage kcu 
                        ON c.column_name = kcu.column_name AND c.table_name = kcu.table_name
                    LEFT JOIN information_schema.table_constraints tc 
                        ON kcu.constraint_name = tc.constraint_name
                    WHERE c.table_name = %s;
                """, (table_name,))
                columns = cursor.fetchall()
        if not columns:
            logger.warning(f"Table not found when fetching schema: {table_name}")
            return f"Table '{table_name}' does not exist."
        schema_info = "\n".join([f"{col['column_name']} ({col['data_type']})" for col in columns])
        logger.info(f"Fetched schema for table '{table_name}': {schema_info}")
        return f"Schema for '{table_name}':\n{schema_info}"
    except Exception as e:
        logger.error(f"Error fetching schema for table '{table_name}': {str(e)}")
        return f"Error fetching schema for '{table_name}': {str(e)}"
    
@tool()
def execute_read_query(query: str) -> str:
    """Executes a read-only SQL query (SELECT statements only). Use this to retrieve data from the database."""
    if not is_query_safe(query):
        return "Query is not safe to execute. Only SELECT statements that do not access restricted tables are allowed."
    start_time = time.time()
    try:
        with psycopg2.connect(settings.DATABASE_URL) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SET statement_timeout TO 5000;")  # Set a timeout of 5 seconds for the query
                logger.info(f"Executing query: {query}")
                cursor.execute(query)
                results = cursor.fetchmany(100)  # Fetch 100 rows at a time
        execution_time = round(time.time() - start_time, 2)
        logger.info(f"Executed query: {query} - Rows returned: {len(results)} in {execution_time} seconds")
        if not results:
            return "Query executed successfully but returned no results."
        return f"Query executed successfully. Results:\n{results}"
    except Exception as e:
        logger.error(f"Error executing query: {query} - Error: {str(e)}")
        return f"Error executing query: {str(e)}"