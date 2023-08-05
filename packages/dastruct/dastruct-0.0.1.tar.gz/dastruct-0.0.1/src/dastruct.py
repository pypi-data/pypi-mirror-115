# Python script to convert different data structure

class NotaTupleException(Exception):
    def __init__(self, message):
        super().__init__(message)


def tuple_to_list(given_tuple):
    output_list = []
    if tuple(given_tuple):
        for i in given_tuple:
            output_list.append(i)
        return output_list
    else:
        raise NotaTupleException("Given Parameter is not a tuple")

