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


@pytest.mark.parametrize('qval, sequences, expected', [
    (2, ('abcd', 'bcde'), [('b', 'c'), ('c', 'd')]),
    (2, ('abcd', 'bcde', 'xbcd'), [('b', 'c'), ('c', 'd')]),
    (2, ('abcd', 'wxyz'), []),
    (None, ('one two three', 'zero two three'), ['two', 'three']),
    (None, ('one two three', 'two three four', 'zero two three'), ['two', 'three']),
    (None, ('one two',), ['one', 'two']),
])
def test_prepared_subsequences(qval, sequences, expected):
    algorithm = ALG(qval=qval, external=False)
    assert algorithm(*sequences) == expected
    assert algorithm.similarity(*sequences) == len(expected)


@pytest.mark.parametrize('qval, sequence', [(None, 'one two'), (2, 'abcd')])
def test_prepared_subsequence_normalization(qval, sequence):
    algorithm = ALG(qval=qval, external=False)
    assert algorithm.normalized_similarity(sequence, sequence) == 1
    assert algorithm.normalized_distance(sequence, sequence) == 0
