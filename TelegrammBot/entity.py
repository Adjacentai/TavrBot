from telethon.tl.types import Channel, Chat, User

async def get_entities(client):
    dialogs = await client.get_dialogs()
    
    for dialog in dialogs:
        entity = dialog.entity
        
        if isinstance(entity, Channel):
            print(f"Канал: {entity.title}")
            print(f"ID канала: {entity.id}")
            print(f"Юзернейм канала: {entity.username}")
        elif isinstance(entity, Chat):
            print(f"Чат: {entity.title}")
            print(f"ID чата: {entity.id}")
        elif isinstance(entity, User):
            print(f"Пользователь: {entity.first_name} {entity.last_name}")
            print(f"ID пользователя: {entity.id}")
            print(f"Юзернейм пользователя: {entity.username}")
        
        print("---")