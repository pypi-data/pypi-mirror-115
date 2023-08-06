from .init import boot, initialize, launch

def run(main_module):
    boot(False)
    initialize()
    launch(main_module)