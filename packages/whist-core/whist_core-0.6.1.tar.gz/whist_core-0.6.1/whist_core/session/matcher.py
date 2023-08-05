"""
Match making tool.
"""
import abc
import random

from whist_core.error.matcher_error import NotEnoughPlayersError
from whist_core.scoring.team import Team
from whist_core.session.userlist import UserList


# pylint: disable=too-few-public-methods
class Matcher(abc.ABC):
    """
    Abstrakt class for player to teams matching.
    """

    @staticmethod
    @abc.abstractmethod
    def distribute(num_teams: int, team_size: int, users: UserList) -> list[Team]:
        """
        Distributes cards according to subclass implementation.
        :param num_teams: the amount of teams
        :param team_size: how many players per team
        :param users: the user list at that table
        :return: the list of teams with players distributed to them
        """
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """
        Checks if the objects are of the same class.
        :param other: to be checked
        :return: True if same class else False
        """
        return isinstance(other, self.__class__)


class RoundRobinMatcher(Matcher):
    """
    Distributes the players in the order of the user list.
    """

    @staticmethod
    def distribute(num_teams: int, team_size: int, users: UserList) -> list[Team]:
        """
        Distributes one player to each team each round in order of the user list. Repeats until
        the user list is empty.
        :param num_teams: the amount of teams
        :param team_size: how many players per team
        :param users: the user list at that table
        :return: the teams in round robin distribution
        """
        if team_size <= 0:
            raise ValueError('The team size must be positive.')
        if num_teams <= 0:
            raise ValueError('There must be at least one team.')
        players = users.players
        if num_teams * team_size > len(players):
            raise NotEnoughPlayersError(f'{num_teams * team_size} of players are need, but only '
                                        f'{len(players)} have joined.')
        for _ in range(0, team_size):
            for team_id in range(0, num_teams):
                users.change_team(players.pop(0), team_id)

        return users.teams


class RandomMatcher(Matcher):
    """
    Distributes the players randomly to teams.
    """

    @staticmethod
    def distribute(num_teams: int, team_size: int, users: UserList) -> list[Team]:
        """
        For given parameter distributes the players to teams.
        :return: None
        :rtype: None
        """
        players = users.players
        teams: list = list(range(0, team_size)) * num_teams
        for player in players:
            team_id = random.choice(teams)  # nosec random
            users.change_team(player, team_id)
            teams.remove(team_id)
        return users.teams
