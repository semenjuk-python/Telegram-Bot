#run this file to start the bot
import logging
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                    level=logging.INFO)
from app import bot, updater, dispatcher
from config import TOKEN, PORT

if __name__=='__main__':
    
	updater.start_webhook(listen='0.0.0.0',
						  port=PORT,
						  url_path=TOKEN)
	updater.bot.setWebhook('https://alabama-bot.herokuapp.com/'+TOKEN)
	updater.idle()
