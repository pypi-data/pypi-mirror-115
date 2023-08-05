class Password:
    def __init__(self, var):
        if var:
            for i in range(1, 10000):
                print("{:04}".format(i))
        else:
            for i in range(1, 1000000):
                print("{:06}".format(i))


print(Password(False))
