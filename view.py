"""
Created on 5/12/23
@author: josephloeffler
"""
import tkinter as tk
from tkinter import ttk
import globalVars as gV


class View:
    """
    View of MVC
    """
    def __init__(self, controller):
        self.controller = controller

        self.window = tk.Tk()
        self.window.geometry("1024x640")
        self.window.title("Basketball Stat Tracker 2.0")

        # Variables
        self.radio_var = tk.StringVar()
        self.done_var = 0
        self.entry_label_text = tk.StringVar()
        self.entry_label_text.set('Team')
        self.team0_score_var = tk.IntVar()
        self.team1_score_var = tk.IntVar()
        self.sub_button_text_var = tk.StringVar()
        self.sub_button_text_var.set("Sub In")

        self.team0_sub_players_lst = []
        for i in range(5):
            sub_player_var = tk.StringVar()
            sub_player_var.set('')
            self.team0_sub_players_lst.append(sub_player_var)

        self.team1_sub_players_lst = []
        for i in range(5):
            sub_player_var = tk.StringVar()
            sub_player_var.set('')
            self.team1_sub_players_lst.append(sub_player_var)

        self.toggle_var = tk.BooleanVar()

        # frames
        self._create_frames()

        # widgets
        self._create_stat_buttons()
        self._create_time()
        self._create_toggle()

        # popup
        self._create_popup()

        # finish button
        self._create_finish_button()

        # substitutions
        self._create_sub_buttons()
    
    def main(self):
        self.window.mainloop()

    def _create_frames(self):
        # Configure window grid
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=3)
        self.window.rowconfigure(2, weight=1)

        # Time frame
        self.time_frame = tk.Frame(self.window, bg="dark gray")
        self.time_frame.grid(row=0, column=0, sticky="nsew")
        self.time_frame.columnconfigure(0, weight=1)
        self.time_frame.columnconfigure(1, weight=0)
        self.time_frame.columnconfigure(2, weight=0)
        self.time_frame.columnconfigure(3, weight=0)
        self.time_frame.columnconfigure(4, weight=1)

        # Score frame
        self.score_frame = tk.Frame(self.window, bg="light gray")
        self.score_frame.grid(row=0, column=1, sticky="nsew")
        self.time_frame.rowconfigure(0, weight=1)
        self.time_frame.columnconfigure("all", weight=1)

        # Toggle frame
        self.toggle_frame = tk.Frame(self.window, bg="dark gray")
        self.toggle_frame.grid(row=0, column=2, sticky="nsew")
        self.time_frame.rowconfigure(0, weight=1)
        self.time_frame.columnconfigure(0, weight=1)

        # Buttons frame
        self.buttons_frame = tk.Frame(self.window, bg="blue")
        self.buttons_frame.grid(row=1, column=1, sticky="nsew")
        # making the grid in the buttons frame
        for i in range(len(gV.STATS)):
            self.buttons_frame.rowconfigure(index=i, weight=1)
        for j in range(len(gV.STATS[0]) * 2):
            self.buttons_frame.columnconfigure(index=j, weight=1)

        # Players frames
        self.left_players_frame = tk.Frame(self.window, bg="dark blue")
        self.left_players_frame.grid(row=1, column=0, sticky="nsew")
        self.right_players_frame = tk.Frame(self.window, bg="dark blue")
        self.right_players_frame.grid(row=1, column=2, sticky="nsew")
        self.time_frame.rowconfigure("all", weight=1)
        self.time_frame.columnconfigure(0, weight=1)

        # Substitutions frame
        self.sub_frame = tk.Frame(self.window, bg="gray")
        self.sub_frame.grid(row=2, columnspan=3, sticky="nsew")

    def _create_stat_buttons(self):
        """
        creates the buttons that will be used to enter stats, as well as the
        counters which are right next to the buttons
        """
        self.selected_stats_lst = []
        for i in range(len(gV.STATS)):
            for j in range(len(gV.STATS[i])):
                caption = gV.STATS[i][j]
                just_display_caption = gV.DISPLAY_STATS[i][j]
                self.stat_button = tk.Button(
                    self.buttons_frame,
                    height=1, width=1,
                    command=lambda x=caption: self.controller.on_button_click(
                        self.radio_var.get(), x),
                    text=just_display_caption
                )
                self.stat_button.grid(row=i, column=j*2, padx=10, pady=10,
                                      sticky=tk.NSEW)
                selected_stat = tk.IntVar()
                self.selected_stats_lst.append(selected_stat)
                self.stat_counter = tk.Label(self.buttons_frame,
                                             textvariable=selected_stat)
                self.stat_counter.grid(row=i, column=(j*2+1), padx=10, pady=10,
                                       sticky=tk.NSEW)

    def _create_time(self):
        """
        creates the time spin boxes
        """
        self.time_dec_min = ttk.Spinbox(self.time_frame, width=1, from_=0, to=6)
        self.time_dec_min.grid(row=0, column=0, padx=(0, 2), pady=5, sticky="e")

        self.time_ones_min = ttk.Spinbox(self.time_frame, width=1, from_=0,
                                         to=9)
        self.time_ones_min.grid(row=0, column=1, padx=(0, 2), pady=5,
                                sticky="w")

        colon = tk.Label(self.time_frame, text=":", width=1, bg="dark gray",
                         font=('Helvetica bold', 26))
        colon.grid(row=0, column=2, padx=(0, 0))

        self.time_dec_sec = ttk.Spinbox(self.time_frame, width=1, from_=0, to=6)
        self.time_dec_sec.grid(row=0, column=3, padx=(0, 2), pady=5, sticky="e")

        self.time_ones_sec = ttk.Spinbox(self.time_frame, width=1, from_=0,
                                         to=9)
        self.time_ones_sec.grid(row=0, column=4, padx=(0, 2), pady=5,
                                sticky="w")

    def create_score(self):
        """
        creates the score and team names
        """
        team0 = ttk.Label(self.score_frame, font=('Helvetica bold', 26),
                          text=gV.TEAM0)
        team0.grid(row=0, column=0)

        team0_score = ttk.Label(self.score_frame, font=('Helvetica bold', 26),
                                textvariable=self.team0_score_var)
        team0_score.grid(row=0, column=1)

        dash = ttk.Label(self.score_frame, font=('Helvetica bold', 26),
                         text="-")
        dash.grid(row=0, column=2)

        team1 = ttk.Label(self.score_frame, font=('Helvetica bold', 26),
                          text=gV.TEAM1)
        team1.grid(row=0, column=4)

        team1_score = ttk.Label(self.score_frame, font=('Helvetica bold', 26),
                                textvariable=self.team1_score_var)
        team1_score.grid(row=0, column=3)

    def _create_toggle(self):
        """
        creates the subtraction toggle
        """
        toggle = ttk.Checkbutton(self.toggle_frame, text="Subtraction Toggle",
                                 variable=self.toggle_var)
        toggle.grid(row=0, column=0)

    def _create_finish_button(self):
        self.finish_button = tk.Button(
            self.toggle_frame, text="Finished",
            command=lambda: self.controller.on_finish_click()
        )
        self.finish_button.grid(row=1, column=0)

    def create_roster_radios(self, roster0, roster1):
        # Left
        r = 0
        for player in roster0:
            radio = tk.Radiobutton(
                self.left_players_frame, text=player, value=player,
                command=self.update_stat_labels,
                variable=self.radio_var
            )
            radio.grid(row=r)
            r += 1

        # Right
        r = 0
        for player in roster1:
            radio = tk.Radiobutton(
                self.right_players_frame, text=player, value=player,
                command=self.update_stat_labels,
                variable=self.radio_var
            )
            radio.grid(row=r)
            r += 1

    def _create_popup(self):
        self.popup = tk.Toplevel(self.window)
        self.popup.title("Input Teams, Players")
        self.player_entry_var = tk.StringVar()

        self.entry_label = ttk.Label(self.popup,
                                     textvariable=self.entry_label_text)
        self.entry_label.pack(side="left")

        self.name_entry = ttk.Entry(self.popup,
                                    textvariable=self.player_entry_var,
                                    width=30)
        self.name_entry.pack(side="left")
        self.name_entry.bind(
            '<Return>', lambda event, done_var=self.done_var:
            self.controller.on_return_key(event, self.done_var)
        )

        self.done_button = ttk.Button(
            self.popup, text="Done",
            command=lambda: self.controller.on_done_click()
        )
        self.done_button.pack(side="left")

    def _create_sub_buttons(self):
        self.sub_button = ttk.Button(
            self.sub_frame, textvariable=self.sub_button_text_var,
            command=lambda: self.controller.on_sub_button_click()
        )
        self.sub_button.grid(row=0, column=5)

        for i in range(5):
            self.sub_label = tk.Label(
                self.sub_frame, textvariable=self.team0_sub_players_lst[i]
            )
            self.sub_label.grid(row=0, column=i, padx=5, pady=5)

        for i in range(5):
            self.sub_label = tk.Label(
                self.sub_frame, textvariable=self.team1_sub_players_lst[i]
            )
            self.sub_label.grid(row=0, column=i+6, padx=5, pady=5)
        self.sub_frame.columnconfigure(index="all", weight=1)
        self.sub_frame.rowconfigure(index=0, weight=1)

    def close_popup(self):
        self.popup.destroy()

    def clear_entry(self):
        self.player_entry_var.set('')

    def done_var_plus_one(self):
        self.done_var += 1

    def label_player_team_toggle(self):
        if self.entry_label_text.get() == "Team":
            self.entry_label_text.set("Player")
        elif self.entry_label_text.get() == "Player":
            self.entry_label_text.set("Team")

    def update_score(self, score0, score1):
        self.team0_score_var.set(score0)
        self.team1_score_var.set(score1)

    def update_selected_stat(self, player, stat):
        flat_stats_list = [stat for sublist in gV.STATS for stat in sublist]
        for i in range(len(flat_stats_list)):
            if flat_stats_list[i] == stat:
                new_value = 6969
                for team in gV.TPS_DICT.keys():
                    if player in gV.TPS_DICT[team].keys():
                        new_value = gV.TPS_DICT[team][player][stat]
                self.selected_stats_lst[i].set(new_value)

    def update_stat_labels(self):
        player = self.radio_var.get()
        flat_stats_list = [stat for sublist in gV.STATS for stat in sublist]
        for (var, stat) in zip(self.selected_stats_lst, flat_stats_list):
            for team in gV.TPS_DICT.keys():
                if player in gV.TPS_DICT[team].keys():
                    stat_num = gV.TPS_DICT[team][player][stat]
                    var.set(stat_num)

        if player in [player.get() for player in self.team0_sub_players_lst]:
            self.sub_button_text_var.set("Sub Out")
        elif player in self.team1_sub_players_lst:
            self.sub_button_text_var.set("Sub Out")
        else:
            self.sub_button_text_var.set("Sub In")

    def window_destroy(self):
        self.window.destroy()


if __name__ == '__main__':
    pass
