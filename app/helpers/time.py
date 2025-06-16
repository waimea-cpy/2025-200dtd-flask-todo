from datetime import datetime
from zoneinfo import ZoneInfo


def utc_timestamp_to_local(utc_timestamp_str, local_format="%a, %d/%m/%Y at %I:%M%p"):
    utc_dt = datetime.strptime(utc_timestamp_str, "%Y-%m-%d %H:%M:%S")
    utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to local timezone (Pacific/Auckland handles DST automatically)
    local_dt = utc_dt.astimezone(ZoneInfo("Pacific/Auckland"))

    # Format to a user-friendly string
    return local_dt.strftime(local_format)


def utc_timestamp_to_local_date(utc_timestamp_str):
    return utc_timestamp_to_local(utc_timestamp_str, "%d/%m/%Y")


def utc_timestamp_to_local_day(utc_timestamp_str):
    return utc_timestamp_to_local(utc_timestamp_str, "%a")


def utc_timestamp_to_local_time(utc_timestamp_str):
    return utc_timestamp_to_local(utc_timestamp_str, "%I:%M%p")


def register_datetime_handlers(app):
    # Register Jinja filters
    app.jinja_env.filters['localtimestamp'] = utc_timestamp_to_local
    app.jinja_env.filters['localdate']      = utc_timestamp_to_local_date
    app.jinja_env.filters['localday']       = utc_timestamp_to_local_day
    app.jinja_env.filters['localtime']      = utc_timestamp_to_local_time



def utc_timestamp(local_date_str, local_time_str="00:00:00"):
    # Assume input is in local timezone (e.g., Pacific/Auckland)
    local_tz = ZoneInfo("Pacific/Auckland")

    # If no seconds provided, add some
    if len(local_time_str) == 5:
        local_time_str += ":00"

    # Parse the combined date and time string
    local_dt_str = f"{local_date_str} {local_time_str}"
    local_dt = datetime.strptime(local_dt_str, "%Y-%m-%d %H:%M:%S")
    local_dt = local_dt.replace(tzinfo=local_tz)

    # Convert to UTC
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))

    # Format as UTC timestamp string
    return utc_dt.strftime("%Y-%m-%d %H:%M:%S")


def utc_timestamp_now():
    # Get date/time now
    local_dt = datetime.now()
    local_date_str = local_dt.strftime("%Y-%m-%d")
    local_time_str = local_dt.strftime("%H:%M:%S")

    # Convert to UTC
    return utc_timestamp(local_date_str, local_time_str)

