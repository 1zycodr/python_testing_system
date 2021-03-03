import json
import random

def get_json():
    """
    Получает данные из data.json
    :return: - dict, list 
    """
    data = None
    with open('data.json') as f:
        data = json.load(f)
    return data

def write_json(data):  
    """
    Записывает данные в data.json
    :param data: - list, dict
    """
    with open("data.json", 'w') as file:
        json.dump(data, file, sort_keys=True, indent=4)


def test():
    """
    Меню тестирования
    """
    data = get_json()
    questions = data['questions']
    score = 0
    total = len(questions)
    st = []
    
    while True:
        if len(st) == total:
            print(f'Вы набрали {score} из {total}!')
            input()
            break
        question = random.choice(questions)
        while question in st:
            question = random.choice(questions)
        st.append(question)
        user_answer = input(f"Вопрос: \n\t{question['text']}\nВаш ответ: ")
        if user_answer == question['answer']:
            score += 1
            question['cor_answers'] += 1
        else:
            question['wrong_answers'] += 1
    
    write_json(data)

def edit():
    """
    Меню редактирования вопросов
    """
    while True:
        data = get_json()
        questions = data['questions']

        for ind, question in enumerate(questions):
            print(f"[id: {ind}] - text: {question['text']}\n\t\tanswer: {question['answer']}\n\t\tcorrect answers: {question['cor_answers']}\n\t\twrong answers: {question['wrong_answers']}")

        print('[1] - Создать вопрос\n[2] - Изменить вопрос\n[3] - Удалить вопрос\n[4] - Обнулить статистику\n[5] - Выход')
        user_input = input('Выберите действие: ')
        while user_input not in ['1', '2', '3', '4', '5']:
            user_input = input('Ошибка! Выберите действие (1 - 5): ')
        
        if user_input == '1':
            new_question_text = input('Введите текст вопроса (# - отменить): ')
            if new_question_text == '#':
                continue
            new_question_answer = input('Введите ответ на вопрос (# - отменить): ')
            if new_question_answer == '#':
                continue
            
            confirm = input(f"Текст: {new_question_text}\nОтвет: {new_question_answer}\nСоздать вопрос? \n[1] - Да \n[2] - Отмена\n:")
            
            while confirm not in ['1', '2']:
                confirm = input('Создать вопрос? \n[1] - Да \n[2] - Отмена\n:')
            
            if confirm == '2':
                input('Создание отменено!')
                continue
            
            questions.append({
                'text' : new_question_text,
                'answer' : new_question_answer,
                'cor_answers' : 0,
                'wrong_answers' : 0
            })
            write_json(data)
            input('Вопрос был добавлен!')
        elif user_input == '2':
            q_id = input('Введите id вопроса, который хотите изменить: ')
            while (not q_id.isdigit()) or (not (0 <= int(q_id) < len(questions))):
                q_id = input('Ошибка! Введите id вопроса, который хотите изменить: ')
            
            current_question = questions[int(q_id)]

            f = False

            new_question_text = input('Введите новый текст вопроса (# - не менять): ')
            if new_question_text != '#':
                current_question['text'] = new_question_text
                write_json(data)
                f = True
            new_question_answer = input('Введите новый ответ на вопрос (# - не менять): ')
            if new_question_answer != '#':
                current_question['answer'] = new_question_answer
                write_json(data)
                f = True
            input('Вопрос изменён!' if f else 'Изменений не произошло.')
        elif user_input == '3':
            q_id = input('Введите id вопроса, который хотите удалить: ')
            while (not q_id.isdigit()) or (not (0 <= int(q_id) < len(questions))):
                q_id = input('Ошибка! Введите id вопроса, который хотите удалить: ')
            
            confirm = input('Вы уверены, что хотите удалить этот вопрос? (y - Да, n - Нет): ')
            while confirm not in ['y', 'n']:
                confirm = input('Ошибка! Вы уверены, что хотите удалить этот вопрос? (y - Да, n - Нет): ')
            
            if confirm == 'y':
                del questions[int(q_id)]
                write_json(data)
                input('Вопрос был удалён!')
            else:
                input('Удаление вопроса отменено!')
        elif user_input == '4':
            user_input = input('[1] - Обнулить статистику всех вопросов\n[2] - Обнулить статистику одного вопроса\n[3] - Назад\nВыберите действие: ')
            while user_input not in ['1', '2', '3']:
                user_input = input('Ошибка! Выберите действие (1 - 3): ')
            
            if user_input == '1':
                confirm = input('Вы уверены, что хотите обнулить статистику всех вопросов? (y - Да, n - Нет): ')
                while confirm not in ['y', 'n']:
                    confirm = input('Ошибка! Вы уверены, что хотите обнулить статистику всех вопросов? (y - Да, n - Нет): ')
                
                if confirm == 'y':
                    for question in questions:
                        question['cor_answers'] = 0
                        question['wrong_answers'] = 0
                    write_json(data)
                    input('Статистика вопросов обнулена!')
                else:
                    input('Действие отменено.')
            elif user_input == '2':
                q_id = input('Введите id вопроса, статистику которого хотите обнулить: ')
                while (not q_id.isdigit()) or (not (0 <= int(q_id) < len(questions))):
                    q_id = input('Ошибка! Введите id вопроса, статистику которого хотите обнулить: ')       
                
                confirm = input('Вы уверены, что хотите обнулить статистику этого вопроса? (y - Да, n - Нет): ')
                while confirm not in ['y', 'n']:
                    confirm = input('Ошибка! Вы уверены, что хотите обнулить статистику этого вопроса? (y - Да, n - Нет): ')
                
                if confirm == 'y':
                    question = questions[int(q_id)]
                    question['cor_answers'] = 0
                    question['wrong_answers'] = 0
                    write_json(data)
                    input('Статистика вопроса обнулена!')
                else:
                    input('Действие отменено.')
        else:
            return

def main():
    while True:
        user_input = input('[1] - Пройти тест\n[2] - Редактировать вопросы\n[3] - Выйти\nВыберите действие: ')
        while user_input not in ['1', '2', '3']:
            user_input = input('Ошибка! Выберите действие (1 - 3): ')
        if user_input == '1':
            test()
        elif user_input == '2':
            edit()
        else:
            print('Пока!')
            exit(0)

if __name__ == '__main__':
    main()