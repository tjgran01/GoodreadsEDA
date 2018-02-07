def escape_double_quotes(string):
    """When entering information into the SQL db, there is a chance to get
    double quote characters within the text. This turns them into single
    quotes, so they do not escape the insert command."""

    string = string.replace('"', "'")
    return(string)




string = """This sting has "" in it"""
string = escape_double_quotes(string)
print(string)
