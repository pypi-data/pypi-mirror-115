import click


class ProfileContext:

    def __init__(self):
        self._profile = None

    def set_profile(self, profile: str):
        if self._profile:
            raise click.UsageError("Unsuitable usage: `-p`, `--profile` can only be provided once")
        self._profile = profile

    def get_profile(self):
        return self._profile


class MutuallyExclusiveOption(click.Option):

    def __init__(self, *args: list, **kwargs: dict):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = (f"{help}\n\nNOTE: This argument is mutually exclusive to arguments: [{ex_str}].")
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            ex_str = ", ".join(self.mutually_exclusive)
            raise click.UsageError(f"Unsuitable usage: `{self.name}` is mutually exclusive to arguments `{ex_str}`")
        return super().handle_parse_result(ctx, opts, args)
