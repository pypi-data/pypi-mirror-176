from typing import Optional

from libddog.common.types import JsonDict


class MonitorOptions:
    def __init__(
        self,
        *,
        # enable_logs_sample,
        # escalation_message,
        evaluation_delay: Optional[int] = None,
        # group_retention_duration,
        groupby_simple_monitor: Optional[bool] = False,
        include_tags: Optional[bool] = True,
        # min_failure_duration,
        # min_location_failed,
        # new_group_delay,
        # no_data_timeframe,
        # notify_audit,
        # notify_by,  # TODO
        # notify_no_data,  # TODO
        # on_missing_data,  # TODO
        # renotify_interval,  # TODO
        # renotify_occurrences,  # TODO
        # renotify_statuses,
        # require_full_window,
        # scheduling_options,
        # threshold_windows,
        # thresholds,
        # timeout_h,
        # variables,
    ) -> None:
        self.evaluation_delay = evaluation_delay
        self.groupby_simple_monitor = groupby_simple_monitor
        self.include_tags = include_tags

    def as_dict(self) -> JsonDict:
        return {
            "evaluation_delay": self.evaluation_delay,
            "groupby_simple_monitor": self.groupby_simple_monitor,
            "include_tags": self.include_tags,
        }
