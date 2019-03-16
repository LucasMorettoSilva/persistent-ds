class Numbers:

    @staticmethod
    def non_zero(n):
        if n == 0:
            return 0
        i = 1
        for c in reversed(str(n)):
            if c != "0":
                return i
            i += 1

    @staticmethod
    def skew_binary(n):
        if n < 0:
            raise ValueError(
                "Expects positive number, got negative: {}".format(n))
        if n == 0:
            return 0
        remainder, digits = Numbers.__skew_binary(n, 1)
        number = ""
        for d in digits:
            number += str(d)
        return int(number)

    @staticmethod
    def __skew_binary(n, weight):
        if n < weight:
            return n, []
        rest, digits = Numbers.__skew_binary(n, 2 * weight + 1)
        if rest == 2 * weight:
            return 0, digits + [2]
        elif rest >= weight:
            return rest - weight, digits + [1]
        else:
            return rest, digits + [0]


