import sxcne.processors.cache as cache

# Test if cache works
def test__cache():
    cache.updateCache("Hello!", "Hi!")
    assert cache.getCached("Hello!") == "Hi!"

# Test if cache performs well on variations of the same word
def test__cache_basic():
    assert cache.getCached("Hello") == "Hi!"
    assert cache.getCached("hello") == "Hi!"
    assert cache.getCached("hello?") == "Hi!"

# Test if cache performs well on variations of the same word but more variants
def test__cache_basic_hard():
    cache.updateCache("Hi!", "oof!")
    assert cache.getCached("hi") == "oof!"
    assert cache.getCached("hi!") == "oof!"
    assert cache.getCached("oh hi?") == "oof!"
    assert cache.getCached("hans?") == None


# Vocab tests to see if it performs well on word swaps
def test__cache_vocab_basic():
    cache.updateCache("John ate ice cream.", "ok")
    assert cache.getCached("John ate ice cream.") == "ok"

    assert cache.getCached("John ate the ice cream.") == "ok"
    assert cache.getCached("John already eat the ice cream.") == "ok"
    assert cache.getCached("John did not eat the ice cream.") == None



# Hard vocab tests. It is ok if it fails.
def test__cache_vocab_hard():
    cache.updateCache("Bob made the cake.", "lol")
    assert cache.getCached("Bob made the cake.") == "lol"

    assert cache.getCached("Bob baked the cake.") == "lol"
    assert cache.getCached("Bob cooked the cake.") == "lol"
    
    assert cache.getCached("Bob ate the cake.") == None


def test__real_world():
    cache.updateCache("You are cool.", "thanks")

    assert cache.getCached("You are cool.") == "thanks"
    assert cache.getCached("U are cool.") == "thanks"
    assert cache.getCached("U are not cool.") == None
    assert cache.getCached("You are not cool.") == None
