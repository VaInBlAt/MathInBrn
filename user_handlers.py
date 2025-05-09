#МОЯ ВЕРСИЯ

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.choo_diff_kb import MainMenu
from TASKS import *
from JSONfunctions import *
from typing import Optional
from random import shuffle
from latexTEST import *
from time import time

router = Router()

class States(StatesGroup):
    current_difficulty: Optional[int] = State()
    current_theme: Optional[str] = State()
    current_answer: Optional[int] = State()
    current_user_answer: Optional[int] = State()
    current_time_start: Optional[float] = State()
    current_test_time: Optional[int] = State()
    current_test: Optional[list] = State()
    current_test_task: Optional[int] = State()
    current_count: Optional[int] = State()
    

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выберите тему:",
        reply_markup=MainMenu.to_choo_theme_kb()
    )
    

@router.callback_query(F.data.startswith('choo_theme_'))
async def handle_theme(callback: types.CallbackQuery, state: FSMContext): 
    theme = callback.data.split('_')[-1]
    await state.update_data(current_theme=theme)
    await callback.message.edit_text(
        f"Выбрана тема {theme}\nВыберите сложность:\nимя {callback.from_user.first_name} id {callback.from_user.id}" ,
        reply_markup=MainMenu.to_choo_diff_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('choo_diff_'))
async def handle_diff(callback: types.CallbackQuery, state: FSMContext): 
    difficulty = int(callback.data.split('_')[-1])
    await state.update_data(current_difficulty=difficulty)
    data = await state.get_data()
    await callback.message.edit_text(
        f"Выбрана сложность {difficulty} и тема {data['current_theme']}",
        reply_markup=MainMenu.to_begin_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('begin'))
async def begin(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    difficulty = data['current_difficulty']
    theme = data['current_theme']
    start = time()
    await state.update_data(current_time_start=start)   

    match theme:
        case 'line':
            formula, answer = generate_linear_equation(int(difficulty))
        case 'quadratic':
            formula, answer = generate_quadratic_equation(int(difficulty))
        case 'proportion':
            formula, answer = generate_proportion_equation(int(difficulty))
        
    await state.update_data(current_answer=answer)   
    image = await generate_formula_image(formula)
    
    if isinstance(answer, tuple):
        # Для квадратных уравнений берем один из корней (меньший)
        correct_root = min(answer)
        answers = [
            str(int(correct_root/2)),
            str(int(correct_root+2)),
            str(correct_root),
            str(int(correct_root*2))
        ]
    else:
        # Для линейных уравнений
        answers = [
            str(int(answer/2)),
            str(int(answer+2)),
            str(answer),
            str(int(answer*2))
        ]
    
    shuffle(answers)
            
    caption = f"Решите уравнение:\n{formula}\nЕсли корней несколько, выпишите меньший из них"
    await callback.message.answer_photo(
        photo=image,
        caption=caption,
        reply_markup=MainMenu.answers_kb(*answers)
    )
    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data.startswith('user_answer_'))
async def handle_answer(callback: types.CallbackQuery, state: FSMContext): 
    user_answer = int(callback.data.split('_')[-1])
    data = await state.get_data()
    end = time()
    timer = int(end - data.get('current_time_start'))
    correct_answer = data.get('current_answer')

    if type(correct_answer) == tuple:
        text = f"❌ Неверно за {timer}с! Правильный ответ: {min(correct_answer)}"
        if int(user_answer) == int(min(correct_answer)):
            text = f"✅ Верно! За {timer}с"
            if data.get('current_test'):
                count = data.get('current_count')
                count += 1
                await state.update_data(current_count=count)
        if data.get('current_test'):
            test_time = data.get('current_test_time')
            test_time += timer
            await state.update_data(current_test_time=test_time)
    elif type(correct_answer) == int:
        text = f"❌ Неверно за {timer}с! Правильный ответ: {correct_answer}"
        if int(user_answer) == int(correct_answer):
            text = f"✅ Верно! За {timer}с"
            if data.get('current_test'):
                count = data.get('current_count')
                count += 1
                await state.update_data(current_count=count)
        if data.get('current_test'):
            test_time = data.get('current_test_time')
            test_time += timer
            await state.update_data(current_test_time=test_time)
        
    if data.get('current_test'):     
        await callback.message.answer(text, reply_markup=MainMenu.to_continue_test_kb())
    else:
        await callback.message.answer(text, reply_markup=MainMenu.to_continue_kb())
    await callback.answer()

