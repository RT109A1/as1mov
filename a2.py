import pickle
def getUserFile():
  file = open('users.sf.gds', 'rb')
  all_users_list = pickle.load(file)
  return all_users_list
print(getUserFile())