from dataplane import neo4j
from scripts.utils import info, title


def format_q(q):
    return f""


def main() -> None:
    print(info("Generating questionnaire"))

    def generator(tx):
        tx_return = tx.run("""
        CREATE (RepeatedVisit:Result {id:0})
        CREATE (Ambulance:Result {id:1})
        CREATE (HouseCall:Result {id:2})
        CREATE (TraumaCenter:Result {id:3})

        CREATE (Orthopedist:Specialty {id:0, name:"ортопед"})
        CREATE (Rheumatologist:Specialty {id:1, name:"ревматолог"})
        CREATE (Ophthalmologist:Specialty {id:2, name:"офтальмолог"})
        CREATE (Neurologist:Specialty {id:3, name:"невролог"})
        CREATE (Infectologist:Specialty {id:4, name:"инфекционист"})
        CREATE (Surgeon:Specialty {id:5, name:"хирург"})
        CREATE (Gastroenterologist:Specialty {id:6, name:"гастроэнтеролог"})
        CREATE (Otolaryngologist:Specialty {id:7, name:"отоларинголог"})
        CREATE (Coloproctologist:Specialty {id:8, name:"колопроктолог"})
        CREATE (Urologist:Specialty {id:9, name:"уролог"})
        CREATE (Oncologist:Specialty {id:10, name:"онколог"})

        CREATE (FirstTime:Question {}) 
        """)
        return tx_return.single()

    result = neo4j.run_sync(generator)

    print("Successfully generated all questions")
    print(title("QUESTIONS"))
    for q in result:
        print(format_q(q))


if __name__ == "__main__":
    raise RuntimeError("Do not run scripts directly!")
