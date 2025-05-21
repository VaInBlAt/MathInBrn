import json

def load_json_data(filename):
    try:
        with open('data\\'+filename+'.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}

def save_json_data(data, filename):
    with open('data\\'+filename+'.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        


async def send_leaderboard(filename):
    try:
        data = load_json_data(filename)
    except FileNotFoundError:
        return "Рейтинг пока пуст"
    
    sorted_users = sorted(
        data["users"].values(),
        key=lambda x: x["score"],
        reverse=True
    )[:10]
    
    leaderboard_text = ""
    for i, user in enumerate(sorted_users, 1):
        leaderboard_text += f"{i}. {user['username']}: {user['score']} очков\n"
    
    return leaderboard_text