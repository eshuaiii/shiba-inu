import discord
from discord.ext import commands, tasks
import logging
import random
import os
import asyncio
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='$') # create the bot

# --- Logging ---
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# --- Variables ---
wellness = ["What have you done lately just for you?", "What is your favorite memory?", "What are you most grateful for right now?", "What thought patterns are holding you back right now?", "What are you afraid of?", "What does success mean to you?", "What limiting beliefs are holding you back from living your dream life?", "What are you grateful for this week?", "What have you done lately that you are proud of?", "What are your priorities for this year?", "What is one adjustment you’d like to make to your morning routine?", "What is one adjustment you’d like to make to your evening routine?", "How do you remind yourself that you’re enough?", "What’s your ultimate goal in life?", "What is causing you stress right now?", "What is one thing you can do today to reduce stress in your life?", "If I could talk to my younger self, the one thing I would say is…", "Describe the most unforgettable moment in your life.", "Name what is enough for you.", "What do you love about life?", "Describe yourself in 10 words or less", "Write about a failure you had. What can you learn from that?", "Make a list of everything you’d like to say no to. How many of these are you currently doing?", "Make a list of everything you’d like to say yes to. How many of these are you currently doing?", "How will making myself a priority positively impact my life?", "What are 3 things that I’m currently doing that no longer serve me? How can I stop doing these things?", "What can I do to add more flow and relaxation to my day?", "When I’m really busy how can I find 10 minutes of time for myself? What can I do in that time?", "Write a letter of gratitude to yourself for looking after your own wellbeing. ", "What’s one positive habit I can make in my daily life?", "Consider your mindset. Is it serving you? How can you make a shift if it isn’t working for you?", "How can you celebrate yourself today?", "What helps you slow down and feel more present?", "How do you stay focused and steer clear of distractions?", "How do you notice when you’re nearing burnout?", "How do you ask for help or support when you need it?", "What Things Make You Happy", "What’s a funny story that makes you laugh every time?", "What brings you genuine joy?", "What makes you happiest in life?", "What are you proud of yourself for?", "One thing I need to work on is __________", "What do you need to forgive yourself for?", "Name a habit you need to stop doing to live a more meaningful life?", "What is your proudest moment?", "I’m most proud that I __________", "What makes you feel powerful?", "What could you do to make your life more joyful every day?", "How can I show myself more love?", "When do you feel most confident?", "Make a list of 30 things that make you smile.", "What does unconditional love look like for you?", "Write the words that would make you happier today.", "What acts of self-care truly make me happy? How can I add more of this to my self care routine?", "I feel happiest when ______________.", "What personal needs am I sacrificing to meet the needs of others?", "What makes me feel calm?", "What makes you feel in control?", "How do you put yourself first without feeling guilty?", "How do you practice self-acceptance?", "How do you set boundaries and avoid taking on someone else’s emotions and stress?", "How do you advocate for yourself?", "How do you forgive yourself when you make a mistake?", "How do you calm your nerves in a difficult situation?", "How do you trust yourself to make big decisions?", "What does your dream life look like?", "What do you want your life to look like three years from now?", "What do you want your legacy to be?", "What do you need to let go of?", "What would your ideal day look like?", "What do you need most to heal right now?", "What do you need to forgive yourself for?", "What would you do if it was impossible to fail?", "What does your ideal day look like from morning to night?", "What do you wish you had more time for?", "What’s the best dream you can remember?", "A mantra I’d like to live by is…", "What would you do if you loved yourself unconditionally? How would you treat yourself? How can you start doing that now?", "Is my morning serving me well? What does it look like? Do I have a routine? Are mornings rushed?", "I am the best version of myself when I...", "Am I living in alignment with my values?  What can I change to make this happen?", "How do you savor the time you get alone?", "How do you embrace your true self, even if it looks different from what others expect?", "Write a letter to yourself from the future version of you. Tell yourself how awesome your life is now.", "If you could make a living doing anything, what would it be?", "What are some things that inspire you?", "How have you been getting in the way of achieving your goals?", "What did you/can you do today to bring yourself closer to your dream?", "What is your best accomplishment?", "A book that has impacted me is __________", "What’s inspiring you right now?", "What wild and crazy thing would you like to try?", "What have you learned today?", "If I could accomplish one thing in the next three months, what would it be?", "A topic you want to learn about that will help you be happier? How can you start learning about it?", "How can I encourage myself when I’m trying something new?", "What can you do today that you didn’t think you could do a year ago?", "How can you step outside your comfort zone to grow?", "Who is your best friend?", "Who is someone you’d like to treat better?", "Who is your favorite person to talk to?", "Who’s your biggest idol?", "What makes you a good friend?", "What qualities do you think others admire about you?", "How do you add value to those nearest to you?", "Who inspires you most in life?", "What is your favorite personality trait?", "Make a list of the people in your life who make up your support system.", "I really wish others knew this about me…", "Name a way you’ve supported a friend recently. How can you do the same for yourself?", "How do you share your feelings with the people who care about you?", "How do you make the time you spend with people more intentional?", "If you could take a vacation anywhere in the world, where would it be?", "What do I need more of in my life?", "When you wake up in the morning, how do you want to feel?", "How do you add value to the world?", "My favorite way to spend the day is…", "I couldn’t imagine living without…", "Write the obstacles you face for practicing self-care daily. How can you overcome at least one of them?", "A space in my home that makes me feel happy. ", "When is the best time in my day to practice self-care?", "I am grateful to money because_________.", "Write all of the ways money will help you live to your fullest potential.", "What feelings come up when I think about my desire for money?", "What did your parents teach you about money?", "What is my biggest challenge with managing money? What step can I take to change that?", "What is your ideal income? How would your life be impacted as a result of earning this amount?", "Reflect on a past money mistake? How can you forgive yourself for this?", "What’s your favorite physical feature?", "What items are in your self-care toolkit?", "Today I can honor my body by _________", "If my body could talk, it would say…", "I feel most energized when…", "I feel happiest in my skin when…", "Today my self care mantra is…", "How do I feel about the importance of practicing self-care?", "Self-care is important to me because I want to feel _________.", "What does bedtime look and feel like? Is there anything I can change for a more restful night’s sleep?", "Reflect on a time when I didn’t practice self-care and write about all the positive changes I’ve made in my life.", "What would I say to someone that thinks self-care is selfish?", "What’s something I can do to feel good today? ", "How do you recharge?"]
daily_prompt = True
wellness_channel = # your channel ID here

