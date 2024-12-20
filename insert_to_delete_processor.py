import sqlparse
import re


def delete_processor(sql_script):
    """
    Processes the input SQL script, generates DELETE statements for INSERT statements,
    and modifies comments to replace variations of 'INSERT' with 'DELETE'.
    """
    # Parse the input SQL script into individual statements
    parsed_statements = sqlparse.parse(sql_script)
    output_statements = []

    for statement in parsed_statements:
        # Preserve original content of the statement
        original_statement = str(statement).strip()

        # Modify comments to replace 'INSERT' with 'DELETE'
        modified_statement = modify_comments(original_statement)

        # Process INSERT statements
        if statement.get_type() == "INSERT":
            try:
                delete_statement = generate_delete(statement)
                output_statements.append(delete_statement)
            except ValueError as e:
                # If parsing fails, include the original statement with a warning comment
                output_statements.append(modified_statement)
                output_statements.append(f"-- Error generating DELETE: {e}")
        else:
            # For non-INSERT statements (e.g., SELECT, CREATE), retain as is
            output_statements.append(modified_statement)

    # Combine all the processed statements, preserving formatting
    return "\n".join(output_statements)


def modify_comments(statement):
    """
    Replaces variations of the word 'INSERT' with 'DELETE' in comments only.
    Handles different spellings such as 'insert', 'inserted', 'inserting', etc.
    """
    # Replace 'insert' variations with 'delete' in single-line comments
    statement = re.sub(r'(--.*?\binsert\w*\b.*?$)', 
                      lambda m: re.sub(r'insert', 'delete', m.group(0), flags=re.IGNORECASE), 
                      statement, flags=re.MULTILINE)
    
    # Replace 'insert' variations with 'delete' in multi-line (block) comments
    statement = re.sub(r'(/\*.*?\binsert\w*\b.*?\*/)', 
                      lambda m: re.sub(r'insert', 'delete', m.group(0), flags=re.IGNORECASE), 
                      statement, flags=re.DOTALL)
    return statement


def generate_delete(parsed):
    """
    Converts an INSERT statement into a DELETE statement by extracting the table name,
    column names, and values.
    """
    tokens = [t for t in parsed.tokens if not t.is_whitespace and t.ttype != sqlparse.tokens.Comment]

    # Extract table name
    table_name = None
    for i, token in enumerate(tokens):
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'INTO':
            table_name = tokens[i + 1].value  # The token following 'INTO' is the table name
            break

    if not table_name:
        raise ValueError("Unable to parse table name from the SQL statement.")

    # Extract column names and values
    column_token = None
    values_token = None

    for token in tokens:
        if token.is_group:  # Look for grouped tokens like (columns) or (values)
            if 'VALUES' not in token.value.upper():  # If it's not a VALUES group, it must be columns
                column_token = token
            else:
                values_token = token

    if not column_token or not values_token:
        raise ValueError("Unable to parse columns or values from the SQL statement.")

    # Parse columns and values
    columns = [col.strip() for col in column_token.value.strip('()').split(',')]
    values = [val.strip() for val in values_token.value.strip('VALUES ()').split(',')]

    # Construct DELETE script
    where_clauses = [f"{col} = {val}" for col, val in zip(columns, values)]
    delete_statement = f"DELETE FROM {table_name} WHERE {' AND '.join(where_clauses)};"
    return delete_statement
