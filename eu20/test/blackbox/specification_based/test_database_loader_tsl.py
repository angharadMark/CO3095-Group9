import json
from database.database_loader import DatabaseLoader


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)


# DL_T1
def test_DL_T1_missing_file_returns_empty_db(tmp_path):
    missing = tmp_path / "missing.json"
    db = DatabaseLoader().load(str(missing))
    assert db is not None
    assert len(db.films) == 0


# DL_T2
def test_DL_T2_invalid_json_returns_empty_db(tmp_path):
    p = tmp_path / "films.json"
    with open(p, "w", encoding="utf-8") as f:
        f.write("{ bad json")

    db = DatabaseLoader().load(str(p))
    assert db is not None
    assert len(db.films) == 0


# DL_T3
def test_DL_T3_valid_empty_list(tmp_path):
    p = tmp_path / "films.json"
    write_json(p, [])
    db = DatabaseLoader().load(str(p))
    assert len(db.films) == 0


# DL_T4
def test_DL_T4_single_film_minimal(tmp_path):
    p = tmp_path / "films.json"
    write_json(p, [{"name": "Film A", "year": 2020}])

    db = DatabaseLoader().load(str(p))
    assert len(db.films) == 1
    assert db.films[0].name == "Film A"


# DL_T5
def test_DL_T5_invalid_cast_entries_ignored(tmp_path):
    p = tmp_path / "films.json"
    write_json(p, [{
        "name": "Film A",
        "year": 2020,
        "cast": [
            "bad",
            {"actor": "", "role": "Lead"},
            {"actor": "A1", "role": ""}
        ]
    }])

    db = DatabaseLoader().load(str(p))
    assert len(db.films) == 1
    assert len(db.films[0].cast) == 0


# DL_T6
def test_DL_T6_duplicate_cast_removed(tmp_path):
    p = tmp_path / "films.json"
    write_json(p, [{
        "name": "Film A",
        "year": 2020,
        "cast": [
            {"actor": "A1", "role": "Lead"},
            {"actor": "A1", "role": "Lead"}
        ]
    }])

    db = DatabaseLoader().load(str(p))
    assert len(db.films[0].cast) == 1


# DL_T7
def test_DL_T7_actor_reused_across_films(tmp_path):
    p = tmp_path / "films.json"
    write_json(p, [
        {"name": "Film A", "year": 2020, "cast": [{"actor": "A1", "role": "Lead"}]},
        {"name": "Film B", "year": 2021, "cast": [{"actor": "A1", "role": "Lead"}]},
    ])

    db = DatabaseLoader().load(str(p))
    actors = [a for a in db.actors if a.name == "A1"]
    assert len(actors) == 1
