import sys

def printMsg(msg, pre="INFO"):
    print(f"[{pre}]:", msg)
    sys.stdout.flush()


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)

    Reference: https://stackoverflow.com/a/34325723
    """
    percent = 100 * (iteration / float(total))
    percentStr = f'{percent:.1f}'
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percentStr, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

