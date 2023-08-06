from datetime import datetime


def check_date_range(
        date_from: str,
        date_to: str
) -> None:
    """ Check date range validity

    Args:
        date_from: the date from as %Y-%m-%d
        date_to: the date to as %Y-%m-%d

    Returns:
        None

    Raises:
        ValueError: Invalid date range
    """

    if datetime.strptime(date_from, "%Y-%m-%d") > datetime.strptime(date_to, "%Y-%m-%d"):
        raise ValueError(f"date_from={date_from} cannot occur later than date_to={date_to}")