def correctNumbering(self, fidFilenames):
    """
    Correct numbering of the fid files

    Takes:     array       fidFilenames: unordered filenames
    Returns:   array       fidFilenames: filenames, integer-sorted
    """
 
    fidNumbers = []
    
    for filename in fidFilenames:
        if filename.endswith('.fid'):
            a = filename.replace(".fid", "")
            fidNumbers.append(a)
    
    z = sorted(fidNumbers, key=int)
    
    fidFilenames = []
    
    for fidNumber in z:
        fidFilenames.append(fidNumber + '.fid')

    return fidFilenames
