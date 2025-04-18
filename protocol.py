

def data_protocol(x, y, mi, uid, extra=[-1, -1]):
    data = str(x) + ',' + str(y) + ',' + str(mi) + ',' + str(uid) + ',' + str(extra[0]) + ',' + str(extra[1])
    return data