def remove_consecutive_newlines(string):
    return '\n'.join([line for line in string.split('\n') if line.strip()])
