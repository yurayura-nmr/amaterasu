from a_cout import err

def readFile(filename):
    """
    Read file into array. 
    Ignore empty lines.

    Takes:      string      filename
    Returns:    array       columns of the read file
    """
    array = []

    try:
        f = open(filename, 'r')
    except IOError:
        err('Could not open file: ' + filename)

    for line in f:
        columns = line.split()
        if len(columns) > 0:
            array.append(columns)
    f.close()

    return array
