import time
import warnings


def get_suitable_seed():
    """
    Returns a start seed requiring minimal pre-computation
    for squares_CBRNG

    Returns
    -------
    A start seed for squares_CBRNG
    """

    return int(1000000*time.time())


def squares(seed=None, bits=32, safety=True):
    """
    Produces a random number based on
    https://arxiv.org/pdf/2004.06278v3.pdf
    Adapted for non 64-bit integers

    Parameters
    ----------
    seed: int
        If provided, serves as the initial key for the generator.
        If this number is not sufficiently high, can cause
        predictably low numbers for the first few iterations
    bits: int
        Maximal number of bits in the output
    safety: bool
        If true, initialization involves repeatedly calculating
        outputs until a sufficiently high number is reached.
        When true, the first yield may take significantly longer
        than subsequent yields.  This is especially true for
        smaller numbers
    """

    # Initialize generator
    ctr = 0
    key = get_suitable_seed() if seed is None else seed

    # Truncate key if necessary
    if key.bit_length() > bits:
        key = truncate(key, bits)
        if seed is not None:
            warnings.warn('Key truncated due to bit limitation',
                          UserWarning)

    # Define shift
    assert bits % 2 == 0, 'Bits must be even'
    bit_shift = int(bits / 2)

    # Define macro
    def square_step(x, y):
        x = truncate(x*x + y, bits)
        return (x >> bit_shift) | (x << bit_shift)

    # Run generator
    while True:
        x = y = ctr*key
        z = y + key

        x = square_step(x, y)
        x = square_step(x, z)
        x = square_step(x, y)

        out = truncate((x*x + z) >> bit_shift, bits)
        if not safety:
            yield out
        elif out.bit_length() == bits:
            safety = False
        ctr += 1


def truncate(x, bits, right_shift=False):
    """
    Truncates x to the specified number of bits

    Parameters
    ----------
    x: int
        Number to truncate
    bits: int
        Desired length (in bits) of x
    right_shift: bool
        If true, preserves the left (higher power)
        portion of x over the right

    Returns
    -------
    x truncated to 'bits' bits
    """

    if right_shift:
        return x >> (x.bit_length() - bits)
    return x & (1 << bits) - 1
