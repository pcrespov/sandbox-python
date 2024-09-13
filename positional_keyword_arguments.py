def foo(
    pos_only_no_default,  # Positional-only argument, no default
    /,  # All preceding are positional-only
    pos_or_kwarg_no_default,  # Can be passed either positionally or as a keyword, no default
    pos_or_kwarg_with_default="default_value",  # Can be passed either positionally or as a keyword, with default
    *,  # All following arguments are keyword-only
    kwarg_only_no_default,  # Keyword-only argument, no default
    kwarg_only_with_default="default_kwarg",  # Keyword-only argument, with default
):
    """
    A function demonstrating all combinations of positional-only, positional-or-keyword,
    and keyword-only arguments with and without default values.
    """
    print(f"pos_only_no_default: {pos_only_no_default}")
    print(f"pos_or_kwarg_no_default: {pos_or_kwarg_no_default}")
    print(f"pos_or_kwarg_with_default: {pos_or_kwarg_with_default}")
    print(f"kwarg_only_no_default: {kwarg_only_no_default}")
    print(f"kwarg_only_with_default: {kwarg_only_with_default}")


# Example calls:

# 1. Positional arguments only (default for pos_or_kwarg_with_default will be used)
foo(1, 3, kwarg_only_no_default=6)

# 2. Using positional arguments and keyword arguments (pos_or_kwarg_with_default will use its default value)
foo(1, 3, kwarg_only_no_default=6)

# 3. Passing both positional and keyword arguments explicitly (overriding defaults)
foo(
    1,
    3,
    "non_default",
    kwarg_only_no_default=6,
    kwarg_only_with_default="non_default_kwarg",
)

# 4. If you want to rely on more default values
foo(
    1, 3, kwarg_only_no_default=6
)  # pos_or_kwarg_with_default and kwarg_only_with_default use defaults


def bar(
    # pos_only_no_default,  # Positional-only argument, no default
    pos_only_with_default=None,  # Positional-only argument, with default
    /,  # All preceding are positional-only
    # pos_or_kwarg_no_default,     # Can be passed either positionally or as a keyword, no default NOT ALLOWED
    pos_or_kwarg_with_default="default_value",  # Can be passed either positionally or as a keyword, with default
    *,  # All following arguments are keyword-only
    kwarg_only_no_default,  # Keyword-only argument, no default
    kwarg_only_with_default="default_kwarg",  # Keyword-only argument, with default
):
    """
    A function demonstrating all combinations of positional-only, positional-or-keyword,
    and keyword-only arguments with and without default values.
    """
    # print(f"pos_only_no_default: {pos_only_no_default}")
    print(f"pos_only_with_default: {pos_only_with_default}")
    ## print(f"pos_or_kwarg_no_default: {pos_or_kwarg_no_default}")
    print(f"pos_or_kwarg_with_default: {pos_or_kwarg_with_default}")
    print(f"kwarg_only_no_default: {kwarg_only_no_default}")
    print(f"kwarg_only_with_default: {kwarg_only_with_default}")


# Example calls:

# 1. Positional arguments only (default for pos_only_with_default will be used)
bar(1, None, 3, kwarg_only_no_default=6)

# 2. Using positional arguments and keyword arguments (pos_or_kwarg_with_default will use its default value)
bar(1, 2, 3, kwarg_only_no_default=6)

# 3. Passing both positional and keyword arguments explicitly (overriding defaults)
# bar(1, 2, 3, 'non_default', kwarg_only_no_default=6, kwarg_only_with_default='non_default_kwarg')
bar(1, 2, 3, kwarg_only_no_default=6, kwarg_only_with_default="non_default_kwarg")

# 4. If you want to rely on more default values
bar(
    1, 2, 3, kwarg_only_no_default=6
)  # pos_or_kwarg_with_default and kwarg_only_with_default use defaults