@router.callback_query(F.data.startswith('exit'))
async def handle_exit(callback: types.CallbackQuery): 
    await callback.message.edit_text(
        "Добро пожаловать! Выберите тему:",
        reply_markup=MainMenu.to_choo_theme_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('generate_test'))
async def handle_test(callback: types.CallbackQuery, state: FSMContext): 
    data = await state.get_data()
    theme = data['current_theme']

    await state.update_data(current_count=0, current_test_time=0)
    
    test = []
    if theme == 'line':
        test = [
            generate_linear_equation(1),
            generate_linear_equation(1),
            generate_linear_equation(1),
            generate_linear_equation(2),
            generate_linear_equation(2),
            generate_linear_equation(2),
            generate_linear_equation(3),
            generate_linear_equation(3),
            generate_linear_equation(3),
            generate_linear_equation(3)
        ]
    elif theme == 'quadratic':
        # Равномерно распределяем сложности для квадратных уравнений
        test = [
            generate_quadratic_equation(1),
            generate_quadratic_equation(1),
            generate_quadratic_equation(1),
            generate_quadratic_equation(2),
            generate_quadratic_equation(2),
            generate_quadratic_equation(2),
            generate_quadratic_equation(3),
            generate_quadratic_equation(3),
            generate_quadratic_equation(3),
            generate_quadratic_equation(3)
        ]
    
    elif theme == 'proportion':
        # Равномерно распределяем сложности для квадратных уравнений
        test = [
            generate_proportion_equation(1),
            generate_proportion_equation(1),
            generate_proportion_equation(1),
            generate_proportion_equation(2),
            generate_proportion_equation(2),
            generate_proportion_equation(2),
            generate_proportion_equation(3),
            generate_proportion_equation(3),
            generate_proportion_equation(3),
            generate_proportion_equation(3)
        ]
    
    

    await state.update_data(current_test=test, current_test_task=0)

    await callback.message.edit_text(
        f"Выбран тест на тему {theme}",
        reply_markup=MainMenu.to_begin_test_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('test_'))
