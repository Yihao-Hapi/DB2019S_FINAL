import psycopg2
import database as db

#first prompt to print at the top of the main loop
def initialPrompt():
    print("\nMAIN: Please select one of the following query categories:\n"+\
            "\t1. Specific procedure lookup\n"+\
            "\t2. Hospital complications lookup\n"+\
            "\t3. Find average statistics for an area\n"+\
            "\t4. Find the safest hospital for given procedure\n"+\
            "\t5. Find a provider for a procedure under a budget\n"+\
            "\t6. Death rates by location\n"+\
            "\tEXIT. Exit the program\n")

#hospitalQuery not yet implemented
if __name__ == "__main__":
    while(1):
        functions = {"1": db.procedureQuery,"2": db.compQuery,"3":db.avgQuery,"4":db.Safest_Hospital,"5":db.Search_by_Budget,"6":db.deathrate_query}
        initialPrompt()
        command = db.safeInput()
        if (command == "EXIT" ):
            break
        elif (command not in ["1","2","3","4","5","6"]):
            print("ERROR: invalid input")
        else:
            functions[command]()
