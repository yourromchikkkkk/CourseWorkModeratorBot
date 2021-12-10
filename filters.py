from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


## custom filter to check if user, which use some command is admin
class isAdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(selfself, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


## Filter that checks member ability for restricting
class MemberCanRestrictFilter(BoundFilter):
    key = 'member_can_restrict'

    def __init__(self, member_can_restrict: bool):
        self.member_can_restrict = member_can_restrict

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        # I don't know why, but telegram thinks, if member is chat creator, he cant restrict member
        return (member.is_chat_creator() or member.can_restrict_members) == self.member_can_restrict
