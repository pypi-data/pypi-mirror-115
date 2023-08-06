from asyncio import sleep

from nonebot import on_notice
from nonebot.adapters.cqhttp import Bot, Event

bugu = on_notice(priority=5)


@bugu.handle()
async def message_discernment_handle(bot: Bot, event: Event):
    print(f'检测到事件:{event.notice_type}')
    if event.notice_type == 'group_increase':
        new_id = event.user_id
        print(f'检测到受害者:{new_id}')
        new_group = event.group_id
        await sleep(3)

        await bugu.send('您好我是您朋友给您点的布谷鸟')
        await sleep(0.5)
        await bugu.send('祝您在新的一年里')
        await sleep(0.5)
        await bugu.send('布谷布谷布谷布谷布谷布谷布谷布谷')
        await sleep(0.5)
        await bugu.send('不孤不孤不孤不孤不孤不孤不孤不孤')
        await sleep(0.5)
        await bugu.send('布谷布谷布谷布谷布谷布谷布谷布谷')
        await sleep(0.5)
        await bugu.send('不孤不孤不孤不孤不孤不孤不孤不孤')
        await sleep(0.5)
        await bugu.send('布谷布谷布谷布谷布谷布谷布谷布谷')
        await sleep(0.5)
        await bugu.send('不孤不孤不孤不孤不孤不孤不孤不孤')
        await sleep(0.5)
        await bugu.send('服务完毕,欢迎您明年再来')

        await bot.set_group_kick(group_id=new_group, user_id=new_id)
