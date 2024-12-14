from random import randint
from server.token_generator.array import objects

# algorithm for token generation
def token_generator():
    pre_token = []
    token = ''

    for i in range(20):
        number = randint(0, 64)
        object = objects[number]
        pre_token.append(object)

    return token.join(pre_token)