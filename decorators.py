# this is based on the tutorial here: http://thecodeship.com/patterns/guide-to-python-function-decorators/

# Decorators - a function that takes in a function, and returns a different function
# The new function can do anything, including not calling the original function, but typically
    # - does something before calling the function
    # - calls the function
    # - does something after calling the function
    # - returns some alteration of the original function's result

# syntax sugar is:
    # @decorator
    # def decorated_function(...)
# which is equivalent to:
    # original_function = decorator(original_function)

def p_decorate(func):
    def func_wrapper(name):
        return "<p>{0}</p>".format(func(name))
    return func_wrapper

@p_decorate
def get_text(name):
    return "lorem ipsum, {0} dolor sit amet".format(name)

print get_text("Greg")

# you can make a decorator more generic by changing the signature to accept *args, **kwargs
def logger(func):
    def func_wrapper(*args, **kwargs):
        print "*****"
        print "logging all the parameters"
        print args
        print kwargs
        result = func(*args, **kwargs)
        print "logging the result"
        print result
        print "*****"
        return result
    return func_wrapper

@logger 
def first_and_last(first_name, last_name):
    return "Hello " + first_name + " " + last_name

@logger
def first_only(first_name):
    return "Hello " + first_name

print first_and_last("Greg", "Ashby")
print first_only("Greg")

# to use arguments, make a function that takes in those arguments, and returns a decorator
def tag(tag_name):
    def tag_decorator(func):
        def func_wrapper(*args, **kwargs):
            return "<{0}>{1}</{0}>".format(tag_name, func(*args, **kwargs))
        return func_wrapper
    return tag_decorator

@tag("div")
@tag("p")
def content(some_text):
    return "This is your content: " + some_text

print content("some text here")
    
