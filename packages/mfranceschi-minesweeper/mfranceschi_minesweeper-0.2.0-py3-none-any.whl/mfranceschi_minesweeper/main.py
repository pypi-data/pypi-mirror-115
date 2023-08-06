# ENTRY POINT

from .controller.controller_impl import ControllerImpl
from .view.gui_impl import GUIImpl


def main() -> None:
    controller = ControllerImpl()
    gui = GUIImpl(
        grid_dim=controller.difficulty.grid_dim,
        controller=controller
    )
    controller.init_gui(gui)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
