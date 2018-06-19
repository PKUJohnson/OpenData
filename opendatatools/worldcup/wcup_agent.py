# encoding: utf-8

from opendatatools.common import RestAgent
import io
import pandas as pd


class WorldCupAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

        self._data_df = None

    def load_data(self):
        url = 'https://github.com/PKUJohnson/OpenData/raw/master/3rd/WorldCupMatches.xls'
        response = self.do_request(url, None, method='GET', type='binary')
        if response is not None:
            excel = pd.ExcelFile(io.BytesIO(response))
            self._data_df = excel.parse('WorldCupMatches').dropna()
            return self._data_df

        return None

    def _get_winner(self, row):
        team1 = row['Home Team Name']
        score1 = row['Home Team Goals']
        team2 = row['Away Team Name']
        score2 = row['Away Team Goals']
        win_cond = row['Win conditions']

        if score1 > score2:
            winner = team1
        elif score1 < score2:
            winner = team2
        else:
            winner = win_cond.split(" ")[0]

        return winner

    def _get_goal_stat(self, df):
        goal  = 0
        games = 0
        for index, row in df.iterrows():
            score1 = row['Home Team Goals']
            score2 = row['Away Team Goals']

            goal  = goal + score2 + score1
            games = games + 1

        return goal, games, goal/games

    def _get_champion_team(self):
        df_final = self._data_df[self._data_df.Stage == 'Final']
        dict_champion = {}
        for index, row in df_final.iterrows():
            year     = row['Year']
            champion = self._get_winner(row)
            dict_champion[year] = champion

        # 1950 年没有决赛
        dict_champion[1950] = 'Uruguay'
        return dict_champion

    def get_champion_rank(self):
        _get_champion_team = self._get_champion_team()
        dict_chanpion = {}
        for year, champion in _get_champion_team.items():
            if champion in dict_chanpion:
                dict_chanpion[champion] = dict_chanpion[champion] + 1
            else:
                dict_chanpion[champion] = 1

        df = pd.DataFrame(dict_chanpion, index = [0]).T
        df.columns = ['number of champions']
        df.sort_values('number of champions', ascending=False, inplace=True)
        return df

    def get_finalgame_rank(self):
        df_final = self._data_df[self._data_df.Stage == 'Final']
        dict_game = {}
        for index, row in df_final.iterrows():
            team1 = row['Home Team Name']
            team2 = row['Away Team Name']

            if team1 in dict_game:
                dict_game[team1] = dict_game[team1] + 1
            else:
                dict_game[team1] = 1

            if team2 in dict_game:
                dict_game[team2] = dict_game[team2] + 1
            else:
                dict_game[team2] = 1

        df = pd.DataFrame(dict_game, index=[0]).T
        df.columns = ['number of final games']
        df.sort_values('number of final games', ascending=False, inplace=True)
        return df

    def get_wingame_rank(self):
        dict_winner = {}
        for index, row in self._data_df.iterrows():
            winner = self._get_winner(row)
            if winner.strip() == '':
                continue

            if winner in dict_winner:
                dict_winner[winner] = dict_winner[winner] + 1
            else:
                dict_winner[winner] = 1

        df = pd.DataFrame(dict_winner, index = [0]).T
        df.columns = ['number of win games']
        df.sort_values('number of win games', ascending=False, inplace=True)
        return df

    def get_game_rank(self):
        dict_game = {}
        for index, row in self._data_df.iterrows():
            team1 = row['Home Team Name']
            team2 = row['Away Team Name']

            if team1 in dict_game:
                dict_game[team1] = dict_game[team1] + 1
            else:
                dict_game[team1] = 1

            if team2 in dict_game:
                dict_game[team2] = dict_game[team2] + 1
            else:
                dict_game[team2] = 1

        df = pd.DataFrame(dict_game, index=[0]).T
        df.columns = ['number of games']
        df.sort_values('number of games', ascending=False, inplace=True)
        return df

    def get_year_rank(self):
        dict_year = {}
        for index, row in self._data_df.iterrows():
            year  = row['Year']
            team1 = row['Home Team Name']
            team2 = row['Away Team Name']

            if team1 in dict_year:
                dict_year[team1].add(year)
            else:
                dict_year[team1] = {year}

            if team2 in dict_year:
                dict_year[team2].add(year)
            else:
                dict_year[team2] = {year}

        dict_year_num = {k :len(v) for k,v in dict_year.items()}

        df = pd.DataFrame(dict_year_num, index=[0]).T
        df.columns = ['number of year']
        df.sort_values('number of year', ascending=False, inplace=True)
        return df

    def _get_game_stat(self, df, team):
        dict_stat = {}
        for index, row in df.iterrows():
            team1 = row['Home Team Name']
            team2 = row['Away Team Name']
            if team1 == team or team2 == team:
                winner = self._get_winner(row)
                if winner == team:
                    stat = (1, 0, 0)
                elif winner == '':
                    stat = (0, 1, 0)
                else:
                    stat = (0, 0, 1)

                if team in dict_stat:
                    old_stat = dict_stat[team]
                    dict_stat[team] = (stat[0] + old_stat[0], stat[1] + old_stat[1], stat[2] + old_stat[2])

        return dict_stat

    def get_champion_stat(self):
        dict_champion_stat = []
        dict_champion = self._get_champion_team()
        for year, champion in dict_champion:
            df = self._data_df[self._data_df.Year == year]
            dict_stat = self._get_game_stat(df, champion)
            dict_champion_stat.append({
                'year' : year,
                'champion' : champion,
                'num of win'  : dict_stat[0],
                'num of tie'  : dict_stat[1],
                'num of loss' : dict_stat[2],
            })


        return dict_champion_stat

    def _get_firstgame_stat(self, df, team):

        for index, row in df.iterrows():
            year   = row['Year']
            team1  = row['Home Team Name']
            team2  = row['Away Team Name']
            score1 = row['Home Team Goals']
            score2 = row['Away Team Goals']
            win_cond = row['Win conditions']

            if team1 == team or team2 == team:
                winner = self._get_winner(row)
                if winner == team:
                    stat = '胜'
                elif winner == '':
                    stat = '平'
                else:
                    stat = '负'

                detail = {'year': year, 'team1' : team1, 'team2': team2, 'score': '%s : %s' % (score1, score2), 'result' : stat}
                return stat, detail

        return None, None


    def get_champion_fistgame_stat(self):
        dict_champion_fistgame_stat = {}
        list_champion_fistgame_detail = []
        dict_champion = self._get_champion_team()
        for year, champion in dict_champion.items():
            df = self._data_df[self._data_df.Year == year]
            stat, detail = self._get_firstgame_stat(df, champion)

            if stat in dict_champion_fistgame_stat:
                dict_champion_fistgame_stat[stat] = dict_champion_fistgame_stat[stat] + 1
            else:
                dict_champion_fistgame_stat[stat] = 1

            list_champion_fistgame_detail.append(detail)

        return pd.DataFrame([{'result' : k, 'num of games' : v} for k,v in dict_champion_fistgame_stat.items()]), pd.DataFrame(list_champion_fistgame_detail)

    def get_goal_stat(self):
        start_year = 1934
        end_year   = 2018
        list_goal_stat = []
        for year in range(start_year, end_year, 4):
            df = self._data_df[self._data_df.Year == year]
            if len(df) > 0:
                goal, games, avg_goal = self._get_goal_stat(df)
                list_goal_stat.append({'year': year, 'goal' : goal, 'games' : games, 'avg_goal': avg_goal})

        df = pd.DataFrame(list_goal_stat)
        df.sort_values('year', inplace=True)
        return df

    def _get_goal_stat_team(self, df, team):
        goal  = 0
        lose  = 0
        games = 0
        for index, row in df.iterrows():
            team1 = row['Home Team Name']
            team2 = row['Away Team Name']
            score1 = row['Home Team Goals']
            score2 = row['Away Team Goals']

            if team1 == team or team2 == team:
                if team1 == team:
                    goal = goal + score1
                    lose = lose + score2
                else:
                    goal = goal + score2
                    lose = lose + score1

                games = games + 1

        return goal, lose, games, goal/games, lose/games

    def get_champion_goal_stat(self):
        list_champion_goal_stat = []
        dict_champion = self._get_champion_team()
        for year, champion in dict_champion.items():
            df = self._data_df[self._data_df.Year == year]
            goal, lose, games, avg_goal, avg_lose = self._get_goal_stat_team(df, champion)

            list_champion_goal_stat.append({'year': year,
                                            'champion' : champion,
                                            'goal' : goal,
                                            'lose' : lose,
                                            'games': games,
                                            'avg_goal' : avg_goal,
                                            'avg_lose' : avg_lose,}
                                           )

        df = pd.DataFrame(list_champion_goal_stat)
        df.sort_values('year', inplace=True)

        return df