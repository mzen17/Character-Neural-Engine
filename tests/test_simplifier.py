import sxcne.utilities

# Aterisk Tests
def test__simplify_basic():
    string1 = "What up?"
    string2 = "What is up?"
    assert sxcne.utilities.simplify_sentence(string1) == sxcne.utilities.simplify_sentence(string2)

def test__simplify_basic():
    string1 = "Bob at a special cake."
    string2 = "Bob at a unique cake."
    assert sxcne.utilities.simplify_sentence(string1) == sxcne.utilities.simplify_sentence(string2)

