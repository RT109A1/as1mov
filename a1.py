import pickle

example_list = [9323054664, 50000, 'openchat/openchat-7b:free', True, [{"role": "user", "content": "This is a placeholder message. You can ignore it."}]]

users_list = [example_list]

with open("users.sf.gds", "wb") as file:
    pickle.dump(users_list, file)