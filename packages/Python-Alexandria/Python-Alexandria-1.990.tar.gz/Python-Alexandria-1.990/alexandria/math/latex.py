from alexandria.shell import print_color


def latex_eq(var, formula):
    """
    LaTeX equation wrap.
    """
    print_color(r"\begin{equation}", "blue")
    print_color(f"   {var} = {formula}", "blue")
    print_color(r"\end{equation}", "blue")


