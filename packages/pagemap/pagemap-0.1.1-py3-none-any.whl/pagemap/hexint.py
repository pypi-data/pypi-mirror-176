import click


class HexInt(click.ParamType):
    name = "hex integer"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
        except ValueError:
            self.fail(f"{value!r} is not a valid hex integer", param, ctx)
