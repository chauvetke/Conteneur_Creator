import pytest
import platform
from conteneurcreator import detect_os, is_docker_installed, create_container
import subprocess

def test_detect_os():
    os_detected = detect_os()
    assert os_detected in ["Linux", "Windows", "Darwin"], f"Système d'exploitation détecté : {os_detected}"

def test_is_docker_installed(monkeypatch):
    # Simuler Docker installé
    class MockCompletedProcess:
        def __init__(self):
            self.returncode = 0

    def mock_run_success(*args, **kwargs):
        return MockCompletedProcess()

    monkeypatch.setattr(subprocess, "run", mock_run_success)
    assert is_docker_installed() == True

    # Simuler Docker non installé
    def mock_run_failure(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(subprocess, "run", mock_run_failure)
    assert is_docker_installed() == False

def test_create_container(monkeypatch):
    # Simuler une création de conteneur réussie
    class MockCompletedProcess:
        def __init__(self):
            self.returncode = 0

    def mock_run_success(*args, **kwargs):
        return MockCompletedProcess()

    monkeypatch.setattr(subprocess, "run", mock_run_success)
    assert create_container("hello-world") == True

    # Simuler une erreur lors de la création du conteneur
    def mock_run_failure(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "docker")

    monkeypatch.setattr(subprocess, "run", mock_run_failure)
    assert create_container("invalid-image") == False