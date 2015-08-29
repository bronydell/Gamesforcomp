import vk

#Объект Game с полями link(ссылка), users(кол.во юзеров проголосовало), score(коффициент пятачков ⊂(▀¯▀⊂))
class Game:
    def __init__(self, link, users, score):
        self.link = link;
        self.users = users;
        self.score = score;
    def __repr__(self):
        return repr((self.link, self.users, self.score))

#Массив игр
games = list()
#Отступ, что бы получать все записи
offset=1
#Константа количества записей
count = 100
#Среднее количество проголосовавших
users_per_game = 0
#Авторизируемся
vkapi = vk.API(access_token="токен_сюда")
#Делаем запрос на получение записей
while offset+count <= 1997:

    numoftry=0
    #Если выдает таймаут, то вызывает еще раз и так до тех пор, пока не уйдет ошибка таймаута
    while True:
        try:
            feedback = vkapi.wall.get(owner_id="-53524685", offset = str(offset), count=str(count), filter="owner", extended="0")
        except:
            numoftry+=1

            continue
        else:
            print("Запрос сделан за",numoftry,"попыток")
            break

    #Получаем из запроса лист игр
    for post in feedback["items"]:
    #Чекаем, пост это игра или нет(игра - это пост с опросом на 6 вариантов(5, 4, 3, 2, 1, Результат)
      if 'attachments' in post:
        for attach in post["attachments"]:
            if attach["type"] == 'poll':
               if len(attach["poll"]["answers"]) == 6:
                        #Считаем юзеров
                        users_per_game+=attach["poll"]["votes"]
                        #Делаем объект Game
                        game = Game('https://vk.com/wall-53524685_'+str(post['id']), attach["poll"]["votes"], attach["poll"]["answers"][0]["rate"])
                        #Добавляем в list
                        games.append(game)
    offset +=count
    print("Процесс: ", offset)
#Узнаеем среднее количество пользоватаелей на пост
users_per_game /= len(games)
print("Среднее количество проголосовавших на пост:", users_per_game, " Всего обработано игр:", len(games))
#Сортируем по пятеркам
games = sorted(games, key=lambda Game: Game.score, reverse=True)
i=0
for game in games:
    #Поздравляю, вы поразительны ;)
    if game.users > users_per_game:
        i+=1
        print(i,".",game.link, " с коэффициентом ", game.score, ". Всего проголосовало", game.users, "человек")







