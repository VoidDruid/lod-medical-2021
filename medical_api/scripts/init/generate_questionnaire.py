from dataplane import neo4j
from scripts.utils import info, title


def format_q(q):
    return f""


# Слайдер с форматированием
# И ответы на вопросы с выбором без


def main() -> None:
    print(info("Generating questionnaire"))

    def generator(tx):
        tx_return = tx.run(
            """
        CREATE (RepeatedVisit:Result {})
        CREATE (Ambulance:Result {})
        CREATE (HouseCall:Result {})
        CREATE (TraumaCenter:Result {})

        CREATE (Orthopedist:Specialist {id:0, name:"ортопед"})
        CREATE (Rheumatologist:Specialist {id:1, name:"ревматолог"})
        CREATE (Ophthalmologist:Specialist {id:2, name:"офтальмолог"})
        CREATE (Neurologist:Specialist {id:3, name:"невролог"})
        CREATE (Infectologist:Specialist {id:4, name:"инфекционист"})
        CREATE (Surgeon:Specialist {id:5, name:"хирург"})
        CREATE (Gastroenterologist:Specialist {id:6, name:"гастроэнтеролог"})
        CREATE (Otolaryngologist:Specialist {id:7, name:"отоларинголог"})
        CREATE (Coloproctologist:Specialist {id:8, name:"колопроктолог"})
        CREATE (Urologist:Specialist {id:9, name:"уролог"})
        CREATE (Oncologist:Specialist {id:10, name:"онколог"})

        CREATE (FirstTime:Question {}) 
        """
        )
        return tx_return.single()

    result = neo4j.run_sync(generator)

    print("Successfully generated all questions")
    print(title("QUESTIONS"))
    for q in result:
        print(format_q(q))


if __name__ == "__main__":
    raise RuntimeError("Do not run scripts directly!")
