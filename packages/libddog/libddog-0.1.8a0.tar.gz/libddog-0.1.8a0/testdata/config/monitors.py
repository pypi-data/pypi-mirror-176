from typing import List

from monitors import qa_events, qa_metrics

from libddog.monitors import Monitor


def get_monitors() -> List[Monitor]:
    monitors = qa_events.get_monitors() + qa_metrics.get_monitors()

    return monitors
