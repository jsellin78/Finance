import subprocess
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import html
from decimal import Decimal 
import shlex

# Parse telegram input and do some action based on the input. 

# Define the function to handle the 'n' command
def launch_script_n(update, context):
    # Get the arguments passed by the user
    message_text = update.message.text.lower()
    args = message_text.split()[1:]  # Remove the first element 'n' from the message text

    if len(args) != 3:
        # Send an error message to the user indicating the incorrect argument format
        update.message.reply_text("Incorrect argument format for 'n' command. Please provide 3 arguments. n Day hour currency ")

    command = ['tmux', 'send-keys', '-t', 'ifvalues', '/root/newstart/newtest1.sh'] + [' '] + list(' '.join(args)) + [' '] + ['&'] + ['Enter']
 # Execute the another script with arguments using subprocess
    subprocess.run(command)

def Price_alert(update, context, number, currency, sentiment, args, description):
    # Get the arguments passed by the user
    message_text = update.message.text.lower()
    args = message_text.split()[1:]  # Remove the first element 'n' from the message text

    command = ['tmux', 'send-keys', '-t', 'ifvalues', 'python3 ', '/root/price/pricealert.py'] + \
            [' '] + ['--currency='] + [currency] + \
            [' '] + ['--target='] + [str(number)] + \
            [' '] + ['--timeout='] + ['200000'] + \
            [' '] + ['--type='] + [sentiment] + \ 
            [' '] + ['--interval='] + ['2'] + \
            [' '] + ['--workers='] + ['2'] + \
            [' '] + ['--patterndate='] + ['2023-01-24'] + \
            [' '] + ['--description='] + [shlex.quote(str(description))] + \
            [' '] + ['&', 'Enter'] 


    subprocess.run(command)

def launch_script_p(update, context):
    # Execute your script for command 'p' using subprocess and capture the output
    output = subprocess.check_output(['bash', '/files/price5.sh']).decode('utf-8')

    # Escape special characters in the output text
    escaped_output = html.escape(output)

    # Format the output using HTML
    formatted_output = f"<pre>{escaped_output}</pre>"
    # Send the formatted output as a response message
    update.message.reply_html(formatted_output)

    
def help_p(update, context):
    update.message.reply_text("For 4 hour you need to provide n DAY HOUR currency \ for 15 min you need to provide y DAY HOUR MINUTE CURRENCY")

def launch_script_y(update, context):
    # Get the arguments 
    message_text = update.message.text.lower()
    args = message_text.split()[1:]  # Remove the first element 'y' from the message text

    if len(args) != 4:
        update.message.reply_text("Incorrect argument format for 'y' command. Please provide 4 arguments. y DAY HOUR MINUTE CURRENCY")
        return

    command = ['tmux', 'send-keys', '-t', 'ifvalues', '/root/newstart/15min/15min2.sh'] + [' '] + list(' '.join(args)) + [' '] + ['&'] + ['Enter']
    subprocess.run(command)

# Define the function to handle messages
def handle_message(update, context):
    # Get the received message text
    message_text = update.message.text.lower()

    # Check if the message text is 'p'
    if message_text == 'p':
        # If user type p then run func p 
        launch_script_p(update, context)
    elif message_text.startswith('y '):
        
        launch_script_y(update, context)
    elif message_text.startswith('n '):
        launch_script_n(update, context)

    elif message_text.startswith('h'):
        help_p(update, context)

    elif message_text.startswith('.') or message_text[0].isdigit() and ('.' in message_text or not message_text[1:].isdigit()):
        # Extract the number and arguments from the user input
         parts = message_text.split()
         if len(parts) >= 3:
             number_str = Decimal(parts[0])
             number = str(number_str)
             currency = parts[1]
             sentiment = parts[2]
             args = parts[3:5]
             if len(parts) >= 4:
                 description = ' '.join(parts[3:]) #If length greather than 4 then add description
             else:
                 description = None
             Price_alert(update, context, number, currency, sentiment, args, description)
         else:
             update.message.reply_text("Incorrect argument format. Please provide a number followed by two arguments.")    
    else:
        update.message.reply_text("Unrecognized command. Please use 'p', 'y', or 'n' followed by arguments.")

# Set up the Telegram bot
updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

# Register the command handler for 'p' command
dispatcher.add_handler(CommandHandler('p', launch_script_p))

dispatcher.add_handler(CommandHandler('number', Price_alert))

dispatcher.add_handler(CommandHandler('h', help_p, pass_args=True))

dispatcher.add_handler(CommandHandler('n', launch_script_n))
# Register the message handler
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot
updater.start_polling()
