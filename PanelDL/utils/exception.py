class error(Exception):
    def __init__(self, *args):
        print("An Error Occured:",end='')
        for i in args:
            print(i, end=' ')

