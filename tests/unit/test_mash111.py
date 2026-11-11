import pytest

from python_model.mash111.mash111 import Mash111


@pytest.mark.parametrize("width", [1, 4, 20])
def test_initial_state(width):
    model = Mash111(width=width)

    assert model.accumulators == (0, 0, 0)
    assert model.modulus == 2**width
    assert model.mask == 2**width - 1


@pytest.mark.parametrize("width", [0, -1])
def test_rejects_nonpositive_width(width):
    with pytest.raises(ValueError):
        Mash111(width=width)


@pytest.mark.parametrize("width", [True, 2.5, "20", None])
def test_rejects_noninteger_width(width):
    with pytest.raises(TypeError):
        Mash111(width=width)


@pytest.mark.parametrize("frac_word", [-1, 16])
def test_rejects_input_outside_range(frac_word):
    model = Mash111(width=4)

    with pytest.raises(ValueError):
        model.step(frac_word)


@pytest.mark.parametrize("frac_word", [True, 0.5, "1", None])
def test_rejects_noninteger_input(frac_word):
    model = Mash111(width=4)

    with pytest.raises(TypeError):
        model.step(frac_word)


def test_zero_input_keeps_zero_state():
    model = Mash111()

    for _ in range(100):
        assert model.step(0) == 0
        assert model.accumulators == (0, 0, 0)


def test_accumulators_wrap_and_use_previous_cycle_state():
    model = Mash111(width=2)

    model.step(3)
    assert model.accumulators == (3, 0, 0)

    model.step(3)
    assert model.accumulators == (2, 3, 0)

    model.step(3)
    assert model.accumulators == (1, 1, 3)


def test_reset_clears_accumulators_and_output_history():
    model = Mash111(width=4)

    for _ in range(37):
        model.step(11)

    model.reset()

    assert model.accumulators == (0, 0, 0)
    assert [model.step(0) for _ in range(10)] == [0] * 10


def test_reset_reproduces_sequence():
    model = Mash111(width=4)
    inputs = [0, 1, 4, 8, 12, 15] * 10

    first_run = [model.step(value) for value in inputs]
    model.reset()
    second_run = [model.step(value) for value in inputs]

    assert second_run == first_run