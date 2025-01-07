class Cell:
    def __init__(self, button=None):
        self.is_mine = False
        self.mine_count = 0
        self.is_revealed = False
        self.button = button

    def reveal(self):
        """Revela a célula e atualiza o estado visual"""
        self.is_revealed = True
        self.update_visual_state()

    def show_mine(self):
        """Mostra a mina durante o game over"""
        self.button.configure(text="💣", state="disabled", bg="red")

    def update_visual_state(self):
        """Atualiza a aparênncia visual da célula de acordo com o seu estado"""
        if not self.button:
            return
            
        if self.is_revealed:
            if self.is_mine:
                self.show_mine()
            elif self.mine_count == 0:
                self.button.configure(text="", state="disabled", bg="lightgrey")
            else:
                self.button.configure(
                    text=str(self.mine_count),
                    state="disabled",
                    bg="lightgrey"
                )