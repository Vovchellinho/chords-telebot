import telebot
from selenium import webdriver
from selenium.webdriver import Keys
import bs4
from settings import TG_TOKEN
# Создаем экземпляр бота
bot = telebot.TeleBot(TG_TOKEN)

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Пришлите мне, пожалуйста, название песни и исполнителя. Например: Цой Кукушка)')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        driver = webdriver.Chrome()
        flag = 1
        query = message.text
        bot.send_message(message.chat.id, 'Ожидайте, обрабатываем Ваш запрос: ' + message.text)
        driver.get("https://amdm.ru/")
        input_google = driver.find_element_by_xpath('//input[@name="q"]')
        input_google.send_keys(query)
        input_google.send_keys(Keys.RETURN)
        xpath = '/html/body/div[2]/article/table/tbody/tr[1]/td[3]/a[2]'
        driver.find_element_by_xpath(xpath).click()  # переходим на страницу с песней
        xpath = '/html/body/div[2]/article/div[1]/div[2]/div[4]/pre'
        song = driver.find_element_by_xpath(xpath)
        text_song = song.get_attribute('innerHTML')
        text_song = bs4.BeautifulSoup(text_song, 'html.parser').get_text()
        driver.quit()
    except:
        text_song = 'Не удалось выполнить ваш запрос. Проверьте правильность написания исполнителя и названия песни:('
    bot.send_message(message.chat.id, text_song)

# Запускаем бота
bot.polling(none_stop=True, interval=0)