import schedule
import random

def admin_key():
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    key = "admin-" + (str(random.randint(0, 9)))
    for i in range(10):
        key += random.choice(chars)
    with open('db/admin_key', 'r+') as f:
        f.truncate(0)
        f.write(key)
        f.close()
    print(34567890)


schedule.every(3).seconds.do(admin_key)

while True:
    schedule.run_pending()