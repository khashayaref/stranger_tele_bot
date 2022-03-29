from types import SimpleNamespace
from src.utils.keyboards import create_keyboard
    

keys = SimpleNamespace(
    random_connect=':bust_in_silhouette: Random Connect',
    settings=':gear: Setting',
    exit=':cross_mark: Exit'
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.random_connect, keys.settings),
    exit=create_keyboard(keys.exit)
)

states = SimpleNamespace(
    random_connection='RANDOM_CONNECT',
    main='MAIN',
    connected='CONNECTED'
)