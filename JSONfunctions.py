import json
from aiogram import types
from aiogram.fsm.context import FSMContext

def load_json_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}

def save_json_data(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        
data = load_json_data()


async def send_leaderboard(callback: types.CallbackQuery):
    data = load_json_data()

    # Сортируем пользователей по очкам (по убыванию)
    sorted_users = sorted(
        data["users"].items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )
    
    # Формируем текст сообщения
    leaderboard_text = "🏆 Рейтинг игроков:\n\n"
    for i, (user_id, user_data) in enumerate(sorted_users, 1):
        leaderboard_text += f"{i}. {user_data['username']}: {user_data['score']} очков\n"
    
    # Отправляем сообщение
    return leaderboard_text