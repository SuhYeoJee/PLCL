class NoTableDataError(Exception):...

def print_error_box(e,*args):
    size = 70
    print('\n')
    print("#"*size)
    print(("##" + str(e)).ljust(size-2) + "##")
    print("##" + "-"*(size-4) + "##")
    [ print(("##" + str(x)).ljust(size-2) + "##") for x in args]
    print("#"*size)
    print('\n')