@bot.command(name='echo', help='Get the bot to say something!')
async def echo(ctx, arg):
    await ctx.send(arg)

@bot.command(name='ping', help='Check to see if the bot is online.')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='prompt', help="Generate a random wellness prompt!")
async def send_prompt(ctx):
    print(type(ctx))
    message = "Hi everyone! Here is today's prompt!"
    x = random.randint(0, len(wellness))
    if type(ctx) == discord.ext.commands.context.Context:
        ctx = ctx.message.channel
        print("invoked by command")
        message = "Here's your wellness prompt!"
    embed = discord.Embed(title="Prompt", description=f"{message}\n\n**{wellness[x]}**", color=random.randint(0, 0xFFFFFF))
    await ctx.send(embed=embed)
    await ctx.send(f"{message} **{wellness[x]}**")
    await ctx.edit(topic=f"Today's Prompt: **{wellness[x]}**")
    # try:
    # call_channel = ctx.channel
    # except AttributeError:
    #     channel = ctx
    # finally:
    # print(type(ctx))
    # x = random.randint(0, len(wellness))
    # await ctx.channel.send(wellness[x])
    # await ctx.channel.edit(topic=f"Today's Prompt: **{wellness[x]}**")

@bot.command(name='dailyprompt', help="Generate a wellness prompt daily. \"on\" to turn this feature on, and \"off\" to turn this feature off.")
async def dailyprompt(ctx, arg):
    global daily_prompt
    if arg.lower() == "on":
        daily_prompt = True
        await ctx.send("Daily prompt is turned on.")
    elif arg.lower() == "off":
        daily_prompt = False
        await ctx.send("Daily prompt is turned off.")
    else:
        await ctx.send("Sorry, that's not a valid argument! Use \"on\" to turn this feature on, or \"off\" to turn this feature off.")


@bot.command(name='hours', help="Start a study session on Hours. Sets channel description.")
async def hours(ctx, link):
  await ctx.channel.edit(topic=link)
  await ctx.send(f"Done! Hours Study Session: {link}")

# https://stackoverflow.com/questions/57631314/making-a-bot-that-sends-messages-at-a-scheduled-date-with-discord-py
@tasks.loop(seconds=30)
async def called_once_a_day():
    if daily_prompt == False:
        pass
    else:
        message_channel = bot.get_channel(wellness_channel)
        print(f"Got channel {message_channel}")
        await send_prompt(message_channel)

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")
    now = datetime.now()
    print(now)
    # if now.hour > 15: # currently set to 8 AM, or 3 PM UTC
    #   next_time = datetime(now.year, now.month, now.day + 1, 15, 0, 0, 0)
    # else:
    #   next_time = datetime(now.year, now.month, now.day, 15, 0, 0, 0)
    # print(next_time)
    # diff = next_time - now
    # print(f"Time calculation complete. Will sleep for {diff.total_seconds()} seconds.")
    # await asyncio.sleep(diff.total_seconds())
    

called_once_a_day.start()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run('<<secret API here>>')