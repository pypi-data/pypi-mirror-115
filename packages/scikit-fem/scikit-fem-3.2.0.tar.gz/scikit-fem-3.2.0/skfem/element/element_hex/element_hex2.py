import numpy as np

from ..element_h1 import ElementH1
from ...refdom import RefHex


def output(a, b, c, d):
    return a, np.array([b, c, d])


_generated_basis = [
    lambda x, y, z: output(
        0.0
        + x * y * z * (-1.0 + y * (2.0 - 4.0 * z) + 2.0 * z)
        + x ** 2 * y * z * (2.0 - 4.0 * z + y * (-4.0 + 8.0 * z)),
        y
        * z
        * (
            -1.0
            + y * (2.0 - 4.0 * z)
            + 2.0 * z
            + x * (4.0 - 8.0 * z + y * (-8.0 + 16.0 * z))
        ),
        x
        * z
        * (
            -1.0
            + y * (4.0 - 8.0 * z)
            + 2.0 * z
            + x * (2.0 - 4.0 * z + y * (-8.0 + 16.0 * z))
        ),
        x
        * y
        * (
            -1.0
            + y * (2.0 - 8.0 * z)
            + 4.0 * z
            + x * (2.0 - 8.0 * z + y * (-4.0 + 16.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x
        * y
        * (1.0 - 3.0 * z + 2.0 * z ** 2 + y * (-2.0 + 6.0 * z - 4.0 * z ** 2))
        + x ** 2
        * y
        * (
            -2.0 + 6.0 * z - 4.0 * z ** 2 + y * (4.0 - 12.0 * z + 8.0 * z ** 2)
        ),
        y
        * (
            1.0
            - 3.0 * z
            + 2.0 * z ** 2
            + y * (-2.0 + 6.0 * z - 4.0 * z ** 2)
            + x
            * (
                -4.0
                + 12.0 * z
                - 8.0 * z ** 2
                + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
            )
        ),
        x
        * (
            1.0
            - 3.0 * z
            + 2.0 * z ** 2
            + y * (-4.0 + 12.0 * z - 8.0 * z ** 2)
            + x
            * (
                -2.0
                + 6.0 * z
                - 4.0 * z ** 2
                + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
            )
        ),
        x
        * y
        * (
            -3.0
            + y * (6.0 - 8.0 * z)
            + 4.0 * z
            + x * (6.0 - 8.0 * z + y * (-12.0 + 16.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x
        * z
        * (1.0 + y ** 2 * (2.0 - 4.0 * z) - 2.0 * z + y * (-3.0 + 6.0 * z))
        + x ** 2
        * z
        * (-2.0 + y * (6.0 - 12.0 * z) + 4.0 * z + y ** 2 * (-4.0 + 8.0 * z)),
        z
        * (
            1.0
            + y ** 2 * (2.0 - 4.0 * z)
            - 2.0 * z
            + y * (-3.0 + 6.0 * z)
            + x
            * (
                -4.0
                + y * (12.0 - 24.0 * z)
                + 8.0 * z
                + y ** 2 * (-8.0 + 16.0 * z)
            )
        ),
        x
        * z
        * (
            -3.0
            + y * (4.0 - 8.0 * z)
            + 6.0 * z
            + x * (6.0 - 12.0 * z + y * (-8.0 + 16.0 * z))
        ),
        x
        * (
            1.0
            + y ** 2 * (2.0 - 8.0 * z)
            - 4.0 * z
            + y * (-3.0 + 12.0 * z)
            + x
            * (
                -2.0
                + y * (6.0 - 24.0 * z)
                + 8.0 * z
                + y ** 2 * (-4.0 + 16.0 * z)
            )
        ),
    ),
    lambda x, y, z: output(
        0.0
        + y
        * z
        * (1.0 + x ** 2 * (2.0 - 4.0 * z) - 2.0 * z + x * (-3.0 + 6.0 * z))
        + y ** 2
        * z
        * (-2.0 + x * (6.0 - 12.0 * z) + 4.0 * z + x ** 2 * (-4.0 + 8.0 * z)),
        y
        * z
        * (
            -3.0
            + y * (6.0 - 12.0 * z)
            + 6.0 * z
            + x * (4.0 - 8.0 * z + y * (-8.0 + 16.0 * z))
        ),
        z
        * (
            1.0
            - 2.0 * z
            + x * (-3.0 + y * (12.0 - 24.0 * z) + 6.0 * z)
            + y * (-4.0 + 8.0 * z)
            + x ** 2 * (2.0 - 4.0 * z + y * (-8.0 + 16.0 * z))
        ),
        y
        * (
            1.0
            - 4.0 * z
            + y * (-2.0 + 8.0 * z)
            + x * (-3.0 + y * (6.0 - 24.0 * z) + 12.0 * z)
            + x ** 2 * (2.0 - 8.0 * z + y * (-4.0 + 16.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x
        * (
            -1.0
            + 3.0 * z
            - 2.0 * z ** 2
            + y ** 2 * (-2.0 + 6.0 * z - 4.0 * z ** 2)
            + y * (3.0 - 9.0 * z + 6.0 * z ** 2)
        )
        + x ** 2
        * (
            2.0
            - 6.0 * z
            + 4.0 * z ** 2
            + y * (-6.0 + 18.0 * z - 12.0 * z ** 2)
            + y ** 2 * (4.0 - 12.0 * z + 8.0 * z ** 2)
        ),
        -1.0
        + 3.0 * z
        - 2.0 * z ** 2
        + y ** 2 * (-2.0 + 6.0 * z - 4.0 * z ** 2)
        + y * (3.0 - 9.0 * z + 6.0 * z ** 2)
        + x
        * (
            4.0
            - 12.0 * z
            + 8.0 * z ** 2
            + y * (-12.0 + 36.0 * z - 24.0 * z ** 2)
            + y ** 2 * (8.0 - 24.0 * z + 16.0 * z ** 2)
        ),
        x
        * (
            3.0
            - 9.0 * z
            + 6.0 * z ** 2
            + y * (-4.0 + 12.0 * z - 8.0 * z ** 2)
            + x
            * (
                -6.0
                + 18.0 * z
                - 12.0 * z ** 2
                + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
            )
        ),
        x
        * (
            3.0
            + y ** 2 * (6.0 - 8.0 * z)
            - 4.0 * z
            + y * (-9.0 + 12.0 * z)
            + x
            * (
                -6.0
                + y * (18.0 - 24.0 * z)
                + 8.0 * z
                + y ** 2 * (-12.0 + 16.0 * z)
            )
        ),
    ),
    lambda x, y, z: output(
        0.0
        + y
        * (
            -1.0
            + 3.0 * z
            - 2.0 * z ** 2
            + x ** 2 * (-2.0 + 6.0 * z - 4.0 * z ** 2)
            + x * (3.0 - 9.0 * z + 6.0 * z ** 2)
        )
        + y ** 2
        * (
            2.0
            - 6.0 * z
            + 4.0 * z ** 2
            + x * (-6.0 + 18.0 * z - 12.0 * z ** 2)
            + x ** 2 * (4.0 - 12.0 * z + 8.0 * z ** 2)
        ),
        y
        * (
            3.0
            - 9.0 * z
            + 6.0 * z ** 2
            + y * (-6.0 + 18.0 * z - 12.0 * z ** 2)
            + x
            * (
                -4.0
                + 12.0 * z
                - 8.0 * z ** 2
                + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
            )
        ),
        -1.0
        + 3.0 * z
        - 2.0 * z ** 2
        + y * (4.0 - 12.0 * z + 8.0 * z ** 2)
        + x
        * (
            3.0
            - 9.0 * z
            + 6.0 * z ** 2
            + y * (-12.0 + 36.0 * z - 24.0 * z ** 2)
        )
        + x ** 2
        * (
            -2.0
            + 6.0 * z
            - 4.0 * z ** 2
            + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
        ),
        y
        * (
            3.0
            - 4.0 * z
            + y * (-6.0 + 8.0 * z)
            + x * (-9.0 + y * (18.0 - 24.0 * z) + 12.0 * z)
            + x ** 2 * (6.0 - 8.0 * z + y * (-12.0 + 16.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + (
            -1.0
            + 3.0 * y
            - 2.0 * y ** 2
            + x ** 2 * (-2.0 + 6.0 * y - 4.0 * y ** 2)
            + x * (3.0 - 9.0 * y + 6.0 * y ** 2)
        )
        * z
        + (
            2.0
            - 6.0 * y
            + 4.0 * y ** 2
            + x * (-6.0 + 18.0 * y - 12.0 * y ** 2)
            + x ** 2 * (4.0 - 12.0 * y + 8.0 * y ** 2)
        )
        * z ** 2,
        z
        * (
            3.0
            + y ** 2 * (6.0 - 12.0 * z)
            - 6.0 * z
            + y * (-9.0 + 18.0 * z)
            + x
            * (
                -4.0
                + y * (12.0 - 24.0 * z)
                + 8.0 * z
                + y ** 2 * (-8.0 + 16.0 * z)
            )
        ),
        z
        * (
            3.0
            - 6.0 * z
            + y * (-4.0 + 8.0 * z)
            + x * (-9.0 + y * (12.0 - 24.0 * z) + 18.0 * z)
            + x ** 2 * (6.0 - 12.0 * z + y * (-8.0 + 16.0 * z))
        ),
        -1.0
        + y * (3.0 - 12.0 * z)
        + 4.0 * z
        + y ** 2 * (-2.0 + 8.0 * z)
        + x ** 2
        * (-2.0 + y * (6.0 - 24.0 * z) + 8.0 * z + y ** 2 * (-4.0 + 16.0 * z))
        + x
        * (3.0 + y ** 2 * (6.0 - 24.0 * z) - 12.0 * z + y * (-9.0 + 36.0 * z)),
    ),
    lambda x, y, z: output(
        1.0
        - 3.0 * z
        + 2.0 * z ** 2
        + y * (-3.0 + 9.0 * z - 6.0 * z ** 2)
        + y ** 2 * (2.0 - 6.0 * z + 4.0 * z ** 2)
        + x ** 2
        * (
            2.0
            - 6.0 * z
            + 4.0 * z ** 2
            + y * (-6.0 + 18.0 * z - 12.0 * z ** 2)
            + y ** 2 * (4.0 - 12.0 * z + 8.0 * z ** 2)
        )
        + x
        * (
            -3.0
            + 9.0 * z
            - 6.0 * z ** 2
            + y ** 2 * (-6.0 + 18.0 * z - 12.0 * z ** 2)
            + y * (9.0 - 27.0 * z + 18.0 * z ** 2)
        ),
        -3.0
        + 9.0 * z
        - 6.0 * z ** 2
        + y ** 2 * (-6.0 + 18.0 * z - 12.0 * z ** 2)
        + y * (9.0 - 27.0 * z + 18.0 * z ** 2)
        + x
        * (
            4.0
            - 12.0 * z
            + 8.0 * z ** 2
            + y * (-12.0 + 36.0 * z - 24.0 * z ** 2)
            + y ** 2 * (8.0 - 24.0 * z + 16.0 * z ** 2)
        ),
        -3.0
        + 9.0 * z
        - 6.0 * z ** 2
        + y * (4.0 - 12.0 * z + 8.0 * z ** 2)
        + x
        * (
            9.0
            - 27.0 * z
            + 18.0 * z ** 2
            + y * (-12.0 + 36.0 * z - 24.0 * z ** 2)
        )
        + x ** 2
        * (
            -6.0
            + 18.0 * z
            - 12.0 * z ** 2
            + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
        ),
        -3.0
        + y * (9.0 - 12.0 * z)
        + 4.0 * z
        + y ** 2 * (-6.0 + 8.0 * z)
        + x ** 2
        * (
            -6.0
            + y * (18.0 - 24.0 * z)
            + 8.0 * z
            + y ** 2 * (-12.0 + 16.0 * z)
        )
        + x
        * (
            9.0
            + y ** 2 * (18.0 - 24.0 * z)
            - 12.0 * z
            + y * (-27.0 + 36.0 * z)
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x ** 2 * y * z * (-8.0 + y * (16.0 - 16.0 * z) + 8.0 * z)
        + x * y * z * (4.0 - 4.0 * z + y * (-8.0 + 8.0 * z)),
        y
        * z
        * (
            4.0
            - 4.0 * z
            + y * (-8.0 + 8.0 * z)
            + x * (-16.0 + y * (32.0 - 32.0 * z) + 16.0 * z)
        ),
        x
        * z
        * (
            4.0
            - 4.0 * z
            + x * (-8.0 + y * (32.0 - 32.0 * z) + 8.0 * z)
            + y * (-16.0 + 16.0 * z)
        ),
        x
        * y
        * (
            4.0
            - 8.0 * z
            + y * (-8.0 + 16.0 * z)
            + x * (-8.0 + y * (16.0 - 32.0 * z) + 16.0 * z)
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x ** 2 * y * z * (-8.0 + y * (8.0 - 16.0 * z) + 16.0 * z)
        + x * y * z * (4.0 - 8.0 * z + y * (-4.0 + 8.0 * z)),
        y
        * z
        * (
            4.0
            - 8.0 * z
            + y * (-4.0 + 8.0 * z)
            + x * (-16.0 + y * (16.0 - 32.0 * z) + 32.0 * z)
        ),
        x
        * z
        * (
            4.0
            - 8.0 * z
            + y * (-8.0 + 16.0 * z)
            + x * (-8.0 + y * (16.0 - 32.0 * z) + 16.0 * z)
        ),
        x
        * y
        * (
            4.0
            - 16.0 * z
            + y * (-4.0 + 16.0 * z)
            + x * (-8.0 + y * (8.0 - 32.0 * z) + 32.0 * z)
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x ** 2 * y * z * (-4.0 + y * (8.0 - 16.0 * z) + 8.0 * z)
        + x * y * z * (4.0 - 8.0 * z + y * (-8.0 + 16.0 * z)),
        y
        * z
        * (
            4.0
            - 8.0 * z
            + y * (-8.0 + 16.0 * z)
            + x * (-8.0 + y * (16.0 - 32.0 * z) + 16.0 * z)
        ),
        x
        * z
        * (
            4.0
            - 8.0 * z
            + x * (-4.0 + y * (16.0 - 32.0 * z) + 8.0 * z)
            + y * (-16.0 + 32.0 * z)
        ),
        x
        * y
        * (
            4.0
            - 16.0 * z
            + x * (-4.0 + y * (8.0 - 32.0 * z) + 16.0 * z)
            + y * (-8.0 + 32.0 * z)
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x ** 2
        * y
        * (
            8.0
            - 24.0 * z
            + 16.0 * z ** 2
            + y * (-8.0 + 24.0 * z - 16.0 * z ** 2)
        )
        + x
        * y
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + y * (4.0 - 12.0 * z + 8.0 * z ** 2)
        ),
        y
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + y * (4.0 - 12.0 * z + 8.0 * z ** 2)
            + x
            * (
                16.0
                - 48.0 * z
                + 32.0 * z ** 2
                + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            )
        ),
        x
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
            + x
            * (
                8.0
                - 24.0 * z
                + 16.0 * z ** 2
                + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            )
        ),
        x
        * y
        * (
            12.0
            - 16.0 * z
            + y * (-12.0 + 16.0 * z)
            + x * (-24.0 + y * (24.0 - 32.0 * z) + 32.0 * z)
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x ** 2
        * y
        * (
            4.0
            - 12.0 * z
            + 8.0 * z ** 2
            + y * (-8.0 + 24.0 * z - 16.0 * z ** 2)
        )
        + x
        * y
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
        ),
        y
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + y * (8.0 - 24.0 * z + 16.0 * z ** 2)
            + x
            * (
                8.0
                - 24.0 * z
                + 16.0 * z ** 2
                + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            )
        ),
        x
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + y * (16.0 - 48.0 * z + 32.0 * z ** 2)
            + x
            * (
                4.0
                - 12.0 * z
                + 8.0 * z ** 2
                + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            )
        ),
        x
        * y
        * (
            12.0
            - 16.0 * z
            + x * (-12.0 + y * (24.0 - 32.0 * z) + 16.0 * z)
            + y * (-24.0 + 32.0 * z)
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x
        * z
        * (-4.0 + y * (12.0 - 12.0 * z) + 4.0 * z + y ** 2 * (-8.0 + 8.0 * z))
        + x ** 2
        * z
        * (
            8.0 + y ** 2 * (16.0 - 16.0 * z) - 8.0 * z + y * (-24.0 + 24.0 * z)
        ),
        z
        * (
            -4.0
            + y * (12.0 - 12.0 * z)
            + 4.0 * z
            + y ** 2 * (-8.0 + 8.0 * z)
            + x
            * (
                16.0
                + y ** 2 * (32.0 - 32.0 * z)
                - 16.0 * z
                + y * (-48.0 + 48.0 * z)
            )
        ),
        x
        * z
        * (
            12.0
            - 12.0 * z
            + y * (-16.0 + 16.0 * z)
            + x * (-24.0 + y * (32.0 - 32.0 * z) + 24.0 * z)
        ),
        x
        * (
            -4.0
            + y * (12.0 - 24.0 * z)
            + 8.0 * z
            + y ** 2 * (-8.0 + 16.0 * z)
            + x
            * (
                8.0
                + y ** 2 * (16.0 - 32.0 * z)
                - 16.0 * z
                + y * (-24.0 + 48.0 * z)
            )
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x
        * z
        * (-4.0 + y * (12.0 - 24.0 * z) + 8.0 * z + y ** 2 * (-8.0 + 16.0 * z))
        + x ** 2
        * z
        * (4.0 + y ** 2 * (8.0 - 16.0 * z) - 8.0 * z + y * (-12.0 + 24.0 * z)),
        z
        * (
            -4.0
            + y * (12.0 - 24.0 * z)
            + 8.0 * z
            + y ** 2 * (-8.0 + 16.0 * z)
            + x
            * (
                8.0
                + y ** 2 * (16.0 - 32.0 * z)
                - 16.0 * z
                + y * (-24.0 + 48.0 * z)
            )
        ),
        x
        * z
        * (
            12.0
            - 24.0 * z
            + x * (-12.0 + y * (16.0 - 32.0 * z) + 24.0 * z)
            + y * (-16.0 + 32.0 * z)
        ),
        x
        * (
            -4.0
            + y * (12.0 - 48.0 * z)
            + 16.0 * z
            + y ** 2 * (-8.0 + 32.0 * z)
            + x
            * (
                4.0
                + y ** 2 * (8.0 - 32.0 * z)
                - 16.0 * z
                + y * (-12.0 + 48.0 * z)
            )
        ),
    ),
    lambda x, y, z: output(
        0.0
        + y
        * z
        * (-4.0 + x * (12.0 - 12.0 * z) + 4.0 * z + x ** 2 * (-8.0 + 8.0 * z))
        + y ** 2
        * z
        * (
            8.0 + x ** 2 * (16.0 - 16.0 * z) - 8.0 * z + x * (-24.0 + 24.0 * z)
        ),
        y
        * z
        * (
            12.0
            - 12.0 * z
            + x * (-16.0 + y * (32.0 - 32.0 * z) + 16.0 * z)
            + y * (-24.0 + 24.0 * z)
        ),
        z
        * (
            -4.0
            + y * (16.0 - 16.0 * z)
            + 4.0 * z
            + x ** 2 * (-8.0 + y * (32.0 - 32.0 * z) + 8.0 * z)
            + x * (12.0 - 12.0 * z + y * (-48.0 + 48.0 * z))
        ),
        y
        * (
            -4.0
            + y * (8.0 - 16.0 * z)
            + 8.0 * z
            + x ** 2 * (-8.0 + y * (16.0 - 32.0 * z) + 16.0 * z)
            + x * (12.0 - 24.0 * z + y * (-24.0 + 48.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + y
        * z
        * (-4.0 + x * (12.0 - 24.0 * z) + 8.0 * z + x ** 2 * (-8.0 + 16.0 * z))
        + y ** 2
        * z
        * (4.0 + x ** 2 * (8.0 - 16.0 * z) - 8.0 * z + x * (-12.0 + 24.0 * z)),
        y
        * z
        * (
            12.0
            - 24.0 * z
            + y * (-12.0 + 24.0 * z)
            + x * (-16.0 + y * (16.0 - 32.0 * z) + 32.0 * z)
        ),
        z
        * (
            -4.0
            + y * (8.0 - 16.0 * z)
            + 8.0 * z
            + x ** 2 * (-8.0 + y * (16.0 - 32.0 * z) + 16.0 * z)
            + x * (12.0 - 24.0 * z + y * (-24.0 + 48.0 * z))
        ),
        y
        * (
            -4.0
            + y * (4.0 - 16.0 * z)
            + 16.0 * z
            + x ** 2 * (-8.0 + y * (8.0 - 32.0 * z) + 32.0 * z)
            + x * (12.0 - 48.0 * z + y * (-12.0 + 48.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x
        * (
            4.0
            - 12.0 * z
            + 8.0 * z ** 2
            + y * (-12.0 + 36.0 * z - 24.0 * z ** 2)
            + y ** 2 * (8.0 - 24.0 * z + 16.0 * z ** 2)
        )
        + x ** 2
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + y ** 2 * (-8.0 + 24.0 * z - 16.0 * z ** 2)
            + y * (12.0 - 36.0 * z + 24.0 * z ** 2)
        ),
        4.0
        - 12.0 * z
        + 8.0 * z ** 2
        + y * (-12.0 + 36.0 * z - 24.0 * z ** 2)
        + y ** 2 * (8.0 - 24.0 * z + 16.0 * z ** 2)
        + x
        * (
            -8.0
            + 24.0 * z
            - 16.0 * z ** 2
            + y ** 2 * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            + y * (24.0 - 72.0 * z + 48.0 * z ** 2)
        ),
        x
        * (
            -12.0
            + 36.0 * z
            - 24.0 * z ** 2
            + y * (16.0 - 48.0 * z + 32.0 * z ** 2)
            + x
            * (
                12.0
                - 36.0 * z
                + 24.0 * z ** 2
                + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            )
        ),
        x
        * (
            -12.0
            + y * (36.0 - 48.0 * z)
            + 16.0 * z
            + y ** 2 * (-24.0 + 32.0 * z)
            + x
            * (
                12.0
                + y ** 2 * (24.0 - 32.0 * z)
                - 16.0 * z
                + y * (-36.0 + 48.0 * z)
            )
        ),
    ),
    lambda x, y, z: output(
        0.0
        + y
        * (
            4.0
            - 12.0 * z
            + 8.0 * z ** 2
            + x * (-12.0 + 36.0 * z - 24.0 * z ** 2)
            + x ** 2 * (8.0 - 24.0 * z + 16.0 * z ** 2)
        )
        + y ** 2
        * (
            -4.0
            + 12.0 * z
            - 8.0 * z ** 2
            + x ** 2 * (-8.0 + 24.0 * z - 16.0 * z ** 2)
            + x * (12.0 - 36.0 * z + 24.0 * z ** 2)
        ),
        y
        * (
            -12.0
            + 36.0 * z
            - 24.0 * z ** 2
            + y * (12.0 - 36.0 * z + 24.0 * z ** 2)
            + x
            * (
                16.0
                - 48.0 * z
                + 32.0 * z ** 2
                + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            )
        ),
        4.0
        - 12.0 * z
        + 8.0 * z ** 2
        + y * (-8.0 + 24.0 * z - 16.0 * z ** 2)
        + x ** 2
        * (
            8.0
            - 24.0 * z
            + 16.0 * z ** 2
            + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
        )
        + x
        * (
            -12.0
            + 36.0 * z
            - 24.0 * z ** 2
            + y * (24.0 - 72.0 * z + 48.0 * z ** 2)
        ),
        y
        * (
            -12.0
            + y * (12.0 - 16.0 * z)
            + 16.0 * z
            + x ** 2 * (-24.0 + y * (24.0 - 32.0 * z) + 32.0 * z)
            + x * (36.0 - 48.0 * z + y * (-36.0 + 48.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + (
            4.0
            - 12.0 * y
            + 8.0 * y ** 2
            + x * (-12.0 + 36.0 * y - 24.0 * y ** 2)
            + x ** 2 * (8.0 - 24.0 * y + 16.0 * y ** 2)
        )
        * z
        + (
            -4.0
            + 12.0 * y
            - 8.0 * y ** 2
            + x ** 2 * (-8.0 + 24.0 * y - 16.0 * y ** 2)
            + x * (12.0 - 36.0 * y + 24.0 * y ** 2)
        )
        * z ** 2,
        z
        * (
            -12.0
            + y * (36.0 - 36.0 * z)
            + 12.0 * z
            + y ** 2 * (-24.0 + 24.0 * z)
            + x
            * (
                16.0
                + y ** 2 * (32.0 - 32.0 * z)
                - 16.0 * z
                + y * (-48.0 + 48.0 * z)
            )
        ),
        z
        * (
            -12.0
            + y * (16.0 - 16.0 * z)
            + 12.0 * z
            + x ** 2 * (-24.0 + y * (32.0 - 32.0 * z) + 24.0 * z)
            + x * (36.0 - 36.0 * z + y * (-48.0 + 48.0 * z))
        ),
        4.0
        + y ** 2 * (8.0 - 16.0 * z)
        - 8.0 * z
        + y * (-12.0 + 24.0 * z)
        + x ** 2
        * (
            8.0
            + y ** 2 * (16.0 - 32.0 * z)
            - 16.0 * z
            + y * (-24.0 + 48.0 * z)
        )
        + x
        * (
            -12.0
            + y * (36.0 - 72.0 * z)
            + 24.0 * z
            + y ** 2 * (-24.0 + 48.0 * z)
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x * y * z * (-16.0 + y * (16.0 - 16.0 * z) + 16.0 * z)
        + x ** 2 * y * z * (32.0 - 32.0 * z + y * (-32.0 + 32.0 * z)),
        y
        * z
        * (
            -16.0
            + y * (16.0 - 16.0 * z)
            + 16.0 * z
            + x * (64.0 - 64.0 * z + y * (-64.0 + 64.0 * z))
        ),
        x
        * z
        * (
            -16.0
            + y * (32.0 - 32.0 * z)
            + 16.0 * z
            + x * (32.0 - 32.0 * z + y * (-64.0 + 64.0 * z))
        ),
        x
        * y
        * (
            -16.0
            + y * (16.0 - 32.0 * z)
            + 32.0 * z
            + x * (32.0 - 64.0 * z + y * (-32.0 + 64.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x * y * z * (-16.0 + y * (16.0 - 32.0 * z) + 32.0 * z)
        + x ** 2 * y * z * (16.0 - 32.0 * z + y * (-16.0 + 32.0 * z)),
        y
        * z
        * (
            -16.0
            + y * (16.0 - 32.0 * z)
            + 32.0 * z
            + x * (32.0 - 64.0 * z + y * (-32.0 + 64.0 * z))
        ),
        x
        * z
        * (
            -16.0
            + y * (32.0 - 64.0 * z)
            + 32.0 * z
            + x * (16.0 - 32.0 * z + y * (-32.0 + 64.0 * z))
        ),
        x
        * y
        * (
            -16.0
            + y * (16.0 - 64.0 * z)
            + 64.0 * z
            + x * (16.0 - 64.0 * z + y * (-16.0 + 64.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x * y * z * (-16.0 + y * (32.0 - 32.0 * z) + 16.0 * z)
        + x ** 2 * y * z * (16.0 - 16.0 * z + y * (-32.0 + 32.0 * z)),
        y
        * z
        * (
            -16.0
            + y * (32.0 - 32.0 * z)
            + 16.0 * z
            + x * (32.0 - 32.0 * z + y * (-64.0 + 64.0 * z))
        ),
        x
        * z
        * (
            -16.0
            + y * (64.0 - 64.0 * z)
            + 16.0 * z
            + x * (16.0 - 16.0 * z + y * (-64.0 + 64.0 * z))
        ),
        x
        * y
        * (
            -16.0
            + y * (32.0 - 64.0 * z)
            + 32.0 * z
            + x * (16.0 - 32.0 * z + y * (-32.0 + 64.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x ** 2
        * z
        * (
            -16.0
            + y * (48.0 - 48.0 * z)
            + 16.0 * z
            + y ** 2 * (-32.0 + 32.0 * z)
        )
        + x
        * z
        * (
            16.0
            + y ** 2 * (32.0 - 32.0 * z)
            - 16.0 * z
            + y * (-48.0 + 48.0 * z)
        ),
        z
        * (
            16.0
            + y ** 2 * (32.0 - 32.0 * z)
            - 16.0 * z
            + y * (-48.0 + 48.0 * z)
            + x
            * (
                -32.0
                + y * (96.0 - 96.0 * z)
                + 32.0 * z
                + y ** 2 * (-64.0 + 64.0 * z)
            )
        ),
        x
        * z
        * (
            -48.0
            + y * (64.0 - 64.0 * z)
            + 48.0 * z
            + x * (48.0 - 48.0 * z + y * (-64.0 + 64.0 * z))
        ),
        x
        * (
            16.0
            + y ** 2 * (32.0 - 64.0 * z)
            - 32.0 * z
            + y * (-48.0 + 96.0 * z)
            + x
            * (
                -16.0
                + y * (48.0 - 96.0 * z)
                + 32.0 * z
                + y ** 2 * (-32.0 + 64.0 * z)
            )
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x
        * y
        * (
            16.0
            - 48.0 * z
            + 32.0 * z ** 2
            + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
        )
        + x ** 2
        * y
        * (
            -16.0
            + 48.0 * z
            - 32.0 * z ** 2
            + y * (16.0 - 48.0 * z + 32.0 * z ** 2)
        ),
        y
        * (
            16.0
            - 48.0 * z
            + 32.0 * z ** 2
            + y * (-16.0 + 48.0 * z - 32.0 * z ** 2)
            + x
            * (
                -32.0
                + 96.0 * z
                - 64.0 * z ** 2
                + y * (32.0 - 96.0 * z + 64.0 * z ** 2)
            )
        ),
        x
        * (
            16.0
            - 48.0 * z
            + 32.0 * z ** 2
            + y * (-32.0 + 96.0 * z - 64.0 * z ** 2)
            + x
            * (
                -16.0
                + 48.0 * z
                - 32.0 * z ** 2
                + y * (32.0 - 96.0 * z + 64.0 * z ** 2)
            )
        ),
        x
        * y
        * (
            -48.0
            + y * (48.0 - 64.0 * z)
            + 64.0 * z
            + x * (48.0 - 64.0 * z + y * (-48.0 + 64.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + y ** 2
        * z
        * (
            -16.0
            + x * (48.0 - 48.0 * z)
            + 16.0 * z
            + x ** 2 * (-32.0 + 32.0 * z)
        )
        + y
        * z
        * (
            16.0
            + x ** 2 * (32.0 - 32.0 * z)
            - 16.0 * z
            + x * (-48.0 + 48.0 * z)
        ),
        y
        * z
        * (
            -48.0
            + y * (48.0 - 48.0 * z)
            + 48.0 * z
            + x * (64.0 - 64.0 * z + y * (-64.0 + 64.0 * z))
        ),
        z
        * (
            16.0
            - 16.0 * z
            + y * (-32.0 + 32.0 * z)
            + x * (-48.0 + y * (96.0 - 96.0 * z) + 48.0 * z)
            + x ** 2 * (32.0 - 32.0 * z + y * (-64.0 + 64.0 * z))
        ),
        y
        * (
            16.0
            - 32.0 * z
            + y * (-16.0 + 32.0 * z)
            + x * (-48.0 + y * (48.0 - 96.0 * z) + 96.0 * z)
            + x ** 2 * (32.0 - 64.0 * z + y * (-32.0 + 64.0 * z))
        ),
    ),
    lambda x, y, z: output(
        0.0
        + x ** 2 * y * z * (-64.0 + y * (64.0 - 64.0 * z) + 64.0 * z)
        + x * y * z * (64.0 - 64.0 * z + y * (-64.0 + 64.0 * z)),
        y
        * z
        * (
            64.0
            - 64.0 * z
            + y * (-64.0 + 64.0 * z)
            + x * (-128.0 + y * (128.0 - 128.0 * z) + 128.0 * z)
        ),
        x
        * z
        * (
            64.0
            - 64.0 * z
            + x * (-64.0 + y * (128.0 - 128.0 * z) + 64.0 * z)
            + y * (-128.0 + 128.0 * z)
        ),
        x
        * y
        * (
            64.0
            - 128.0 * z
            + y * (-64.0 + 128.0 * z)
            + x * (-64.0 + y * (64.0 - 128.0 * z) + 128.0 * z)
        ),
    ),
]


class ElementHex2(ElementH1):
    """Triquadratic element."""

    nodal_dofs = 1
    facet_dofs = 1
    edge_dofs = 1
    interior_dofs = 1
    maxdeg = 6
    dofnames = ["u", "u", "u", "u"]
    doflocs = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
            [1.0, 1.0, 0.5],  # edges
            [1.0, 0.5, 1.0],
            [0.5, 1.0, 1.0],
            [1.0, 0.5, 0.0],
            [0.5, 1.0, 0.0],
            [1.0, 0.0, 0.5],
            [0.5, 0.0, 1.0],
            [0.0, 1.0, 0.5],
            [0.0, 0.5, 1.0],
            [0.5, 0.0, 0.0],
            [0.0, 0.5, 0.0],
            [0.0, 0.0, 0.5],
            [1.0, 0.5, 0.5],  # facets
            [0.5, 0.5, 1.0],
            [0.5, 1.0, 0.5],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.5, 0.5],
        ]
    )
    refdom = RefHex

    def lbasis(self, X, i):

        if i >= 0 and i < 27:
            return _generated_basis[i](*X)

        self._index_error()
