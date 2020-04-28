from typing import Optional

from src.main.util.log_util import log_and_raise_error
from src.main.solution_space.solution_graph import Vertex
from src.main.solution_space.data_classes import User, Profile
from src.main.solution_space.path_finder.path_finder import log
from src.main.canonicalization.diffs.diff_handler import IDiffHandler

class MeasuredVertex:
    def __init__(self, user_diff_handler: IDiffHandler, vertex: Vertex, user: User,
                 distance_to_user: Optional[int] = None):
        # Todo: add fine for rollback
        self._vertex = vertex
        self._distance_to_user = distance_to_user if distance_to_user \
            else vertex.get_diffs_number_to_vertex(user_diff_handler)
        # Todo: get actual vertex profile
        self._profile = self.__init_profile(user)
        self._users_count = len(vertex.get_unique_users())

    @property
    def vertex(self) -> Vertex:
        return self._vertex

    @property
    def distance_to_user(self) -> int:
        return self._distance_to_user

    @property
    def profile(self) -> Profile:
        return self._profile

    @property
    def users_count(self) -> int:
        return self._users_count

    def __init_profile(self, user: User) -> Profile:
        # Todo: add user handling
        return Profile()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MeasuredVertex):
            return False
        if self._distance_to_user != o.distance_to_user or self._profile == o.profile:
            return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __lt__(self, o: object):
        if not isinstance(o, MeasuredVertex):
            log_and_raise_error(f'The object {o} is not {self.__class__} class', log)
        if self._distance_to_user < o.distance_to_user:
            return True
        # Todo: use profile info
        return self._users_count < o.users_count
