import ast, uuid, copy


# Copyright (c) 2017 Kelly Rivers

def runGiveIds(a):
    global idCounter
    idCounter = 0
    giveIds(a)


idCounter = 0


def giveIds(a):
    global idCounter
    if isinstance(a, ast.AST):
        if type(a) in [ast.Load, ast.Store, ast.Del, ast.AugLoad, ast.AugStore, ast.Param]:
            return  # skip these
        a.global_id = uuid.uuid1()
        idCounter += 1
        for field in a._fields:
            child = getattr(a, field)
            if type(child) == list:
                for i in range(len(child)):
                    # Get rid of aliased items
                    if hasattr(child[i], "global_id"):
                        child[i] = copy.deepcopy(child[i])
                    giveIds(child[i])
            else:
                # Get rid of aliased items
                if hasattr(child, "global_id"):
                    child = copy.deepcopy(child)
                    setattr(a, field, child)
                giveIds(child)
