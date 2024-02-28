from telegram import Update
from telegram.ext import CallbackContext, CommandHandler 

from shivu import application, top_global_groups_collection, pm_users, OWNER_ID 


async def broadcast(update: Update, context: CallbackContext) -> None:
    OWNER_ID = '6655070772'  # Set the OWNER_ID directly within the function

    if str(update.effective_user.id) == OWNER_ID:
        if update.message.reply_to_message is None:
            await update.message.reply_text('Please reply to a message to broadcast.')
            return

        all_users = await user_collection.find({}).to_list(length=None)
        all_groups = await group_user_totals_collection.find({}).to_list(length=None)

        unique_user_ids = set(user['id'] for user in all_users)
        unique_group_ids = set(group['group_id'] for group in all_groups)

        total_sent = 0
        total_failed = 0

        for user_id in unique_user_ids:
            try:
                await context.bot.forward_message(chat_id=user_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        for group_id in unique_group_ids:
            try:
                await context.bot.forward_message(chat_id=group_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Broadcast report:\n\nTotal messages sent successfully: {total_sent}\nTotal messages failed to send: {total_failed}'
        )
    else:
        await update.message.reply_text('Only Murat Can use')


async def broadcast2(update: Update, context: CallbackContext) -> None:
    OWNER_ID = '6655070772'  # Set the OWNER_ID directly within the function

    if str(update.effective_user.id) == OWNER_ID:
        if update.message.reply_to_message is None:
            await update.message.reply_text('Please reply to a message to broadcast.')
            return

        all_groups = await group_user_totals_collection.find({}).to_list(length=None)
        unique_group_ids = set(group['group_id'] for group in all_groups)

        total_sent = 0
        total_failed = 0

        for group_id in unique_group_ids:
            try:
                await context.bot.forward_message(chat_id=group_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Broadcast report:\n\nTotal messages sent successfully: {total_sent}\nTotal messages failed to send: {total_failed}'
        )
    else:
        await update.message.reply_text('Only the owner can use this command for group broadcast.')


application.add_handler(CommandHandler('broadcast2', broadcast2, block=False))
application.add_handler(CommandHandler('broadcast', broadcast, block=False))


