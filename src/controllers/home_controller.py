class HomeController:
    def __init__(self, home_view, main_controller):
        self.view = home_view
        self.main_controller = main_controller
        
        self.view.on_available.connect(self.main_controller.show_available_setup)
        self.view.on_history.connect(self.main_controller.show_history)
