from pyargos.element import ArgosElement


class ArgosSeparator(ArgosElement):
    def to_argos(self) -> str:
        return "---"
