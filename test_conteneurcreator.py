import subprocess
from colorama import Fore
from conteneurcreator import create_container, is_docker_installed, is_docker_active, container_count, install_ssh

# Test de la détection de Docker installé
def test_is_docker_installed(mocker):
    # Docker est installé (subprocess.run ne renvoie pas d'exception)
    mocker.patch('subprocess.run', return_value=True)
    assert is_docker_installed() is True

    # Docker n'est pas installé (subprocess.run lève une FileNotFoundError)
    mocker.patch('subprocess.run', side_effect=FileNotFoundError)
    assert is_docker_installed() is False


# Test de la vérification du service Docker actif
def test_is_docker_active(mocker):
    # Docker est actif (subprocess.run ne renvoie pas d'exception)
    mocker.patch('subprocess.run', return_value=True)
    assert is_docker_active() is True

    # Docker est inactif (subprocess.run lève une CalledProcessError)
    mocker.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'docker'))
    assert is_docker_active() is False


# Test de la création d'un conteneur Ubuntu sans volume
def test_create_container_ubuntu_no_volume(mocker):
    global container_count
    container_count = 0  # Réinitialiser le compteur

    # Mock de l'entrée utilisateur pour choisir Ubuntu sans volume
    mocker.patch('builtins.input', side_effect=["1", "n"])

    # Mock subprocess.run pour éviter l'exécution des commandes réelles
    mock_subprocess = mocker.patch('subprocess.run')

    # Mock display_message pour éviter l'affichage de messages
    mock_display_message = mocker.patch('conteneurcreator.display_message')

    # Appel de la fonction de création de conteneur
    create_container()

    # Vérification que les bons messages sont affichés
    mock_display_message.assert_any_call("Création du conteneur NOM-OS_A1 basé sur ubuntu...", Fore.YELLOW)

    # Vérification que la bonne commande docker est exécutée
    mock_subprocess.assert_called_with(
        "docker run -d --name NOM-OS_A1 --network bridge ubuntu sleep infinity",
        shell=True
    )

    # Vérification que le compteur de conteneurs est incrémenté
    assert container_count == 1


# Test de la création d'un conteneur Fedora avec un volume
def test_create_container_fedora_with_volume(mocker):
    global container_count
    container_count = 0  # Réinitialiser le compteur

    # Mock de l'entrée utilisateur pour choisir Fedora avec volume
    mocker.patch('builtins.input', side_effect=["2", "y", "/my/volume"])

    # Mock subprocess.run pour éviter l'exécution des commandes réelles
    mock_subprocess = mocker.patch('subprocess.run')

    # Mock display_message pour éviter l'affichage de messages
    mock_display_message = mocker.patch('conteneurcreator.display_message')

    # Appel de la fonction de création de conteneur
    create_container()

    # Vérification que les bons messages sont affichés
    mock_display_message.assert_any_call("Création du conteneur NOM-OS_A1 basé sur fedora...", Fore.YELLOW)

    # Vérification que la bonne commande docker est exécutée avec le volume
    mock_subprocess.assert_called_with(
        "docker run -d --name NOM-OS_A1 --network bridge -v /my/volume:/data fedora sleep infinity",
        shell=True
    )

    # Vérification que le compteur de conteneurs est incrémenté
    assert container_count == 1


# Test de la gestion d'un choix invalide
def test_create_container_invalid_choice(mocker):
    global container_count
    container_count = 0  # Réinitialiser le compteur

    # Mock de l'entrée utilisateur pour un choix invalide
    mocker.patch('builtins.input', side_effect=["4", "n"])

    # Mock subprocess.run pour éviter l'exécution des commandes réelles
    mock_subprocess = mocker.patch('subprocess.run')

    # Mock display_message pour éviter l'affichage de messages
    mock_display_message = mocker.patch('conteneurcreator.display_message')

    # Appel de la fonction de création de conteneur
    create_container()

    # Vérification que le message d'erreur est affiché
    mock_display_message.assert_any_call("Choix invalide.", Fore.RED)

    # Vérification qu'aucune commande docker n'a été exécutée
    mock_subprocess.assert_not_called()

    # Vérification que le compteur de conteneurs n'est pas incrémenté
    assert container_count == 0


# Test de l'installation de SSH dans un conteneur Ubuntu
def test_install_ssh_ubuntu(mocker):
    # Mock subprocess.run pour éviter l'exécution des commandes réelles
    mock_subprocess = mocker.patch('subprocess.run')

    # Mock display_message pour éviter l'affichage de messages
    mock_display_message = mocker.patch('conteneurcreator.display_message')

    # Appel de la fonction d'installation de SSH
    install_ssh("test_container", "ubuntu")

    # Vérification des commandes SSH spécifiques à Ubuntu
    mock_subprocess.assert_any_call(
        "docker exec -it test_container bash -c 'apt update && apt install -y openssh-server'", shell=True)
    mock_subprocess.assert_any_call("docker exec -it test_container bash -c 'service ssh start'", shell=True)

    # Vérification que les bons messages sont affichés
    mock_display_message.assert_any_call("SSH installé et configuré dans le conteneur test_container.", Fore.GREEN)


# Test de l'installation de SSH dans un conteneur Fedora
def test_install_ssh_fedora(mocker):
    # Mock subprocess.run pour éviter l'exécution des commandes réelles
    mock_subprocess = mocker.patch('subprocess.run')

    # Mock display_message pour éviter l'affichage de messages
    mock_display_message = mocker.patch('conteneurcreator.display_message')

    # Appel de la fonction d'installation de SSH
    install_ssh("test_container", "fedora")

    # Vérification des commandes SSH spécifiques à Fedora
    mock_subprocess.assert_any_call("docker exec -it test_container bash -c 'dnf install -y openssh-server'", shell=True)
    mock_subprocess.assert_any_call("docker exec -it test_container bash -c 'ssh-keygen -A'", shell=True)
    mock_subprocess.assert_any_call("docker exec -it test_container bash -c '/usr/sbin/sshd'", shell=True)

    # Vérification que les bons messages sont affichés
    mock_display_message.assert_any_call("SSH installé et configuré dans le conteneur test_container.", Fore.GREEN)
