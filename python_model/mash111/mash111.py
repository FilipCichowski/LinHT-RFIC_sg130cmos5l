class Mash111:
    def __init__(self, width: int = 20) -> None:
        if type(width) is not int:
            raise TypeError("width must be an integer")
        if width < 1:
            raise ValueError("width must be positive")

        self.width = width
        self.modulus = 1 << width
        self.mask = self.modulus - 1
        self.reset()

    def reset(self) -> None:
        self._acc1 = 0
        self._acc2 = 0
        self._acc3 = 0

        self._c1_d1 = 0
        self._c1_d2 = 0
        self._c2_d1 = 0
        self._c2_d2 = 0
        self._c3_d1 = 0
        self._c3_d2 = 0

    @property
    def accumulators(self) -> tuple[int, int, int]:
        """Return the three unsigned accumulator states for diagnostics."""
        return self._acc1, self._acc2, self._acc3

    def step(self, frac_word: int) -> int:
        """Advance one clock cycle and return the signed divider offset.
        frac_word: Fractional division word in [0, 2**width).
        Returns signed integer in the range [-3, 4]."""
        if type(frac_word) is not int:
            raise TypeError("frac_word must be an integer")
        if not 0 <= frac_word < self.modulus:
            raise ValueError("frac_word is outside the configured width")

        sum1 = self._acc1 + frac_word
        sum2 = self._acc2 + self._acc1
        sum3 = self._acc3 + self._acc2

        carry1 = sum1 >> self.width
        carry2 = sum2 >> self.width
        carry3 = sum3 >> self.width

        output = (
            self._c1_d2
            + self._c2_d1
            - self._c2_d2
            + carry3
            - 2 * self._c3_d1
            + self._c3_d2
        )

        self._acc1 = sum1 & self.mask
        self._acc2 = sum2 & self.mask
        self._acc3 = sum3 & self.mask

        self._c1_d2, self._c1_d1 = self._c1_d1, carry1
        self._c2_d2, self._c2_d1 = self._c2_d1, carry2
        self._c3_d2, self._c3_d1 = self._c3_d1, carry3

        return output
