from discord.ext import commands
import random
import json
import re


with open("./config.json", "r") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix="$")


async def get_random_number(ctx, arg):
    min_num = int(arg[1])
    max_num = int(arg[2])
    random_number = random.randint(min_num, max_num)

    await ctx.send(random_number)


async def get_random_option(ctx, arg):
    sample_num = int(arg[1])
    sample_set = arg[2:]
    if sample_num < 0:
        sample_num = len(sample_set)
    sample = random.sample(sample_set, sample_num)

    await ctx.send("\n".join(sample))

async def get_credits(ctx, arg):
    credits = ["Created by NAEK"]
    credits_joined = "\n".join(credits)
    
    await ctx.send(credits_joined)

async def play_roulette(ctx, arg):
    player_choice = []

    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    green = [37, 38]

    roulette_choice = random.randint(1, 38)
    color = ""

    if roulette_choice in red:
        color = "red"
    if roulette_choice in black:
        color = "black"
    if roulette_choice in green:
        color = "green"
        roulette_choice = 0 if roulette_choice == 37 else "00"

    if len(arg) > 1:
        player_choice = " ".join(arg[1:]).lower()
        number_regex = re.compile(r"(\d+)").findall(player_choice)
        color_regex = re.compile(r"(black|red|green)").findall(player_choice)
        player_outcome = "won"
        if color_regex:
            player_color = color_regex.pop()
        else:
            color_regex = None
        if number_regex:
            player_number = number_regex.pop()
        else:
            player_number = None

        if player_color and player_color.lower() != color.lower():
            player_outcome = "lost"

        if player_number and str(roulette_choice) != str(player_number):
            player_outcome = "lost"

        end_message = ["You {}.".format(player_outcome), "{} {}".format(color.capitalize(), roulette_choice)]

        await ctx.send("\n".join(end_message))
        return

    await ctx.send("{} {}".format(color.capitalize(), roulette_choice))


@bot.command(name="random")
async def arg_random(ctx, *arg):
    if arg[0] == "number":
        await get_random_number(ctx, arg)
    if arg[0] == "option":
        await get_random_option(ctx, arg)


@bot.command(name="play")
async def arg_play(ctx, *arg):
    if arg[0] == "roulette":
        await play_roulette(ctx, arg)


bot.run(config.get("bot_token"))
