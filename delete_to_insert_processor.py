import sqlparse
import os
import re
import datetime
import sys

def insert_processor(sql_script):
    """
    Processes a SQL script, converting DELETE statements to INSERT statements.
    """
    print('Start line 10', flush=True)
    # Parse the input SQL script into individual statements
    parsed_statements = sqlparse.parse(sql_script)
    output_statements = []

    for statement in parsed_statements:
        # Preserve original content of the statement
        original_statement = str(statement).strip()

        # Process comments to replace 'DELETE' with 'INSERT'
        original_statement = modify_comments_for_inserts(original_statement)
        print("20")
        # Process DELETE statements
        if original_statement.upper().startswith("DELETE"):
            print("here")
            try:
                print("here 2")
                insert_statement = generate_insert(statement)
                output_statements.append(insert_statement)
            except ValueError as e:
                # If parsing fails, include the original statement with a warning comment
                output_statements.append(original_statement)
                output_statements.append(f"-- Error generating INSERT: {e}")
        else:
            # For non-DELETE statements (e.g., comments or other SQL), retain as is
            output_statements.append(original_statement)

    # Combine all the processed statements, preserving formatting
    return "\n".join(output_statements)


def modify_comments_for_inserts(statement):
    """
    Replaces variations of the word 'DELETE' with 'INSERT' in comments only.
    """
    # Replace 'delete' variations with 'insert' in comments (case-insensitive)
    statement = re.sub(
        r'(--.*?\bdelete\w*\b.*?$)',
        lambda m: re.sub(r'delete', 'insert', m.group(0), flags=re.IGNORECASE),
        statement,
        flags=re.MULTILINE,
    )
    statement = re.sub(
        r'(/\*.*?\bdelete\w*\b.*?\*/)',
        lambda m: re.sub(r'delete', 'insert', m.group(0), flags=re.IGNORECASE),
        statement,
        flags=re.DOTALL,
    )
    return statement


def generate_insert(parsed):
    tokens = [t for t in parsed.tokens if not t.is_whitespace and t.ttype != sqlparse.tokens.Comment]

    # Extract table name
    table_name = None
    for i, token in enumerate(tokens):
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'FROM':
            table_name = tokens[i + 1].get_real_name()  # Get the actual table name
            break

    if not table_name:
        raise ValueError("Unable to parse table name from the DELETE statement.")

    # Extract WHERE clause
    where_clause_tokens = None
    for i, token in enumerate(tokens):
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'WHERE':
            where_clause_tokens = tokens[i + 1:]  # Collect all tokens after WHERE
            break

    if not where_clause_tokens:
        raise ValueError("Unable to parse WHERE clause from the DELETE statement.")

    # Process WHERE clause conditions
    conditions = []
    for token in where_clause_tokens:
        if isinstance(token, sqlparse.sql.Comparison):  # Check for comparison tokens
            conditions.append(str(token))
        elif token.is_group:  # Handle grouped conditions (e.g., parenthesized expressions)
            conditions.extend([str(t) for t in token.flatten() if isinstance(t, sqlparse.sql.Comparison)])

    if not conditions:
        raise ValueError("Failed to extract conditions from WHERE clause.")

    # Parse columns and values
    columns = []
    values = []
    for condition in conditions:
        if '=' in condition:
            col, val = condition.split('=')
            columns.append(col.strip())
            values.append(val.strip())

    # Construct INSERT statement
    insert_statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
    return insert_statement
