from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.choo_diff_kb import MainMenu
from TASKS import *
from JSONfunctions import *
from typing import Optional
from latexTEST import *
from time import time

router = Router()

class States(StatesGroup):
    current_difficulty: Optional[int] = State()
    current_theme: Optional[str] = State()
    current_answer: Optional[str] = State()
    current_formula: Optional[str] = State()
    current_user_answer: Optional[str] = State()
    current_time_start: Optional[float] = State()
    current_test: Optional[list] = State()
    current_test_task_index: Optional[int] = State()
    current_count: Optional[int] = State()
    current_test_time: Optional[int] = State()
    is_testing: Optional[bool] = State()
    current_table: Optional[str] = State()
    current_task: Optional[str] = State()

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
    if theme != 'OGE':
        await callback.message.edit_text(
        f"Выбрана тема {theme}\nВыберите сложность:",
        reply_markup=MainMenu.to_choo_diff_kb()
    )
    else:
        await callback.message.edit_text(
        f"Выберите задание",
        reply_markup=MainMenu.to_choo_OGE_task_kb())

    await callback.answer()

@router.callback_query(F.data.startswith('task_'))
async def handle_theme(callback: types.CallbackQuery, state: FSMContext): 
    task = callback.data.split('_')[-1]
    await state.update_data(current_task=task)
    if task != 'OGE':
        await callback.message.edit_text(
        f"Выбрано задание {task}\nВыберите вид:",
        reply_markup=MainMenu.to_choo_OGE_kind_kb(task)
    )
    await callback.answer()

@router.callback_query(F.data.startswith('kind_'))
async def handle_theme(callback: types.CallbackQuery, state: FSMContext): 
    task = callback.data.split('_')[-1]
    await state.update_data(current_task=task)
    if task != 'OGE':
        await callback.message.edit_text(
        f"Выбрано задание {task}",
        reply_markup=MainMenu.to_begin_kb()
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
    theme = data['current_theme']
    if not data.get('current_task'):
        difficulty = data['current_difficulty']
    else:
        difficulty = data.get('current_task')
    start = time()

    match theme:
        case 'line':
            formula, answer = generate_linear_equation(difficulty)
        case 'quadratic':
            formula, answer = generate_quadratic_equation(difficulty)
        case 'proportion':
            formula, answer = generate_proportion_equation(difficulty)
        case 'powers':
            formula, answer = generate_powers_equation(difficulty)
        case 'OGE':
            formula, answer = generate_OGE_equation(difficulty)
            
        
        case _:
            await callback.answer("Неизвестная тема")
            return

    await state.update_data(
        current_time_start=start,
        current_answer=str(answer),
        current_formula=formula,
        current_user_answer="",
        is_testing=False
    )
    
    image = await generate_formula_image(formula)
    await callback.message.answer_photo(
        photo=image,
        caption="ОТВЕТ: ...",
        reply_markup=MainMenu.num_board_kb()
    )
    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data.startswith('num_'))
