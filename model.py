"""
Created on 5/12/23
@author: josephloeffler
"""
import globalVars as gV
import csv
import json


class Model:
    """
    Model of MVC
    """
    def __init__(self):
        self.tps_dict = {}

    def log_team(self, team_name):
        self.tps_dict[team_name] = {}

    def log_player(self, team, name):
        names_lst = []
        for team in self.tps_dict.keys():
            for player in self.tps_dict[team].keys():
                names_lst.append(player)

        if name not in names_lst:
            self.tps_dict[team][name] = {}
            for stat_lst in gV.STATS:
                for stat in stat_lst:
                    self.tps_dict[team][name][stat] = 0
                self.tps_dict[team][name]["sub log"] = []

    def stat_plus_one(self, player, stat, pm):
        for team in self.tps_dict.keys():
            team_key = f"{team} (team)"
            if player in self.tps_dict[team].keys():
                if "(team)" in player:
                    self.tps_dict[team][team_key][stat] += pm*1
                else:
                    self.tps_dict[team][player][stat] += pm*1
                    self.tps_dict[team][team_key][stat] += pm*1
        gV.TPS_DICT = self.tps_dict

    def get_score(self):
        score0 = 0
        for stat, pt in [("FTMake", 1), ("2ptMake", 2), ("3ptMake", 3)]:
            score0 += pt * self.tps_dict[gV.TEAM0][f"{gV.TEAM0} (team)"][stat]

        score1 = 0
        for stat, pt in [("FTMake", 1), ("2ptMake", 2), ("3ptMake", 3)]:
            score1 += pt * self.tps_dict[gV.TEAM1][f"{gV.TEAM1} (team)"][stat]

        return score0, score1

    def log_sub(self, player, time, in_out):
        score0 = self.tps_dict[gV.TEAM0][f"{gV.TEAM0} (team)"]["FTMake"] + \
                 2 * self.tps_dict[gV.TEAM0][f"{gV.TEAM0} (team)"]["2ptMake"]\
                 + 3 * self.tps_dict[gV.TEAM0][f"{gV.TEAM0} (team)"]["3ptMake"]
        score1 = \
            self.tps_dict[gV.TEAM1][f"{gV.TEAM1} (team)"]["FTMake"] + \
            2 * self.tps_dict[gV.TEAM1][f"{gV.TEAM1} (team)"]["2ptMake"] + \
            3 * self.tps_dict[gV.TEAM1][f"{gV.TEAM1} (team)"]["3ptMake"]

        if player in self.tps_dict[gV.TEAM0].keys():
            tup = (time, in_out, score0 - score1)
            self.tps_dict[gV.TEAM0][player]["sub log"].append(tup)
        elif player in self.tps_dict[gV.TEAM1].keys():
            tup = (time, in_out, score1 - score0)
            self.tps_dict[gV.TEAM1][player]["sub log"].append(tup)

    def log_to_file(self):
        file0 = open(f"{gV.TEAM0} (vs. {gV.TEAM1})", 'w')
        lst0 = []

        for player in sorted(self.tps_dict[gV.TEAM0].keys()):
            app = self.tps_dict[gV.TEAM0][player]
            app["Name"] = player
            lst0.append(app)

        display_stats_labels = [
            "Name", "PTS", "FGM", "FGA", "FG%", "2PM", "2PA", "2FG%",
            "3PM", "3PA", "3FG%", "FTM", "FTA", "FT%", "AST", "TOV",
            "AST:TOV", "REB", "OREB", "BLK", "STL", "AND-1's and BONUS FT *trips* that don't end in an OREB", "PF", "TECH",
            "MINS", "+/-", "eFG%", "TOV%", "OREB%", "FT Rate (%)"
        ]

        display_stats_lst_dict = []

        for team in self.tps_dict.keys():
            player_lst = self.tps_dict[team].keys()
            player_lst = sorted(player_lst)
            player_lst = sorted(player_lst, key=lambda x: "(team)" in x)
            for player in player_lst:
                d = {}

                d["Name"] = player
                d["PTS"] = \
                    3 * self.tps_dict[team][player]["3ptMake"] + \
                    2 * self.tps_dict[team][player]["2ptMake"] + \
                    self.tps_dict[team][player]["FTMake"]
                d["FGM"] = \
                    self.tps_dict[team][player]["3ptMake"] + \
                    self.tps_dict[team][player]["2ptMake"]
                d["FGA"] = \
                    self.tps_dict[team][player]["3ptMake"] + \
                    self.tps_dict[team][player]["3ptMiss"] + \
                    self.tps_dict[team][player]["2ptMake"] + \
                    self.tps_dict[team][player]["2ptMiss"]
                if d["FGA"]:
                    d["FG%"] = d["FGM"] / d["FGA"]
                else:
                    d["FG%"] = "/"
                d["2PM"] = self.tps_dict[team][player]["2ptMake"]
                d["2PA"] = \
                    self.tps_dict[team][player]["2ptMake"] + \
                    self.tps_dict[team][player]["2ptMiss"]
                if d["2PA"]:
                    d["2FG%"] = d["2PM"] / d["2PA"]
                else:
                    d["2FG%"] = "/"
                d["3PM"] = self.tps_dict[team][player]["3ptMake"]
                d["3PA"] = \
                    self.tps_dict[team][player]["3ptMake"] + \
                    self.tps_dict[team][player]["3ptMiss"]
                if d["3PA"]:
                    d["3FG%"] = d["3PM"] / d["3PA"]
                else:
                    d["3FG%"] = "/"
                d["FTM"] = self.tps_dict[team][player]["FTMake"]
                d["FTA"] = \
                    self.tps_dict[team][player]["FTMake"] + \
                    self.tps_dict[team][player]["FTMiss"]
                if d["FTA"]:
                    d["FT%"] = d["FTM"] / d["FTA"]
                else:
                    d["FT%"] = "/"
                d["AST"] = self.tps_dict[team][player]["AST"]
                d["TOV"] = self.tps_dict[team][player]["TOV"]
                if d["TOV"]:
                    d["AST:TOV"] = d["AST"] / d["TOV"]
                else:
                    d["AST:TOV"] = "/"
                d["REB"] = \
                    self.tps_dict[team][player]["DREB"] + \
                    self.tps_dict[team][player]["OREB"]
                d["OREB"] = self.tps_dict[team][player]["OREB"]
                d["BLK"] = self.tps_dict[team][player]["BLK"]
                d["STL"] = self.tps_dict[team][player]["STL"]
                d["AND-1's and BONUS FT *trips* that don't end in an OREB"] = self.tps_dict[team][
                    player]["AND-1's and BONUS FT *trips* that don't end in an OREB"]
                d["PF"] = self.tps_dict[team][player]["PF"]
                d["TECH"] = self.tps_dict[team][player]["TECH"]
                sub_log = self.tps_dict[team][player]["sub log"]
                d["MINS"], d["+/-"] = self._convert_sub_log(sub_log)
                if d["FGA"]:
                    d["eFG%"] = ((d["FGM"]) + (0.5 * d["3PM"])) / d["FGA"]
                else:
                    d["eFG%"] = "/"

                if "(team)" in player:
                    if d["FGA"]:
                        d["FT Rate (%)"] = d["FTA"] / d["FGA"]
                    else:
                        d["FT Rate (%)"] = "/"
                    if d["FGA"] + (d["FTA"] * 0.44) + d["AST"] + d["TOV"]:
                        d["TOV%"] = d["TOV"] / (d["FGA"] + (d["FTA"] * 0.44) +
                                                d["AST"] + d["TOV"])
                    else:
                        d["TOV%"] = "/"
                    opp_dreb = None
                    for team_key in self.tps_dict.keys():
                        if team_key != team:
                            opp_dreb = self.tps_dict[team_key][
                                team_key + " (team)"]["DREB"]
                    if d["OREB"] + opp_dreb:
                        d["OREB%"] = d["OREB"] / (d["OREB"] + opp_dreb)
                    else:
                        d["OREB%"] = "/"

                display_stats_lst_dict.append(d)

        writer = csv.DictWriter(file0, fieldnames=display_stats_labels)
        writer.writeheader()
        writer.writerows(display_stats_lst_dict)

        dictionary = self.tps_dict
        with open('dictionaries.txt', 'a') as convert_file:
            convert_file.write(json.dumps(dictionary))

    @staticmethod
    def _convert_sub_log(sub_log):
        plus_minus = 0
        secs = 0

        time_in = 0
        diff_in = 0
        for tup in sub_log:
            if tup[1] == "IN":
                time_in = tup[0]
                diff_in = tup[2]
            if tup[1] == "OUT":
                time_out = tup[0]
                diff_out = tup[2]

                secs += (time_in - time_out)
                plus_minus += (diff_out - diff_in)

        return secs/60, plus_minus


if __name__ == '__main__':
    pass
