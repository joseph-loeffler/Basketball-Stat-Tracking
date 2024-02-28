"""
Created on 5/12/23
@author: josephloeffler
"""
import globalVars as gV


class Controller:
    """
    Controller of MVC
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def main(self):
        self.view.main()

    def on_button_click(self, player, stat):
        if self.view.toggle_var.get():
            pm = -1
        else:
            pm = 1
        self.model.stat_plus_one(player, stat, pm)
        score0, score1 = self.model.get_score()
        self.view.update_score(score0, score1)
        self.view.update_selected_stat(player=player, stat=stat)

    def on_return_key(self, event, done_var):
        name = self.view.player_entry_var.get()
        if name and ((done_var == 1) or (done_var == 3)):
            if done_var == 1:
                self.model.log_player(gV.TEAM0, name)
            elif done_var == 3:
                self.model.log_player(gV.TEAM1, name)
            self.view.clear_entry()

    def on_done_click(self):
        done_var = self.view.done_var
        name = self.view.player_entry_var.get()

        if done_var == 0:
            gV.TEAM0 = name
            self.model.log_team(name)
            self.view.label_player_team_toggle()

            # Logging the team name as player to record team stats
            self.model.log_player(name, f"{name} (team)")
        elif done_var == 1:
            if name:
                self.model.log_player(gV.TEAM0, name)
            self.view.label_player_team_toggle()
        elif done_var == 2:
            gV.TEAM1 = name
            self.model.log_team(name)
            self.view.label_player_team_toggle()

            # Logging the team name as player to record team stats
            self.model.log_player(name, f"{name} (team)")
        elif done_var == 3:
            if name:
                self.model.log_player(gV.TEAM1, name)
            self.view.close_popup()
            roster0 = sorted(self.model.tps_dict[gV.TEAM0].keys())
            roster0 = sorted(roster0, key=lambda x: "(team)" not in x)
            roster1 = sorted(self.model.tps_dict[gV.TEAM1].keys())
            roster1 = sorted(roster1, key=lambda x: "(team)" not in x)
            self.view.create_roster_radios(roster0, roster1)
            self.view.create_score()

        self.view.done_var_plus_one()
        self.view.clear_entry()

    def on_finish_click(self):
        for player in [player.get() for player in
                       self.view.team0_sub_players_lst]:
            self.model.log_sub(player, 0, "OUT")
            print(player)
        for player in [player.get() for player in
                       self.view.team1_sub_players_lst]:
            self.model.log_sub(player, 0, "OUT")

        self.model.log_to_file()
        self.view.window_destroy()

    def on_sub_button_click(self):
        player = self.view.radio_var.get()
        if player in self.model.tps_dict[gV.TEAM0].keys():
            for var in self.view.team0_sub_players_lst:
                if self.view.sub_button_text_var.get() == "Sub In":
                    if var.get():
                        continue
                    else:  # SUB IN
                        var.set(player)
                        self.view.sub_button_text_var.set("Sub Out")
                        time = \
                            10 * 60 * int(self.view.time_dec_min.get()) + \
                            60 * int(self.view.time_ones_min.get()) + \
                            10 * int(self.view.time_dec_sec.get()) + \
                            int(self.view.time_ones_sec.get())
                        self.model.log_sub(player, time, "IN")

                elif self.view.sub_button_text_var.get() == "Sub Out":
                    if var.get() == player:  # SUB OUT
                        var.set('')
                        self.view.sub_button_text_var.set("Sub In")
                        time = \
                            10 * 60 * int(self.view.time_dec_min.get()) + \
                            60 * int(self.view.time_ones_min.get()) + \
                            10 * int(self.view.time_dec_sec.get()) + \
                            int(self.view.time_ones_sec.get())
                        self.model.log_sub(player, time, "OUT")
                    else:
                        continue
                break
        else:
            for var in self.view.team1_sub_players_lst:
                if self.view.sub_button_text_var.get() == "Sub In":
                    if var.get():
                        continue
                    else:  # SUB IN
                        var.set(player)
                        self.view.sub_button_text_var.set("Sub Out")
                        time = \
                            10 * 60 * int(self.view.time_dec_min.get()) + \
                            60 * int(self.view.time_ones_min.get()) + \
                            10 * int(self.view.time_dec_sec.get()) + \
                            int(self.view.time_ones_sec.get())
                        self.model.log_sub(player, time, "IN")

                elif self.view.sub_button_text_var.get() == "Sub Out":
                    if var.get() == player:  # SUB OUT
                        var.set('')
                        self.view.sub_button_text_var.set("Sub In")
                        time = \
                            10 * 60 * int(self.view.time_dec_min.get()) + \
                            60 * int(self.view.time_ones_min.get()) + \
                            10 * int(self.view.time_dec_sec.get()) + \
                            int(self.view.time_ones_sec.get())
                        self.model.log_sub(player, time, "OUT")
                    else:
                        continue
                break


if __name__ == '__main__':
    pass
