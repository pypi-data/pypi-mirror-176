from functools import partial

import jax
import jax.numpy as jnp
from typing import Tuple


@partial(jax.custom_jvp, nondiff_argnums=(0, 2))
def __generic_mantissa(op, x: jnp.ndarray, n: int) -> jnp.ndarray:
    def fn(x):
        s = jnp.sign(x)
        x = jnp.abs(x)
        a = jnp.floor(jnp.log2(x))
        x = x / 2**a
        # assert jnp.all(1.0 <= x) and jnp.all(x < 2.0), x
        x = op(x * 2**n) / 2**n
        x = x * 2**a
        return s * x

    return jnp.where(x == 0.0, 0.0, fn(jnp.where(x == 0.0, 1.0, x)))


@__generic_mantissa.defjvp
def _jvp(
    op,
    n: int,
    primals: Tuple[jnp.ndarray],
    tangents: Tuple[jnp.ndarray],
) -> Tuple[jnp.ndarray, jnp.ndarray]:
    (x,) = primals
    (x_dot,) = tangents

    primal = __generic_mantissa(op, x, n)
    tangent = x_dot
    return primal, tangent


@partial(jax.jit, static_argnums=(0, 2))
def _generic_mantissa(op, x: jnp.ndarray, n: int) -> jnp.ndarray:
    return __generic_mantissa(op, x, n)


def round_mantissa(x: jnp.ndarray, n: int) -> jnp.ndarray:
    """Round number

    Args:
        x: number to round
        n: number of mantissa digits to keep

    Returns:
        rounded number

    Example:
        >>> round_mantissa(0.5 + 0.25 + 0.125, 0)
        array(1.)

        >>> round_mantissa(0.5 + 0.25 + 0.125, 2)
        array(0.875)
    """
    return _generic_mantissa(jnp.round, x, n)


def floor_mantissa(x: jnp.ndarray, n: int) -> jnp.ndarray:
    """Floor number

    Args:
        x: number to floor
        n: number of mantissa digits to keep

    Returns:
        floored number

    Example:
        >>> floor_mantissa(0.5 + 0.25 + 0.125, 0)
        array(0.5)
    """
    return _generic_mantissa(jnp.floor, x, n)


def ceil_mantissa(x: jnp.ndarray, n: int) -> jnp.ndarray:
    """Ceil number

    Args:
        x: number to ceil
        n: number of mantissa digits to keep

    Returns:
        ceiled number

    Example:
        >>> ceil_mantissa(0.5 + 0.25 + 0.125, 0)
        array(1.)
    """
    return _generic_mantissa(jnp.ceil, x, n)
