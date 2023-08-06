from abc import ABC

from typing import List
from policy.models import Policy, PolicyRenewal


class NotificationTriggerAbs(ABC):

    @classmethod
    def find_activated_policies(cls) -> List[type(Policy.id)]:
        raise NotImplementedError("find_new_activated_policies not implemented")

    @classmethod
    def find_newly_effective_policies(cls) -> List[type(Policy.id)]:
        raise NotImplementedError("find_new_effective_policies not implemented")

    @classmethod
    def find_renewed_policies(cls) -> List[type(Policy.id)]:
        raise NotImplementedError("find_newly_renewed_policies not implemented")

    @classmethod
    def find_soon_expiring_policies(cls) -> List[type(Policy.id)]:
        raise NotImplementedError("find_soon_expiring_policies not implemented")

    @classmethod
    def find_recently_expired_policies(cls) -> List[type(Policy.id)]:
        raise NotImplementedError("find_soon_expiring_policies not implemented")

    @classmethod
    def find_expiring_today_policies(cls) -> List[type(Policy.id)]:
        raise NotImplementedError("find_soon_expiring_policies not implemented")
