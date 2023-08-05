import polars as pl

def contains(substr: str) -> pl.Expr:
    ''' Used to select all columns containing substr.
    
    Args:
        - substr: Pattern contained in some/all column names

    Returns: A pl.col expression to be used in the select method to return all
            columns with names containing substr.
    '''
    return pl.col('^.*' + substr + '.*$')

def startswith(substr: str) -> pl.Expr:
    ''' Used to select all columns starting with substr.
    
    Args:
        - substr: Pattern at the start of some/all column names

    Returns: A pl.col expression to be used in the select method to return all
            columns with names starting with substr.
    '''
    return pl.col('^' + substr + '.*$')

def endswith(substr: str) -> pl.Expr:
    ''' Used to select all columns ending with substr.
    
    Args:
        - substr: Pattern at the end of some/all column names

    Returns: A pl.col expression to be used in the select method to return all
            columns with names ending with substr.
    '''
    return pl.col('^.*' + substr + '$')