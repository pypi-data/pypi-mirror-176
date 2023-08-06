from datetime import datetime, timedelta

from django.db.models import Q, Count, Max, F
from policy.models import Policy, PolicyRenewal
from itertools import groupby, chain
from collections import ChainMap
from policy_notification.apps import PolicyNotificationConfig
from policy_notification.models import IndicationOfPolicyNotificationsDetails

from policy_notification.notification_triggers.abstract_trigger import NotificationTriggerAbs


class NotificationTriggerEventDetectors(NotificationTriggerAbs):
    # Taken from config, it has to correspond to the time interval at which subsequent scheduled tasks are triggered.
    TIME_INTERVAL_HOURS = PolicyNotificationConfig.trigger_time_interval_hours
    FIRST_CALL_HOUR = PolicyNotificationConfig.trigger_first_call_hour
    LAST_CALL_HOUR = PolicyNotificationConfig.trigger_last_call_hour
    REMINDER_BEFORE_EXPIRY_DAYS = PolicyNotificationConfig.reminder_before_expiry_days
    REMINDER_AFTER_EXPIRY_DAYS = PolicyNotificationConfig.reminder_after_expiry_days

    @classmethod
    def find_activated_policies(cls):
        # active_in_period = NotificationTriggerEventDetectors.policies_activated_from(policies_from)
        return NotificationTriggerEventDetectors.all_activated_policies()

    @classmethod
    def find_renewed_policies(cls):
        return NotificationTriggerEventDetectors.all_renewed_policies()

    @classmethod
    def find_newly_effective_policies(cls):
        if cls.already_called():
            return []

        efficiency_day = datetime.now().date()
        ids = NotificationTriggerEventDetectors.policies_starting_from(efficiency_day=efficiency_day)
        return ids

    @classmethod
    def find_soon_expiring_policies(cls):
        if cls.already_called():
            return []

        expiry_date = datetime.now().date() \
                          + timedelta(days=cls.REMINDER_BEFORE_EXPIRY_DAYS)
        ids = NotificationTriggerEventDetectors.policies_expiring_without_renewal(expiry_date)
        return ids

    @classmethod
    def find_expiring_today_policies(cls):
        if cls.already_called():
            return []

        expiry_date = datetime.now().date()
        ids = NotificationTriggerEventDetectors.policies_expiring_without_renewal(expiry_date)
        return ids

    @classmethod
    def find_recently_expired_policies(cls):
        if cls.already_called():
            return []

        expiry_date = datetime.now().date() \
                          - timedelta(days=cls.REMINDER_AFTER_EXPIRY_DAYS)
        ids = NotificationTriggerEventDetectors.policies_expiring_without_renewal(expiry_date)
        return ids

    @classmethod
    def policies_activated_from(cls, from_time):
        active_and_alternated = NotificationTriggerEventDetectors\
            .__get_all_policies_after(from_time)\
            .filter(status=Policy.STATUS_ACTIVE)\
            .filter(~Q(stage=Policy.STAGE_RENEWED))\
            .all()

        # Id of last policy before time period
        return NotificationTriggerEventDetectors.__filter_activated_after_time(active_and_alternated, from_time)

    @classmethod
    def all_activated_policies(cls):
        active_and_alternated = NotificationTriggerEventDetectors\
            .__get_all_active()
        return NotificationTriggerEventDetectors.__filter_not_sent(active_and_alternated)

    @classmethod
    def all_renewed_policies(cls):
        active_and_alternated = NotificationTriggerEventDetectors\
            .__get_all_renewed()
        return NotificationTriggerEventDetectors.__filter_not_sent(active_and_alternated)

    @classmethod
    def policies_renewed_from(cls, from_time):
        active_and_alternated = NotificationTriggerEventDetectors\
            .__get_all_policies_after(from_time)\
            .filter(Q(stage=Policy.STAGE_RENEWED))

        return NotificationTriggerEventDetectors.__filter_activated_after_time(active_and_alternated, from_time)

    @classmethod
    def policies_starting_from(cls, efficiency_day=None, efficiency_scope=None):
        if efficiency_day:
            return Policy.objects\
                .filter(
                    effective_date=efficiency_day,
                    validity_to__isnull=True,
                    status=Policy.STATUS_ACTIVE
                ).values_list('id', flat=True)
        else:
            from_date, to_date = efficiency_scope
            return Policy.objects\
                .filter(
                    effective_date__gt=from_date,
                    effective_date__lte=to_date,
                    validity_to__isnull=True,
                    status=Policy.STATUS_ACTIVE
                ).values_list('id', flat=True)

    @classmethod
    def __filter_not_sent(cls, p):
        active_and_alternated = p\
            .filter(
                Q(indication_of_notifications__isnull=True)  # Not sent
                | Q(indication_of_notifications__activation_of_policy__isnull=True)  # Not sent
                | (  # Sent but failed
                    Q(indication_of_notifications__activation_of_policy=
                      PolicyNotificationConfig.UNSUCCESSFUL_NOTIFICATION_ATTEMPT_DATE) &
                    Q(indication_of_notifications__details__notification_type="activation_of_policy",
                      indication_of_notifications__details__status=
                      IndicationOfPolicyNotificationsDetails.SendIndicationStatus.NOT_SENT_DUE_TO_ERROR)
                )
            ).annotate(altered_column=F('id'))

        # Id of last policy before time period
        return NotificationTriggerEventDetectors\
            .__filter_activated_after_time(active_and_alternated,
                                           PolicyNotificationConfig.UNSUCCESSFUL_NOTIFICATION_ATTEMPT_DATE)
    @classmethod
    def __did_value_changed(cls, v):
        # V is iterator with single element containing information about current status and status in first
        # legacy record before given period
        unfolded = ChainMap(*v)
        legacy_id = unfolded.get('legacy_value', None)
        current_id = unfolded.get('current_value', None)

        if legacy_id is None:
            # Newly created record
            return True
        elif legacy_id != current_id:
            # Current status differs from status before period
            return True
        else:
            # Current status is the same as latest status before
            return False

    @staticmethod
    def __get_all_policies_after(date_from):
        return Policy.objects\
            .filter(validity_from__gte=date_from, validity_to__isnull=True)\
            .annotate(altered_column=F('id'))

    @staticmethod
    def __get_all_active():
        return Policy.objects.filter(validity_to__isnull=True, status=Policy.STATUS_ACTIVE)\
            .filter(~Q(stage=Policy.STAGE_RENEWED))

    @staticmethod
    def __get_all_renewed():
        return Policy.objects.filter(validity_to__isnull=True, status=Policy.STATUS_ACTIVE)\
            .filter(Q(stage=Policy.STAGE_RENEWED))

    @staticmethod
    def __get_latest_historical_policies_before(date_before, currently_valid_policies):
        last_before_alternation = Policy.objects \
            .filter(validity_to__gte=date_before, validity_from__lte=date_before,
                    legacy_id__in=currently_valid_policies.values_list('id', flat=True)) \
            .values('legacy_id') \
            .annotate(legacy_id_count=Count('legacy_id'), id_max=Max('id')) \
            .order_by()

        return Policy.objects\
            .filter(id__in=last_before_alternation.values_list('id_max', flat=True)) \
            .annotate(altered_column=F('legacy_id'))

    @staticmethod
    def __get_column_values_from_policy_queryset(policy_queryset, *columns):
        return policy_queryset.values(*columns)

    @classmethod
    def policies_expiring_without_renewal(cls, expiry_date):
        renewal_date = expiry_date + timedelta(days=1)

        expiring = Policy.objects\
            .filter(
                validity_to__isnull=True,
                expiry_date=expiry_date)

        not_renewed = []

        # Based on policy.services.insert_renewalse
        for policy in expiring:
            product = cls.__get_product_conversion(policy.product)
            following_policies = Policy.objects.filter(family_id=policy.family_id) \
                .filter(Q(product_id=policy.product_id) | Q(product_id=product.id)) \
                .filter(start_date__gte=renewal_date)
            if not following_policies.exists():
                not_renewed.append(policy)

        return [policy.id for policy in not_renewed]

    @staticmethod
    def __get_product_conversion(product):
        if not product.conversion_product_id:
            previous_products = []
            # Could also add a len(previous_products) < 20 but this avoids loops in the conversion_products
            while product not in previous_products and product.conversion_product:
                previous_products.append(product)
                product = product.conversion_product
        return product

    @staticmethod
    def __filter_activated_after_time(active_and_alternated, from_time):
        historic_policies_data = NotificationTriggerEventDetectors \
            .__get_latest_historical_policies_before(from_time, active_and_alternated)\
            .only('altered_column', 'status')\
            .values('altered_column', 'status')\
            .annotate(legacy_value=F('status'))\
            .all()

        latest = active_and_alternated\
            .only('altered_column', 'status')\
            .values('altered_column', 'status') \
            .annotate(current_value=F('status'))\
            .all()

        result_list = chain(latest, historic_policies_data)
        unique_results = groupby(result_list, key=lambda obj: obj['altered_column'])

        # Policies activated in latest period
        newly_activated = [
            k for k, v in unique_results if NotificationTriggerEventDetectors.__did_value_changed(v)
        ]
        return newly_activated

    @classmethod
    def already_called(cls):
        # Check if this event trigger was already called for given day
        now = datetime.now()
        trigger_delta = timedelta(hours=cls.TIME_INTERVAL_HOURS)

        if (now - trigger_delta).date() == datetime.today():
            return True
        else:
            return False

    @classmethod
    def first_call_in_day(cls):
        # if cls.TIME_INTERVAL_HOURS >= 24:
        #     return True
        now = datetime.now()
        # 1 minute added for compensating time spent previously on code execution
        offset = (now - timedelta(hours=cls.FIRST_CALL_HOUR, minutes=1)).date()
        return offset < now.date()

    @classmethod
    def assign_default_intervals(cls):
        # when called form scheduled task, this variables might be None instead of actual config.
        cls.TIME_INTERVAL_HOURS = PolicyNotificationConfig.trigger_time_interval_hours
        cls.FIRST_CALL_HOUR = PolicyNotificationConfig.trigger_first_call_hour
        cls.LAST_CALL_HOUR = PolicyNotificationConfig.trigger_last_call_hour
        cls.REMINDER_BEFORE_EXPIRY_DAYS = PolicyNotificationConfig.reminder_before_expiry_days
        cls.REMINDER_AFTER_EXPIRY_DAYS = PolicyNotificationConfig.reminder_after_expiry_days

