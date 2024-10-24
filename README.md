# Игра «Угадай старинное слово»
___
Простая консольная игра, которая парсит
сайт https://slovar.kakras.ru и но основе
данных полученных оттуда создает словарь
со старинными словами.
___
**Описание игры:**
Игра выдает описание или значение старинного
слова, а игроку предлагается угадать это 
слово. Если игрок угадывает слово, ему 
добавляется 1 балл, иначе 1 добавляется к 
счету не угаданных слов. При очередном 
вопросе игрок может покинуть игру введя **0**.
После ввода **0** игра пишет ответ на 
последний вопрос (он не учитывается) и 
выводит количество угадланных и не 
угаданных слов.
___
**Возможности:** Поскольку данные игры
содержатся в файле: game_resource.json, можно
отредактировать его увеличив список слов,
описание имеющихся слов и т.д. Однако, если
вы снова распарсите сайт и сохраните данные,
все изменения будут утеряны.
___
**Окончательные положения:** Даже если файл game_resource.json не будет
найден игра автоматически распасит сайт и
создаст файл. Пользователю
при этом выдаются сообщения о всех действиях
программы. При завершении оперций выводится
предложение сыграть в игру