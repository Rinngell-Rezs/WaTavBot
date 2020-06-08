from telegram import *
from telegram.ext import *
import json
from html import escape

def battle(update:Update,context:CallbackContext):
    global ArenaList,tmpPlayers
    query = update.callback_query
    data = json.loads(query.data)

    option,phase = data["op"].split("|")
    if("mov:" in phase):
        phase,mov = phase.split(":")
    room = data['room']
    host = int(data['host'])
    try:
        host_link = ('<a href="tg://user?id={}">{}</a>'.format(host,escape(tmpPlayers[host]['first_name']))).strip()
    except KeyError as e:
        context.bot.answerCallbackQuery(query.id,"This session has expired.",True)
        context.bot.edit_message_text(
                                        text="❓",
                                        inline_message_id=query.inline_message_id,
                                        parse_mode=ParseMode.HTML)
        #error(update,e)
        return

    presser = update.effective_user
    presser_link = ('<a href="tg://user?id={}">{}</a>'.format(presser.id,escape(presser.first_name))).strip()

    if(phase == 'p2'):
        if(host == presser.id):
            quotes = ['The most difficult struggles are the ones you fight with yourself...',
                'A fight with yourself to win the battle for yourself is the biggest and most important one.',
                'Fight with yourself to get the best from yourself.',
                'When you fight yourself to discover the real you, there\'s only one winner.',
                'You don\'t realize how strong you are until you\'re fighting yourself.',
                'It isn\'t ever the world you fight. Always, always, it\'s yourself.',
                'The toughest battle you\'ll ever fight in your life is the battle within yourself.',
                'Fight with others doesn\'t make you sleepless; fighting with yourself is what makes you restless.']
            context.bot.answerCallbackQuery(query.id,'“'+choice(quotes)+'”',True)
            return
        else:
            text = '<b>⚔Duel</b>\nBoth opponents are set! \n%s will face %s on the arena! \n<i>May the gods be with you, warriors...</i>\n\nWaiting for the host to start the duel...'%(host_link,presser_link)
            ArenaList[room] = ArenaObject(
                                            room = room,
                                            P1 = Player(tmpPlayers[host]['first_name'],tmpPlayers[host]['last_name'],host),
                                            P2 = Player(presser.first_name,presser.last_name,presser.id),
                                            text = text)
            context.bot.edit_message_text(
                                            text=text,
                                            inline_message_id=query.inline_message_id,
                                            reply_markup = InlineKeyboardMarkup (
                                                                                    [
                                                                                        [
                                                                                            InlineKeyboardButton(
                                                                                                text = "Start the match!",
                                                                                                callback_data = "{\"op\":\"batt|start\",\"room\":\"%s\",\"host\":\"%s\"}"%(room,host)
                                                                                            )
                                                                                        ]
                                                                                    ]
                                                                                ),
                                            parse_mode=ParseMode.HTML)
            return
    arena = ArenaList[room]#From here on, there's only blood and glory!
    if(presser.id not in list(arena.Players.keys())):
        context.bot.answerCallbackQuery(query.id,"What are you doing? This is not your Fight!",True)
        return
    elif(phase == 'start'):
        P1,P2 = arena.Players.keys()
        text = "<b>⚔Duel</b>\nThe match has started!\n%s❤️ %s\nVs\n%s❤️ %s\n\nRound: %s\nWhat will you do?\n<b>Choose attack and defense points.</b>"%(
            str(arena.Players[P1].hp),
            arena.Players[P1].link,
            str(arena.Players[P2].hp),
            arena.Players[P2].link,
            arena.round)
        context.bot.edit_message_text(
                                        text=text,
                                        inline_message_id=query.inline_message_id,
                                        reply_markup=InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host))),
                                        parse_mode=ParseMode.HTML)
        arena.throwChronos()

    elif(phase == 'mov'):
        act = {'a':'Attack','d':'Defend'}
        part = {'h':'Head','b':'Body','l':'Legs'}
        mc = arena.movAssign(presser.id,mov)
        if(mc):
            context.bot.answerCallbackQuery(query.id,act[mov[0]]+' '+part[mov[1]],False)
        else:
            context.bot.answerCallbackQuery(query.id,"Sorry, you already chose what to %s"%(act[mov[0]]),True)
        if(arena.movCheck()):
            battletext = arena.dmgCalc()
            arena.round += 1
            p1,p2 = list(arena.Players.keys())
            p1n = arena.Players[p1].link
            p1t = arena.Players[p1].time
            p1h = arena.Players[p1].hp

            p2n = arena.Players[p2].link
            p2t = arena.Players[p2].time
            p2h = arena.Players[p2].hp
            text = """<b>⚔Duel⚔</b> round: %s
            %s

%s took %s seconds\n has ❤️%s remaining.\n
%s took %s seconds\n has ❤️%s remaining.
"""%(
                str(arena.round),
                battletext,
                p1n,
                str(p1t),
                str(p1h),
                p2n,
                str(p2t),
                str(p2h))
            if(p1h > 0 and p2h > 0 ):
                arena.movClear()
                arena.throwChronos()
                rpmkup = InlineKeyboardMarkup(kb.kb(op='hits',args=(room,host)))
            else:
                text = arena.lifeCheck()
                rpmkup = None
            try:
                context.bot.edit_message_text(
                                                text=text,
                                                inline_message_id=query.inline_message_id,
                                                reply_markup=rpmkup,
                                                parse_mode=ParseMode.HTML)
            except Exception as e:
                error(update,e)

    return
