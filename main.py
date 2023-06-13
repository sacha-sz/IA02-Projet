from agent_hitman import Agent_Hitman
import time


def main():
    """
    Fonction principale du programme
    """

    hitman = Agent_Hitman()

    # On demande à l'utilisateur s'il souhaite utiliser SAT ou non
    if input("Voulez-vous utiliser SAT ? (y/n) ") == "y":
        start = time.time()
        hitman.phase_1(True)
    else:
        start = time.time()
        hitman.phase_1()
    end = time.time()
    print("Durée de la phase 1 : " + str(end - start) + " secondes")
    #hitman.phase_2()



if __name__ == "__main__":
    main()
    