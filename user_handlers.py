from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.choo_diff_kb import MainMenu
from TASKS import *
from JSONfunctions import *
from THEORY import materials
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
    current_description: Optional[str] = State()
    current_var: Optional[int] = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловат!\n🎯 Выберите тему для тренировки:",
        reply_markup=MainMenu.to_choo_theme_kb()
    )

@router.callback_query(F.data.startswith('choo_theme_'))
async def handle_theme(callback: types.CallbackQuery, state: FSMContext): 
    theme = callback.data.split('_')[-1]
    await state.update_data(current_theme=theme)
    if theme != 'OGE':
        await callback.message.edit_text(
        f"📚 Выбрана тема: {theme}\n\n"
        "Уровни сложности:\n"
        "1️⃣ База - простые задания для разминки\n"
        "2️⃣ Средний - задачи с элементами анализа\n"
        "3️⃣ Продвинутый - комплексные задачи\n\n"
        "📝 Тест - 10 заданий с возрастающей сложностью\n"
        "🏆 Результаты теста попадают в таблицу лидеров!",
        reply_markup=MainMenu.to_choo_diff_kb()
    )
    else:
        await callback.message.edit_text(
        f"📚 Выберите задание ОГЭ:",
        reply_markup=MainMenu.to_choo_OGE_task_kb())

    await callback.answer()

@router.callback_query(F.data.startswith('task_'))
async def handle_theme(callback: types.CallbackQuery, state: FSMContext): 
    task = callback.data.split('_')[-1]
    await state.update_data(current_task=task)
    if task != 'OGE':
        await callback.message.edit_text(
        f"📋 Задание {task}\nВыберите тип задачи:",
        reply_markup=MainMenu.to_choo_OGE_kind_kb(task)
    )
    await callback.answer()

@router.callback_query(F.data.startswith('kind_'))
async def handle_theme(callback: types.CallbackQuery, state: FSMContext): 
    task = callback.data.split('_')[-1]
    await state.update_data(current_task=task)
    if task != 'OGE':
        await callback.message.edit_text(
        f"✅ Выбрано: {task}",
        reply_markup=MainMenu.to_begin_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('choo_diff_'))
