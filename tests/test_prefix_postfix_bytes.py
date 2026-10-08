# external
import pytest

# project
import textdistance


@pytest.mark.parametrize('algorithm, sequences, expected', [
    (textdistance.Prefix, (b'abc', b'abx'), b'ab'),
    (textdistance.Prefix, (b'abc',), b'abc'),
    (textdistance.Prefix, (b'abc', b'abd', b'abe'), b'ab'),
    (textdistance.Prefix, (b'\xff\x00a', b'\xff\x00b'), b'\xff\x00'),
    (textdistance.Prefix, (b'abc', b'xyz'), b''),
    (textdistance.Prefix, (b'', b'abc'), b''),
    (textdistance.Postfix, (b'abc', b'xbc'), b'bc'),
    (textdistance.Postfix, (b'abc',), b'abc'),
    (textdistance.Postfix, (b'cba', b'dba', b'eba'), b'ba'),
    (textdistance.Postfix, (b'a\xff\x00', b'b\xff\x00'), b'\xff\x00'),
    (textdistance.Postfix, (b'abc', b'xyz'), b''),
    (textdistance.Postfix, (b'', b'abc'), b''),
])
def test_prefix_postfix_bytes(algorithm, sequences, expected):
    comparator = algorithm()
    assert comparator(*sequences) == expected
    assert comparator.similarity(*sequences) == len(expected)
