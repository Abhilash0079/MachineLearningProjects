from pathlib import Path
from typing import Any


def extract_match_record(
    match_data: dict[str, Any],
    file_path: Path
) -> dict[str, Any]:
    """
    Extract match-level information from one cricket match JSON file.

    Parameters
    ----------
    match_data : dict
        Parsed cricket match JSON data.

    file_path : Path
        Path of the source JSON file.

    Returns
    -------
    dict
        One flattened match-level record.
    """

    info = match_data["info"]

    teams = info.get("teams", [])
    toss = info.get("toss", {})
    outcome = info.get("outcome", {})
    event = info.get("event", {})
    outcome_by = outcome.get("by", {})

    match_dates = info.get("dates", [])

    player_of_match = info.get("player_of_match", [])

    return {
        "match_id": file_path.stem,
        "season": info.get("season"),
        "match_date": (
            str(match_dates[0])
            if match_dates
            else None
        ),
        "city": info.get("city"),
        "venue": info.get("venue"),
        "match_type": info.get("match_type"),
        "gender": info.get("gender"),
        "team_type": info.get("team_type"),

        "team_1": (
            teams[0]
            if len(teams) > 0
            else None
        ),

        "team_2": (
            teams[1]
            if len(teams) > 1
            else None
        ),

        "toss_winner": toss.get("winner"),
        "toss_decision": toss.get("decision"),

        "winner": outcome.get("winner"),
        "win_by_runs": outcome_by.get("runs", 0),
        "win_by_wickets": outcome_by.get("wickets", 0),

        "result": outcome.get("result"),
        "method": outcome.get("method"),
        "eliminator": outcome.get("eliminator"),

        "player_of_match": (
            player_of_match[0]
            if player_of_match
            else None
        ),

        "event_name": event.get("name"),
        "event_match_number": event.get("match_number"),
        "event_group": event.get("group"),

        "overs": info.get("overs"),
        "balls_per_over": info.get(
            "balls_per_over",
            6
        ),

        "source_file": file_path.name,
    }


def extract_delivery_records(
    match_data: dict[str, Any],
    file_path: Path
) -> list[dict[str, Any]]:
    """
    Extract ball-by-ball delivery records from one match.

    One output record represents one delivery.

    Parameters
    ----------
    match_data : dict
        Parsed cricket match JSON data.

    file_path : Path
        Path of the source JSON file.

    Returns
    -------
    list[dict]
        Flattened delivery-level records.
    """

    records: list[dict[str, Any]] = []

    match_id = file_path.stem
    info = match_data["info"]

    season = info.get("season")
    teams = info.get("teams", [])

    match_dates = info.get("dates", [])

    match_date = (
        str(match_dates[0])
        if match_dates
        else None
    )

    innings_list = match_data.get(
        "innings",
        []
    )

    for innings_number, innings in enumerate(
        innings_list,
        start=1
    ):
        batting_team = innings.get("team")

        bowling_team = next(
            (
                team
                for team in teams
                if team != batting_team
            ),
            None
        )

        target = innings.get("target", {})

        target_runs = target.get("runs")
        target_overs = target.get("overs")

        for over_data in innings.get(
            "overs",
            []
        ):
            over_number = over_data.get("over")

            deliveries = over_data.get(
                "deliveries",
                []
            )

            for delivery_number, delivery in enumerate(
                deliveries,
                start=1
            ):
                runs = delivery.get(
                    "runs",
                    {}
                )

                extras = delivery.get(
                    "extras",
                    {}
                )

                wickets = delivery.get(
                    "wickets",
                    []
                )

                first_wicket = (
                    wickets[0]
                    if wickets
                    else {}
                )

                batter_runs = runs.get(
                    "batter",
                    0
                )

                extra_runs = runs.get(
                    "extras",
                    0
                )

                total_runs = runs.get(
                    "total",
                    0
                )

                wide_runs = extras.get(
                    "wides",
                    0
                )

                no_ball_runs = extras.get(
                    "noballs",
                    0
                )

                bye_runs = extras.get(
                    "byes",
                    0
                )

                leg_bye_runs = extras.get(
                    "legbyes",
                    0
                )

                penalty_runs = extras.get(
                    "penalty",
                    0
                )

                is_legal_delivery = (
                    wide_runs == 0
                    and no_ball_runs == 0
                )

                fielders = first_wicket.get(
                    "fielders",
                    []
                )

                fielder = (
                    fielders[0].get("name")
                    if fielders
                    else None
                )

                is_wicket = bool(wickets)

                dismissal_kind = (
                    first_wicket.get("kind")
                )

                is_bowler_wicket = (
                    is_wicket
                    and dismissal_kind
                    not in {
                        "run out",
                        "retired hurt",
                        "retired out",
                        "obstructing the field",
                    }
                )

                records.append({
                    "match_id": match_id,
                    "season": season,
                    "match_date": match_date,

                    "innings": innings_number,
                    "batting_team": batting_team,
                    "bowling_team": bowling_team,

                    "target_runs": target_runs,
                    "target_overs": target_overs,

                    "over": over_number,
                    "delivery_number": delivery_number,

                    "ball": (
                        f"{over_number}."
                        f"{delivery_number}"
                    ),

                    "batter": delivery.get(
                        "batter"
                    ),

                    "non_striker": delivery.get(
                        "non_striker"
                    ),

                    "bowler": delivery.get(
                        "bowler"
                    ),

                    "batter_runs": batter_runs,
                    "extra_runs": extra_runs,
                    "total_runs": total_runs,

                    "wide_runs": wide_runs,
                    "no_ball_runs": no_ball_runs,
                    "bye_runs": bye_runs,
                    "leg_bye_runs": leg_bye_runs,
                    "penalty_runs": penalty_runs,

                    "is_legal_delivery": int(
                        is_legal_delivery
                    ),

                    "is_dot_ball": int(
                        total_runs == 0
                    ),

                    "is_four": int(
                        batter_runs == 4
                    ),

                    "is_six": int(
                        batter_runs == 6
                    ),

                    "is_boundary": int(
                        batter_runs in {4, 6}
                    ),

                    "is_wicket": int(
                        is_wicket
                    ),

                    "is_bowler_wicket": int(
                        is_bowler_wicket
                    ),

                    "wickets_on_delivery": len(
                        wickets
                    ),

                    "player_dismissed": (
                        first_wicket.get(
                            "player_out"
                        )
                    ),

                    "dismissal_kind": (
                        dismissal_kind
                    ),

                    "fielder": fielder,

                    "source_file": file_path.name,
                })

    return records


def extract_player_records(
    match_data: dict[str, Any],
    file_path: Path
) -> list[dict[str, Any]]:
    """
    Extract players participating in one cricket match.

    One output record represents one player's participation
    in one match.

    Parameters
    ----------
    match_data : dict
        Parsed cricket match JSON data.

    file_path : Path
        Path of the source JSON file.

    Returns
    -------
    list[dict]
        Player participation records.
    """

    records: list[dict[str, Any]] = []

    info = match_data["info"]

    match_id = file_path.stem
    season = info.get("season")

    players_by_team = info.get(
        "players",
        {}
    )

    registry = info.get(
        "registry",
        {}
    )

    people_registry = registry.get(
        "people",
        {}
    )

    for team_name, players in players_by_team.items():
        for player_name in players:
            records.append({
                "match_id": match_id,
                "season": season,
                "team": team_name,
                "player_name": player_name,
                "player_registry_id": (
                    people_registry.get(
                        player_name
                    )
                ),
                "source_file": file_path.name,
            })

    return records