async def handle_diff(callback: types.CallbackQuery, state: FSMContext): 
    difficulty = int(callback.data.split('_')[-1])
    await state.update_data(current_difficulty=difficulty)
    data = await state.get_data()
    await callback.message.edit_text(
        f"🎯 Настройки:\n\n"
        f"🏷 Тема: {data['current_theme']}\n"
        f"📈 Сложность: {difficulty}",
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
            formula, answer, description = generate_linear_equation(difficulty)
        case 'quadratic':
            formula, answer, description = generate_quadratic_equation(difficulty)
        case 'proportion':
            formula, answer, description = generate_proportion_equation(difficulty)
        case 'powers':
            formula, answer, description = generate_powers_equation(difficulty)
        case 'OGE':
            formula, answer, description = generate_OGE_equation(difficulty)
            
        case _:
            await callback.answer("⚠️ Неизвестная тема")
            return

    await state.update_data(
        current_time_start=start,
        current_answer=str(answer),
        current_formula=formula,
        current_user_answer="",
        is_testing=False,
        current_description=description
    )
    
    image = generate_formula_image(formula)
    await callback.message.answer_photo(
        photo=image,
        caption= description + "\n✏️ Введите ответ: ...",
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
    description = data['current_description'] if data.get('current_description') else ''
    pressed_button = callback.data.split('_')[-1]

    if pressed_button == 'del':
        current_user_answer = current_user_answer[:-1]
    elif pressed_button == 'clear':
        current_user_answer = ""
    else:
        current_user_answer += pressed_button

    await state.update_data(current_user_answer=current_user_answer)
    display_answer = current_user_answer.ljust(len(current_answer), '.')

    caption = f"📝 Уравнение:\n{formula}\n{description}\n✏️ Ответ: {display_answer}"
    if is_testing:
        test_task = data['current_test_task_index']
        caption = f"🔢 Вопрос {test_task+1}/10\n{caption}"

    if len(current_user_answer) == len(current_answer):
        end = time()
        timer = int(end - start_time)
        is_correct = current_user_answer == current_answer
        
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

        result_text = (f"✅ Верно! Время: {timer}с" if is_correct 
                       else f"❌ Ошибка! Время: {timer}с\n🔑 Правильный ответ: {current_answer}")
        
        await callback.message.edit_caption(
            caption=f"📝 Уравнение:\n{formula}\n{description}\n{result_text}",
            reply_markup=MainMenu.to_continue_test_kb() if is_testing else MainMenu.to_continue_kb()
        )
    else:
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

    for _ in range(3):
        test.append(generate_equation(theme, 1))
    for _ in range(4):
        test.append(generate_equation(theme, 2))
    for _ in range(3):
        test.append(generate_equation(theme, 3))

    await state.update_data(
        current_test=test,
        current_test_task_index=0,
        current_count=0,
        current_test_time=0,
        is_testing=True
    )
    
    await callback.message.edit_text(
        f"📚 Тест по теме '{theme}' готов!\n\n"
        "▪ 3 простых вопроса\n"
        "▪ 4 средних вопроса\n"
        "▪ 3 сложных вопроса\n\n",
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

        result_text = (
            f"🎉 Тест завершен!\n\n"
            f"✅ Правильных ответов: {data['current_count']}/10\n"
            f"⏱ Общее время: {data['current_test_time']}с\n"
            f"🏅 Начислено очков: {score}"
        )
        await callback.message.delete()
        await callback.message.answer(
            result_text,
            reply_markup=MainMenu.to_choo_theme_kb()
        )
        await state.clear()
        return

    formula, answer, description = test[test_task]
    await state.update_data(
        current_answer=str(answer),
        current_formula=formula,
        current_user_answer="",
        current_time_start=time()
    )
    
    image = generate_formula_image(formula)
    await callback.message.answer_photo(
        photo=image,
        caption=f"🔢 Вопрос {test_task+1}/10\n{description}\n✏️ Введите ответ: ...",
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
    await callback.message.delete()
    await callback.message.answer(
        "👋 Добро пожаловат!\n🎯 Выберите тему для тренировки:",
        reply_markup=MainMenu.to_choo_theme_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('OGEexit'))
async def handle_OGEexit(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "👋 Добро пожаловат!\n🎯 Выберите тему для тренировки:",
        reply_markup=MainMenu.to_choo_theme_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('top'))
async def show_leaderboard(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    theme = data.get('current_theme', 'general')
    leaderboard = await send_leaderboard(theme, state)
    
    await callback.message.edit_text(
        f"🏆 Топ игроков по теме '{theme}':\n\n{leaderboard}",
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
    
    leaderboard = ""
    for i, user in enumerate(sorted_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔸"
        leaderboard += f"{medal} {i}. {user['username']}: {user['score']} очков\n"
    
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

@router.callback_query(F.data.startswith('theory'))
async def show_leaderboard(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    theme = data.get('current_theme', 'general')
    
    await callback.message.delete()
    if data.get('current_test'):
        await callback.message.answer(
                f"📚 Теория по теме:\n\n{materials[theme]}",
                reply_markup=MainMenu.to_back_to_test_kb()
        )
        test_task = data['current_test_task_index']
    
        await state.update_data(current_test_task_index=test_task-1)
    else: 
        await callback.message.answer(
                f"📖 Теоретические материалы:\n\n{materials[theme]}",
                reply_markup=MainMenu.to_choo_diff_kb()
        )
    
    await callback.answer()


@router.callback_query(F.data.startswith('createvar_'))
async def create_variant(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    var = data.get('current_var', 0)
    
    var += 1
    
    task_number = callback.data.split('_')[-1]
    
    try:
        image = generate_oge_variant_image(task_number)
        
        await callback.message.answer_photo(
            photo=image,
            caption=f"📝 Вариант {var} для печати:",
            reply_markup=MainMenu.to_make_new_var_kb(task_number, var)
        )

        await state.update_data(current_var=var)

    except Exception as e:
        await callback.answer(f"Ошибка генерации: {str(e)}")