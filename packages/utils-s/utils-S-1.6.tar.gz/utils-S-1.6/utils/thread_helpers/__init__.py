import threading

def thread(func, args):
    '''
    Must be a function in without ()
    example if the function is def hello():
    thread would be called like so thread(func=hello, args=['argument1', 'argument2']
    '''
    Obj = threading.Thread(target=func, args=args)
    Obj.start()
    return Obj

def multiple_threads(funcs:list, args:list):
    """
    :param funcs:
    Functions must be in a list like so [function1, function2, function3]
    :param args:
    The arguments must be a list containing a list of args per function
    like so [[arg1forfunction1, arg2forfunction1],[arg1forfunction2, arg2forfunction2], ...]
    The arguments list and the function must be have the same index in both list for a function without
    args the list can be done like so [None]
    :return:
    A list of all the started threads
    """
    x = 0
    Objs = []
    for f in funcs:
        if args[x][0] == None:
            Obj = threading.Thread(target=f)
        else:
            Obj = threading.Thread(target=f, args=args[x])

        Objs.append(Obj)

        x = x + 1


    for o in Objs:
        o.start()


    return Objs

