from agent_hitman import Agent_Hitman
import time


def main():
    """
    Fonction principale du programme
    """

    hitman = Agent_Hitman()

    # On lance la phase 1 et on regarde sa durée d'exécution
    start = time.time()
    hitman.phase_1()
    end = time.time()
    print("Durée de la phase 1 : " + str(end - start) + " secondes")



if __name__ == "__main__":
    main()
    