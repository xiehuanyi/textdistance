# external
import pytest

# project
import textdistance


ALG = textdistance.LCSSeq


@pytest.mark.parametrize('left, right, expected', [
    ('ab', 'cd', ''),
    ('abcd', 'abcd', 'abcd'),

    ('test', 'text', 'tet'),
    ('thisisatest', 'testing123testing', 'tsitest'),
    ('DIXON', 'DICKSONX', 'DION'),
    ('random exponential', 'layer activation', 'ratia'),

    ('a' * 80, 'a' * 80, 'a' * 80),
    ('a' * 80, 'b' * 80, ''),
])
def test_distance(left, right, expected):
    actual = ALG(external=False)(left, right)
    assert actual == expected

    actual = ALG(external=True)(left, right)
    assert actual == expected


@pytest.mark.parametrize('seqs, expected', [
    (('a', 'b', 'c'), ''),
    (('a', 'a', 'a'), 'a'),
    (('test', 'text', 'tempest'), 'tet'),
])
def test_distance_multiseq(seqs, expected):
    actual = ALG(external=False)(*seqs)
    assert actual == expected

    actual = ALG(external=True)(*seqs)
    assert actual == expected


@pytest.mark.parametrize('use_numpy', [True, False])
@pytest.mark.parametrize('left, right, expected', [
    ('ABC', 'abc', 'ABC'),
    ('AxB', 'ab', 'AB'),
    ('abc', 'XYZ', ''),
])
def test_custom_comparator(left, right, expected, use_numpy, monkeypatch):
    # built-in
    from array import array

    # project
    from textdistance.algorithms import sequence_based

    if not use_numpy:
        monkeypatch.setattr(sequence_based, 'numpy', None)
        monkeypatch.setattr(sequence_based, 'array', array, raising=False)

    def ignore_case(*characters):
        return len({character.lower() for character in characters}) == 1

    algorithm = ALG(test_func=ignore_case, external=False)
    assert algorithm(left, right) == expected
    assert algorithm.similarity(left, right) == len(expected)