async def handle_number_input(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_answer = data['current_answer']
    current_user_answer = data['current_user_answer']
    formula = data['current_formula']
    start_time = data['current_time_start']
    is_testing = data['is_testing']
    pressed_button = callback.data.split('_')[-1]

    # Обработка специальных кнопок
    if pressed_button == 'del':
        current_user_answer = current_user_answer[:-1]
    elif pressed_button == 'clear':
        current_user_answer = ""
    else:
        current_user_answer += pressed_button

    await state.update_data(current_user_answer=current_user_answer)
    display_answer = current_user_answer.ljust(len(current_answer), '.')

    # Формируем заголовок
    caption = f"{formula}\n\nОТВЕТ: {display_answer}"
    if is_testing:
        test_task = data['current_test_task_index']
        caption = f"Вопрос {test_task+1}/10\n{caption}"

    # Проверка завершения ввода
    if len(current_user_answer) == len(current_answer):
        end = time()
        timer = int(end - start_time)
        is_correct = current_user_answer == current_answer
        
        # Обновление статистики теста
        if is_testing:
            count = data['current_count']
            test_time = data['current_test_time']
            if is_correct:
                count += 1
                test_time += timer
            else:
                test_time += timer
            await state.update_data(
                current_count=count,
                current_test_time=test_time
            )

        # Формирование результата
        result_text = (f"✅ Верно За {timer}с" if is_correct 
                       else f"❌ Неверно! За {timer}с\nПравильный ответ: {current_answer}")
        
        # Обновление сообщения
        await callback.message.edit_caption(
            caption=f"{formula}\n\n{result_text}",
            reply_markup=MainMenu.to_continue_test_kb() if is_testing else MainMenu.to_continue_kb()
        )
    else:
        # Обновление текущего ввода
        await callback.message.edit_caption(
            caption=caption,
            reply_markup=MainMenu.num_board_kb()
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith('generate_test'))
async def handle_test(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    theme = data['current_theme']
    test = []

    # Генерация тестовых вопросов
    for _ in range(3):  # 3 легких вопроса
        test.append(generate_equation(theme, 1))
    for _ in range(4):  # 4 средних вопроса
        test.append(generate_equation(theme, 2))
    for _ in range(3):  # 3 сложных вопроса
        test.append(generate_equation(theme, 3))

    await state.update_data(
        current_test=test,
        current_test_task_index=0,
        current_count=0,
        current_test_time=0,
        is_testing=True
    )
    
    await callback.message.edit_text(
        f"Тест по теме {theme} готов!",
        reply_markup=MainMenu.to_begin_test_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('test_'))
async def begin_test(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    test = data['current_test']
    test_task = data['current_test_task_index']
    theme = data['current_theme']

    if test_task >= len(test):
        # Завершение теста
        users_data = load_json_data(theme)
        user_id = str(callback.from_user.id)
        score = (data['current_count'] * 20) - ((10 - data['current_count']) * 40)
        
        if user_id not in users_data["users"]:
            users_data["users"][user_id] = {
                "username": callback.from_user.first_name,
                "score": 0
            }
        
        users_data["users"][user_id]["score"] += score
        save_json_data(users_data, theme)

        # Формирование результатов
        result_text = (
            f"Тест завершен!\n"
            f"Правильных ответов: {data['current_count']}/10\n"
            f"Общее время: {data['current_test_time']}с\n"
            f"Начислено очков: {score}"
        )
        
        await callback.message.answer(
            result_text,
            reply_markup=MainMenu.to_choo_theme_kb()
        )
        await state.clear()
        return

    # Загрузка текущего вопроса
    formula, answer = test[test_task]
    await state.update_data(
        current_answer=str(answer),
        current_formula=formula,
        current_user_answer="",
        current_time_start=time()
    )
    
    image = await generate_formula_image(formula)
    await callback.message.answer_photo(
        photo=image,
        caption=f"Вопрос {test_task+1}/10\nОТВЕТ: ...",
        reply_markup=MainMenu.num_board_kb()
    )
    await state.update_data(current_test_task_index=test_task + 1)
    await callback.answer()

@router.callback_query(F.data.startswith('continue'))
async def continue_mode(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('is_testing'):
        await begin_test(callback, state)
    else:
        await begin(callback, state)
    await callback.answer()

@router.callback_query(F.data.startswith('exit'))
async def handle_exit(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()  # Удаляем старое сообщение
    await callback.message.answer(  # Отправляем новое сообщение
        "Главное меню:",
        reply_markup=MainMenu.to_choo_theme_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('top'))
async def show_leaderboard(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    theme = data.get('current_theme', 'general')
    leaderboard = await send_leaderboard(theme, state)
    
    await callback.message.edit_text(
        f"🏆 Рейтинг по теме '{theme}':\n\n{leaderboard}",
        reply_markup=MainMenu.to_exit_kb()
    )
    await callback.answer()

async def send_leaderboard(callback: types.CallbackQuery, state: FSMContext) -> str:
    data = await state.get_data()
    users_data = load_json_data(data.get('current_theme'))
    sorted_users = sorted(
        users_data["users"].values(),
        key=lambda x: x["score"],
        reverse=True
    )[:10]
    
    leaderboard = "🏆 Топ игроков:\n"
    for i, user in enumerate(sorted_users, 1):
        leaderboard += f"{i}. {user['username']}: {user['score']} очков\n"
    
    return leaderboard

def generate_equation(theme: str, difficulty: int) -> tuple:
    match theme:
        case 'line': 
            return generate_linear_equation(difficulty)
        case 'quadratic':
            return generate_quadratic_equation(difficulty)
        case 'proportion':
            return generate_proportion_equation(difficulty)
        case 'powers':
            return generate_powers_equation(difficulty)
        case 'OGE':
            return generate_OGE_equation(difficulty)
        
        
    raise ValueError("Неизвестная тема")
