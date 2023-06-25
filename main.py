from agent_hitman import Agent_Hitman
import time


def main():
    """
    Fonction principale du programme
    """

    hitman = Agent_Hitman()

    # On demande à l'utilisateur s'il souhaite utiliser SAT ou non
    print("Bienvenue dans le jeu Hitman !")
    print("Les deux phases du jeu vont s'exécuter :")
    print("Phase 1 : Découverte de la carte avec déduction")
    print("Phase 2 : Elimination de la cible")
    print("La phase 2 va s'exécuter automatiquement après la phase 1")
    print("Vous pouvez choisir d'utiliser SAT pour la phase 1 ou non")
    if input("Voulez-vous utiliser SAT ? (y/n) ") == "y":
        start = time.time()
        hitman.phase_1(True)
    else:
        start = time.time()
        hitman.phase_1()
    end = time.time()
    print("Durée de la phase 1 : " + str(end - start) + " secondes")

    print("------------------------------------------")
    print("Phase 2 : Elimination de la cible")
    hitman.phase_2()
    print("score phase 1 : ", hitman.score_phase1)

    print("Les deux phases du jeu sont terminées")
    print("Fin du jeu !")


if __name__ == "__main__":
    main()
