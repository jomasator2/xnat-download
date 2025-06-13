import pytest
import json
import csv
from pathlib import Path
from xnat_downloader.__main__ import load_projects_and_subjects

def test_load_projects_and_subjects_json(tmp_path):
    print(tmp_path)
    # Crear un archivo JSON de prueba
    json_data = {
        "project_id": {
            "p001": {
                "subject_id": {
                    "s001": {"session_id": ["ses-01", "ses-02"]},
                    "s002": {"session_id": ["ses-01"]}
                }
            }
        }
    }
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
        json.dump(json_data, f)

    # Ejecutar la función
    result = load_projects_and_subjects(json_file, "project_id", "subject_id", "session_id")

    # Verificar el resultado
    assert "p001" in result["projects"]
    assert "s001" in result["projects"]["p001"]["subjects"]
    assert "ses-01" in result["projects"]["p001"]["subjects"]["s001"]["sessions"]

def test_load_projects_and_subjects_csv(tmp_path):
    # Crear un archivo CSV de prueba
    csv_data = [
        {"project_id": "p001", "subject_id": "s001", "session_id": "ses-01"},
        {"project_id": "p001", "subject_id": "s001", "session_id": "ses-02"},
        {"project_id": "p001", "subject_id": "s002", "session_id": "ses-01"}
    ]
    csv_file = tmp_path / "test.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["project_id", "subject_id", "session_id"])
        writer.writeheader()
        writer.writerows(csv_data)

    # Ejecutar la función
    result = load_projects_and_subjects(csv_file, "project_id", "subject_id", "session_id")

    # Verificar el resultado
    assert "p001" in result["projects"]
    assert "s001" in result["projects"]["p001"]["subjects"]
    assert "ses-01" in result["projects"]["p001"]["subjects"]["s001"]["sessions"]

def test_load_projects_and_subjects_empty_file(tmp_path):
    # Crear un archivo vacío
    empty_file = Path() / "empty.json"
    empty_file.touch()
    assert empty_file.stat().st_size == 0
    # Verificar que se lanza un ValueError
    with pytest.raises(ValueError, match="The provided file is empty."):
        load_projects_and_subjects(empty_file, "project_id", "subject_id", "session_id")

def test_load_projects_and_subjects_invalid_format(tmp_path):
    # Crear un archivo con formato no soportado
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("This is not a valid format.")

    # Verificar que se lanza un ValueError
    with pytest.raises(ValueError, match="Unsupported file format. Please use JSON, CSV, or TSV."):
        load_projects_and_subjects(invalid_file, "project_id", "subject_id", "session_id")