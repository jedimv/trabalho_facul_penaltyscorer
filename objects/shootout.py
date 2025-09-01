import random

class ShootoutManager:
    def __init__(self, player_team_name, ia_team_name="Bot", max_rounds=5):
        self.player_team_name = player_team_name
        self.ia_team_name = ia_team_name
        self.max_rounds = max_rounds

        self.round = 1
        self.player_score = 0
        self.ia_score = 0

        # Define aleatoriamente quem começa chutando
        self.current_shooter = random.choice([self.player_team_name, self.ia_team_name])
        self.waiting_next = False

    def player_chute(self, foi_gol: bool):
        """Chute do jogador"""
        if self.current_shooter != self.player_team_name:
            return

        if foi_gol:
            self.player_score += 1

        self.prepare_next_turn()

    def ia_chute(self, foi_gol: bool):
        """Chute da IA"""
        if self.current_shooter != self.ia_team_name:
            return

        if foi_gol:
            self.ia_score += 1

        self.prepare_next_turn()

    def prepare_next_turn(self):
        """Alterna o turno e prepara próxima rodada"""
        if self.current_shooter == self.player_team_name:
            self.current_shooter = self.ia_team_name
        else:
            self.current_shooter = self.player_team_name

        # Se a rodada foi completada (os dois chutaram), incrementa round
        if self.current_shooter == self.player_team_name:
            self.round += 1

        if self.round > self.max_rounds:
            self.end_shootout()

    def end_shootout(self):
        if self.player_score > self.ia_score:
            print(f"Jogador venceu {self.player_score} x {self.ia_score}")
        elif self.ia_score > self.player_score:
            print(f"IA venceu {self.player_score} x {self.ia_score}")
        else:
            print(f"Empate! Morte súbita.")
            self.max_rounds += 1  # aumenta rounds para morte súbita
