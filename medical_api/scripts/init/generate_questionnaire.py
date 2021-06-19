from dataplane import neo4j

from scripts.utils import info, title


def format_q(q):
    return f""

# Слайдер с форматированием
# И ответы на вопросы с выбором без


def main() -> None:
    print(info('Generating questionnaire'))

    def generator(tx):
        tx_return = tx.run("""
        CREATE (RepeatedVisit:Result {})
        CREATE (Ambulance:Result {})
        CREATE (HouseCall:Result {})
        CREATE (TraumaCenter:Result {})

        CREATE (Therapist:Specialist {})
        CREATE (traumatologist orthopedist )
        CREATE (FirstTime:Question {})
        CREATE (
        
        
        """)
        return tx_return.single()

    result = neo4j.run_sync(generator)

    print("Successfully generated all questions")
    print(title("QUESTIONS"))
    for q in result:
        print(format_q(q))


if __name__ == '__main__':
    raise RuntimeError('Do not run scripts directly!')
