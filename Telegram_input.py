import subprocess
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import html

# Parse telegram input and do some action based on the input. 

# Define the function to handle the 'n' command
def launch_script_n(update, context):
    # Get the arguments passed by the user
    message_text = update.message.text.lower()
    args = message_text.split()[1:]  # Remove the first element 'n' from the message text

    if len(args) != 2:
        # Send an error message to the user indicating the incorrect argument format
        update.message.reply_text("Incorrect argument format for 'n' command. Please provide 2 arguments.")
        return 

    command = ['tmux', 'send-keys', '-t', 'ifvalues', '/root/newstart/newtest1.sh'] + [' '] + list(' '.join(args)) + [' '] + ['&'] + ['Enter']
 # Execute the another script with arguments using subprocess
    subprocess.run(command)


# Define the function to handle the 'p' command
def launch_script_p(update, context):
    # Execute your script for command 'p' using subprocess and capture the output
    output = subprocess.check_output(['bash', '/files/price5.sh']).decode('utf-8')

    # Escape special characters in the output text
    escaped_output = html.escape(output)

    # Format the output using HTML
    formatted_output = f"<pre>{escaped_output}</pre>"

    # Send the formatted output as a response message
    update.message.reply_html(formatted_output)

# Define the function to handle the 'y' command
def launch_script_y(update, context):
    # Get the arguments passed by the user
    message_text = update.message.text.lower()
    args = message_text.split()[1:]  # Remove the first element 'y' from the message text

    if len(args) != 4:
        # Send an error message to the user indicating the incorrect argument format
        update.message.reply_text("Incorrect argument format for 'y' command. Please provide 4 arguments.")
        return

    command = ['tmux', 'send-keys', '-t', 'ifvalues', '/root/newstart/15min/15min2.sh'] + [' '] + list(' '.join(args)) + [' '] + ['&'] + ['Enter']
     # Execute the tmux command with arguments using subprocess
    subprocess.run(command)

# Define the function to handle messages
def handle_message(update, context):
    # Get the received message text
    message_text = update.message.text.lower()

    # Check if the message text is 'p'
    if message_text == 'p':
        # Call the function to handle 'p' command
        launch_script_p(update, context)
    elif message_text.startswith('y '):
        # Call the function to handle 'y' command with arguments
        launch_script_y(update, context)
    elif message_text.startswith('n '):
        # Call the function to handle 'n' command with arguments
        launch_script_n(update, context)
    else:
        # Send an error message to the user for unrecognized commands
        update.message.reply_text("Unrecognized command. Please use 'p', 'y', or 'n' followed by arguments.")

# Set up the Telegram bot
updater = Updater(token='5640166055:AAE4vMzP-lk2dh-fszrejyRFBhCCp1UCGXI')
dispatcher = updater.dispatcher

# Register the command handler for 'p' command
dispatcher.add_handler(CommandHandler('p', launch_script_p))

# Register the message handler
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot
updater.start_polling()
