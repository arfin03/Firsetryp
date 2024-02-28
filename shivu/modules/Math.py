from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import re
from Grabber import application

def math(update: Update, context: CallbackContext):
    # Extract the command arguments
    args = context.args
    
    # Check if the user provided the correct number of arguments
    if len(args) != 3:
        update.message.reply_text("Please provide the command in the format /math <number> <operator> <number>")
        return
    
    # Extract the numbers and operator
    num1, operator, num2 = args
    
    # Check if the numbers are valid
    if not (num1.isdigit() and num2.isdigit()):
        update.message.reply_text("Please provide valid numbers.")
        return
    
    num1 = float(num1)
    num2 = float(num2)
    
    # Perform the operation based on the operator
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        if num2 == 0:
            update.message.reply_text("Cannot divide by zero.")
            return
        result = num1 / num2
    else:
        update.message.reply_text("Invalid operator. Please use one of +, -, *, /")
        return
    
    update.message.reply_text(f"Result: {result}")


application.add_handler(CommandHandler("math", math))
