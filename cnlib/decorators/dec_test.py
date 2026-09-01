# def hello():
#     print("hello")

# hello()

# # ------------------------------------------------------------------------------

# def goodbye():
#     print("goodbye")

# hello = goodbye

# hello()

# ------------------------------------------------------------------------------

def goodbye(_func):
    def wrapper():
        print("whatup")
        # print(func())
        print("goodbye")
    return wrapper

# @goodbye
def hello():
    return "hello"

hello = goodbye(hello)

hello()
