from dataplane import neo4j
from scripts.utils import info, title


def format_q(q):
    return f""


def main() -> None:
    print(info("Generating questionnaire"))

    def generator(tx):
        tx_return = tx.run(
            """
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

        CREATE (FirstTime:Question {title:"Первичное обращение?", type: "single", entry:true})
        CREATE (PainScale:Question {title:"Оцените уровень боли", min:1, max:10, type:"scale"})
        CREATE (SymptomsFirst:Question {title:"Укажите, есть ли у вас следующие симптомы", type:"multiple"})
        CREATE (SymptomsSecond:Question {title:"Укажите, есть ли у вас следующие симптомы", type:"multiple"})
        CREATE (Trauma:Question {title:"Причина обращения - недавняя травма?", type:"single"})
        
        CREATE (Body:Question {title:"Укажите, что вас беспокоит", type:"body"})
        CREATE (Stomach:Question {title:"Живот", type:"multiple"})
        
        CREATE
        (FirstTime)-[:ANSWER {text:"Нет"}]->(RepeatedVisit),
        (FirstTime)-[:ANSWER {text:"Да"}]->(PainScale),
        
        (PainScale)-[:ANSWER {min:1, max:3, description:"<b>Слабая боль</b>\\nПочти не мешает заниматься обычными делами"}]->(SymptomsFirst),
        (PainScale)-[:ANSWER {min:4, max:6, description:"<b>Умеренная боль</b>\\nМешает обычной жизни и не дает забыть о себе"}]->(SymptomsFirst),
        (PainScale)-[:ANSWER {min:7, max:10, description:"<b>Сильная боль</b>\\nЗатмевает всё, делает человека зависимым от помощи других"}]->(Ambulance),
        
        (SymptomsFirst)-[:ANSWER {text:"Боли в левой половине грудной клетки"}]->(Ambulance),
        (SymptomsFirst)-[:ANSWER {text:"Продолжающееся кровотечение"}]->(Ambulance),
        (SymptomsFirst)-[:ANSWER {text:"Нарушение дыхания"}]->(Ambulance),
        (SymptomsFirst)-[:ANSWER {text:"Резкое головокружение или неустойчивость, не можете идти, вынуждены лечь"}]->(Ambulance),
        (SymptomsFirst)-[:ANSWER {text:"Тошнота, рвота, повышение температуры, связанные с употреблением конкретных продуктов"}]->(Ambulance),
        (SymptomsFirst)-[:ANSWER {type:"empty"}]->(SymptomsSecond),
        
        (SymptomsSecond)-[:ANSWER {text:"Нарушение обоняния, повышение температуры"}]->(HouseCall),
        (SymptomsSecond)-[:ANSWER {text:"Жидкий стул больше пяти раз в день"}]->(HouseCall),
        (SymptomsSecond)-[:ANSWER {text:"Температура выше 38 вместе с насморком или кашлем"}]->(HouseCall),
        (SymptomsSecond)-[:ANSWER {text:"Пожелтение кожи, глазных белков и повышенная температура"}]->(HouseCall),
        (SymptomsSecond)-[:ANSWER {type:"empty"}]->(Trauma),
        
        (Trauma)-[:ANSWER {text:"Нет"}]->(Body),
        (Trauma)-[:ANSWER {text:"Да"}]->(TraumaCenter),
        
        (Body)-[:ANSWER {id: 3}]->(Stomach),
        
        (Stomach)-[:ANSWER {text:"Диарея"}]->(Infectologist),
        (Stomach)-[:ANSWER {text:"Отрыжка, изжога, горечь во рту"}]->(Gastroenterologist),
        (Stomach)-[:ANSWER {text:"Боли"}]->(Surgeon)
        
        RETURN SymptomsFirst
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
