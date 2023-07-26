import sxcne.utilities

# Aterisk Tests
def test__singeAteriskRemoval():
    string = "Hello *there*"
    assert sxcne.utilities.filter_out_text_between_asterisks(string) == "Hello "

def test__mutltieAteriskRemoval():
    string = "Hello ***there***"
    assert sxcne.utilities.filter_out_text_between_asterisks(string) == "Hello "

def test_multipleAteriskRemoval():
    string = "Hello *there* my *friend*"
    assert sxcne.utilities.filter_out_text_between_asterisks(string) == "Hello  my "


def test_paramRemove():
    string = "Hello (there) my (friend)"
    assert sxcne.utilities.filter_out_text_between_asterisks(string) == "Hello  my "


# Text Slasher Tests

def test__textslasher():
    sentence = "old photos. fwe upfewfewwith you? a friend: feojwfoiew"
    assert sxcne.utilities.slash_sentences(sentence) == "old photos. fwe upfewfewwith you?"