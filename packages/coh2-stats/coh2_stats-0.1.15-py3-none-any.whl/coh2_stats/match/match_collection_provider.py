from coh2_stats.match.match_page_collection import MatchPageCollection
from coh2_stats.match.match_collection import MatchCollection
from coh2_stats.match.match_collection_filter import *

import gc

class MatchCollectionProvider:

    def get_recent_match_collection(self, use_internet = True) -> MatchCollection:
        """
        recent: 
        - all traceable matches in player set
        - filter by playercard (at least one faction above 400)
        - 4vs4 only
        - longer than 5 minutes
        """
        from coh2_stats.leaderboard.leaderboard_collection import LeaderboardCollection
        lbc = LeaderboardCollection()
        lbc.add_elite_leaderboards(use_internet)
        lst = lbc.get_player_id_list()
        del lbc
        gc.collect()

        from coh2_stats.page_provider.personal_stat import PersonalStatPageProvider
        psp = PersonalStatPageProvider(lst)
        psp.load(use_internet)
        performance_pages = psp.get_performance_page_list()

        from coh2_stats.player.playercard_collection import PlayerCardCollection
        playercard_collection = PlayerCardCollection()
        playercard_collection.load_from_pages(performance_pages)

        from coh2_stats.page_provider.recent_match_page import RecentMatchPageProvider
        rmp = RecentMatchPageProvider(lst)
        rmp.load(use_internet)

        match_page_collection = MatchPageCollection(rmp.pages)
        result = match_page_collection.get_match_stats_list()

        recent_mc = MatchCollection("recent", result)
        recent_mc = recent_mc.filter_by_playercard_collection(playercard_collection)
        recent_mc.filter(four_vs_four_match)
        recent_mc.filter(lasts_longer_than_five_minutes)
        return recent_mc

"""
if True:
    mc = MatchCollection("recent")
    mc.load()
    mc.filter(both_team_must_have_at_least_one_arranged_team)
    mc.filter_to_today_only()
    print(mc)
print('end')
"""


