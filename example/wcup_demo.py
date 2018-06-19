# encoding: utf-8

from opendatatools import worldcup

if __name__ == '__main__':
    worldcup.set_proxies({"https" : "https://127.0.0.1:1080"})
    # 加载原始数据
    worldcup.load_data()

    # 夺冠次数排名
    # df = worldcup.get_champion_rank()

    # 参加决赛次数排名
    #df = worldcup.get_finalgame_rank()

    # 获胜场次排名
    # df = worldcup.get_wingame_rank()

    # 参加场次排名
    #df = worldcup.get_game_rank()

    # 参加届数排名
    # df = worldcup.get_year_rank()

    # 进球统计
    # df = worldcup.get_goal_stat()

    # 冠军进球统计
    # df = worldcup.get_champion_goal_stat()
    #print(df)

    # 冠军球队第一场比赛的情况统计
    #df_stat, df_detail = worldcup.get_champion_fistgame_stat()
    #print(df_stat)
    #print(df_detail)



