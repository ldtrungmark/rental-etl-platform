from datetime import datetime, timezone


def get_unix_timestamp_of_day(target_date: datetime = None):
    """Get unix timestamp of target day."""
    if target_date is None:
        target_date = datetime.now()

    start_of_day = datetime(target_date.year, target_date.month, target_date.day, tzinfo=timezone.utc)
    return int(start_of_day.timestamp())