async def begin_test(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    test = data.get('current_test', [])
    
    if not test:
        await callback.message.answer("Тест не найден!")
        return
    
    test_task = data.get('current_test_task', 0)
    start = time()
    await state.update_data(current_time_start=start)

    try:
        if test_task >= len(test):
            # Тест завершен - подсчет результатов
            correct_answers = data.get('current_count', 0)
            total_time = data.get('current_test_time', 0)
            
            # Загружаем данные пользователей
            users_data = load_json_data()
            user_id = str(callback.from_user.id)
            
            # Если пользователя нет в базе - создаем
            if user_id not in users_data["users"]:
                users_data["users"][user_id] = {
                    "username": callback.from_user.first_name,
                    "score": 0
                }
            
            # Вычисляем очки за тест (20 за правильный, -60 за неправильный)
            test_score = (correct_answers * 20) - ((10 - correct_answers) * 60)
            users_data["users"][user_id]["score"] += test_score
            
            # Сохраняем обновленные данные
            save_json_data(users_data)
            
            await state.update_data(current_test=[], current_test_task=0)
            await callback.message.answer(
                "Тест завершен! 🎉\n" \
                f"Результат: {correct_answers}/10 за {total_time} секунд.\n" \
                f"Начислено очков: {test_score}\n" \
                f"Текущий счет: {users_data['users'][user_id]['score']}\n\n" \
                f"{await send_leaderboard(callback)}",
                reply_markup=MainMenu.to_choo_theme_kb()
            )
            return
            
        formula, answer = test[test_task]
        await state.update_data(current_answer=answer)
        
        image = await generate_formula_image(formula)
        
        if isinstance(answer, tuple):
            correct_root1, correct_root2 = answer
            answers = [
                str(correct_root1),
                str(correct_root2),
                str(correct_root1 + random.randint(1, 3)),
                str(correct_root2 - random.randint(1, 3))
            ]
        else:
            answers = [
                str(int(answer / 2)),
                str(int(answer + 2)),
                str(answer),
                str(int(answer * 2))
            ]
        shuffle(answers)
        
        caption = f"Решите уравнение {test_task+1}/10:\n{formula}\nЕсли корней несколько, выпишите меньший из них"
        await callback.message.answer_photo(
            photo=image,
            caption=caption,
            reply_markup=MainMenu.answers_kb(*answers)
        )
        
        await state.update_data(current_test_task=test_task + 1)
        
    except Exception as e:
        await callback.message.answer(
            f"Произошла ошибка: {str(e)}",
            reply_markup=MainMenu.to_choo_diff_kb()
        )
    
    await callback.answer()


@router.callback_query(F.data.startswith('user_answer_'))
async def handle_answer(callback: types.CallbackQuery, state: FSMContext): 
    user_answer = int(callback.data.split('_')[-1])
    data = await state.get_data()
    end = time()
    timer = int(end - data.get('current_time_start'))
    correct_answer = data.get('current_answer')

    # Загружаем данные пользователей
    users_data = load_json_data()
    user_id = str(callback.from_user.id)
    
    # Если пользователя нет в базе - создаем
    if user_id not in users_data["users"]:
        users_data["users"][user_id] = {
            "username": callback.from_user.first_name,
            "score": 0
        }

    if type(correct_answer) == tuple:
        text = f"❌ Неверно за {timer}с! Правильный ответ: {min(correct_answer)}"
        if int(user_answer) == int(min(correct_answer)):
            text = f"✅ Верно! За {timer}с"
            if data.get('current_test'):
                count = data.get('current_count', 0)
                count += 1
                await state.update_data(current_count=count)
                
                # Начисляем 20 очков за правильный ответ в тесте
                users_data["users"][user_id]["score"] += 20
        else:
            if data.get('current_test'):
                # Вычитаем 60 очков за неправильный ответ в тесте
                users_data["users"][user_id]["score"] -= 60
                
        if data.get('current_test'):
            test_time = data.get('current_test_time', 0)
            test_time += timer
            await state.update_data(current_test_time=test_time)
            
    elif type(correct_answer) == int:
        text = f"❌ Неверно за {timer}с! Правильный ответ: {correct_answer}"
        if int(user_answer) == int(correct_answer):
            text = f"✅ Верно! За {timer}с"
            if data.get('current_test'):
                count = data.get('current_count', 0)
                count += 1
                await state.update_data(current_count=count)
                
                # Начисляем 20 очков за правильный ответ в тесте
                users_data["users"][user_id]["score"] += 20
        else:
            if data.get('current_test'):
                # Вычитаем 60 очков за неправильный ответ в тесте
                users_data["users"][user_id]["score"] -= 60
                
        if data.get('current_test'):
            test_time = data.get('current_test_time', 0)
            test_time += timer
            await state.update_data(current_test_time=test_time)
    
    # Сохраняем обновленные данные
    save_json_data(users_data)
        
    if data.get('current_test'):     
        await callback.message.answer(text, reply_markup=MainMenu.to_continue_test_kb())
    else:
        await callback.message.answer(text, reply_markup=MainMenu.to_continue_kb())
    await callback.answer()

    
@router.callback_query(F.data.startswith('top'))
async def handle_theme(callback: types.CallbackQuery, state: FSMContext): 
    await callback.message.edit_text(
        f"{await send_leaderboard(callback)}",
        reply_markup=MainMenu.to_exit_kb()
    )
    await callback.answer()