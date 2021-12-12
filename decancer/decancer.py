import discord
from discord.ext import commands
import stringcase
import re
import random
import unicodedata
from unidecode import unidecode


class Decancer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.coll = bot.plugin_db.get_partition(self)

	nouns = [
		"Dog",
		"Cat",
		"Gamer",
		"Ork",
		"Memer",
		"Robot",
		"Programmer",
		"Player",
		"Doctor",
		"Apple",
		"Godfather",
		"Mafia",
		"Detective",
		"Politician"
	]

	adjectives = [
		"Fast",
		"Defiant",
		"Homeless",
		"Adorable",
		"Delightful",
		"Homely",
		"Quaint",
		"Adventurous",
		"Depressed",
		"Horrible",
		"Aggressive",
		"Determined",
		"Hungry",
		"Real",
		"Agreeable",
		"Different",
		"Hurt",
		"Relieved",
		"Alert",
		"Difficult",
		"Repulsive",
		"Alive",
		"Disgusted",
		"Ill",
		"Rich",
		"Amused",
		"Distinct",
		"Important",
		"Angry",
		"Disturbed",
		"Impossible",
		"Scary",
		"Annoyed",
		"Dizzy",
		"Inexpensive",
		"Selfish",
		"Annoying",
		"Doubtful",
		"Innocent",
		"Shiny",
		"Anxious",
		"Drab",
		"Inquisitive",
		"Shy",
		"Arrogant",
		"Dull",
		"Itchy",
		"Silly",
		"Ashamed",
		"Sleepy",
		"Attractive",
		"Eager",
		"Jealous",
		"Smiling",
		"Average",
		"Easy",
		"Jittery",
		"Smoggy",
		"Awful",
		"Elated",
		"Jolly",
		"Sore",
		"Elegant",
		"Joyous",
		"Sparkling",
		"Bad",
		"Embarrassed",
		"Splendid",
		"Beautiful",
		"Enchanting",
		"Kind",
		"Spotless",
		"Better",
		"Encouraging",
		"Stormy",
		"Bewildered",
		"Energetic",
		"Lazy",
		"Strange",
		"Enthusiastic",
		"Light",
		"Stupid",
		"Bloody",
		"Envious",
		"Lively",
		"Successful",
		"Blue",
		"Evil",
		"Lonely",
		"Super",
		"Blue-eyed",
		"Excited",
		"Long",
		"Blushing",
		"Expensive",
		"Lovely",
		"Talented",
		"Bored",
		"Exuberant",
		"Lucky",
		"Tame",
		"Brainy",
		"Tender",
		"Brave",
		"Fair",
		"Magnificent",
		"Tense",
		"Breakable",
		"Faithful",
		"Misty",
		"Terrible",
		"Bright",
		"Famous",
		"Modern",
		"Tasty",
		"Busy",
		"Fancy",
		"Motionless",
		"Thankful",
		"Fantastic",
		"Muddy",
		"Thoughtful",
		"Calm",
		"Fierce",
		"Mushy",
		"Thoughtless",
		"Careful",
		"Filthy",
		"Mysterious",
		"Tired",
		"Cautious",
		"Fine",
		"Tough",
		"Charming",
		"Foolish",
		"Nasty",
		"Troubled",
		"Cheerful",
		"Fragile",
		"Naughty",
		"Clean",
		"Frail",
		"Nervous",
		"Ugliest",
		"Clear",
		"Frantic",
		"Nice",
		"Ugly",
		"Clever",
		"Friendly",
		"Nutty",
		"Uninterested",
		"Cloudy",
		"Frightened",
		"Unsightly",
		"Clumsy",
		"Funny",
		"Obedient",
		"Unusual",
		"Colorful",
		"Obnoxious",
		"Upset",
		"Combative",
		"Gentle",
		"Odd",
		"Uptight",
		"Comfortable",
		"Gifted",
		"Old-fashioned",
		"Concerned",
		"Glamorous",
		"Open",
		"Vast",
		"Condemned",
		"Gleaming",
		"Outrageous",
		"Victorious",
		"Confused",
		"Glorious",
		"Outstanding",
		"Vivacious",
		"Cooperative",
		"Good",
		"Courageous",
		"Gorgeous",
		"Panicky",
		"Wandering",
		"Crazy",
		"Graceful",
		"Perfect",
		"Weary",
		"Creepy",
		"Grieving",
		"Plain",
		"Wicked",
		"Crowded",
		"Grotesque",
		"Pleasant",
		"Wide-eyed",
		"Cruel",
		"Grumpy",
		"Poised",
		"Wild",
		"Curious",
		"Poor",
		"Witty",
		"Cute",
		"Handsome",
		"Powerful",
		"Worrisome",
		"Happy",
		"Precious",
		"Worried",
		"Dangerous",
		"Healthy",
		"Prickly",
		"Wrong",
		"Dark",
		"Helpful",
		"Proud",
		"Dead",
		"Helpless",
		"Putrid",
		"Zany",
		"Defeated",
		"Hilarious",
		"Puzzled",
		"Zealous",
		"Dank",
		"Sexy",
		"Darth"
	]

	@staticmethod
	def is_cancerous(text: str) -> bool:
		for segment in text.split():
			for char in segment:
				if not (char.isascii() and char.isalnum()):
					return True
		return False

	# the magic
	@staticmethod
	def strip_accs(text):
		try:
			text = unicodedata.normalize("NFKC", text)
			text = unicodedata.normalize("NFD", text)
			text = unidecode(text)
			text = text.encode("ascii", "ignore")
			text = text.decode("utf-8")
		except Exception as e:
			print(e)
		return str(text)

	# the magician
	async def nick_maker(self, old_shit_nick):
		try:
			old_shit_nick = self.strip_accs(old_shit_nick)
			new_cool_nick = re.sub("[^a-zA-Z0-9 \n.]", "", old_shit_nick)
			new_cool_nick = " ".join(new_cool_nick.split())
			new_cool_nick = stringcase.lowercase(new_cool_nick)
			new_cool_nick = stringcase.titlecase(new_cool_nick)
			if len(new_cool_nick.replace(" ", "")) <= 1 or len(new_cool_nick) > 32:
				return f"{random.choice(self.adjectives)} {random.choice(self.nouns)}"
			return new_cool_nick
		except Exception as exc:
			return f"{random.choice(self.adjectives)} {random.choice(self.nouns)}" if type(
				exc) == str else 'Moderated Nickname'

	@commands.Cog.listener()
	async def on_member_join(self, member):
		random_nick = f"{random.choice(self.adjectives)} {random.choice(self.nouns)}"
		nice_nick = await self.nick_maker(member.display_name)

		if member.display_name.lower() == nice_nick.lower():
			return

		nick = nice_nick if 3 < len(nice_nick) < 32 else random_nick

		channel = self.bot.get_channel(676931619294281729)
		await member.edit(nick=nick)
		return await channel.send(f'Decancered `{member.name}` to {nick}')

	@commands.check_any(
		commands.has_permissions(manage_nicknames=True),
		commands.has_role('Farm Hand - Chat Moderator')
	)
	@commands.command(name='decancer', aliases=['dc'])
	async def decancer(self, ctx, member: discord.Member):

		random_nick = f"{random.choice(self.adjectives)} {random.choice(self.nouns)}"
		nice_nick = await self.nick_maker(member.display_name)
		bad_nick = member.display_name

		if member.top_role.position >= ctx.author.top_role.position:
			return await ctx.send('<a:youtried:881184651232817232> lol')

		if nice_nick.lower() == bad_nick.lower():
			return await ctx.send('What are you trying to decancer huh? Its pingable smh')

		nick = nice_nick if 3 < len(nice_nick) < 32 else random_nick
		await member.edit(nick=nick)

		return await ctx.send(
			embed=discord.Embed(title='Randomized their nickname since I couldnt decancer!',
								colour=discord.Colour.red(),
								description=f'**Old nick:** {bad_nick}\n**New nick:** {nick}'))

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.nick != after.nick:
			frozencheck = await self.coll.find_one({"user_id": str(after.id)})
			if not frozencheck:
				return
			frozennick = frozencheck['Nickname']
			await after.edit(nick=frozennick)

	@commands.check_any(
		commands.has_permissions(manage_nicknames=True)
	)
	@commands.command()
	async def freezenick(self, ctx, user: discord.Member, *, Nickname: str):
		if user.top_role.position >= ctx.author.top_role.position:
			return await ctx.send('<a:youtried:881184651232817232> lol')

		frozenadd = {"user_id": str(user.id), "Nickname": Nickname}
		await self.coll.insert_one(frozenadd)
		await ctx.send(f'Trying to freeze {user.nick} to {Nickname}')
		await user.edit(nick=Nickname)
		await ctx.send('Done!')

	@commands.check_any(
		commands.has_permissions(manage_nicknames=True)
	)
	@commands.command()
	async def unfreezenick(self, ctx, user: discord.Member):
		frozencheck = await self.coll.find_one({"user_id": str(user.id)})
		if frozencheck is None:
			return
		await self.coll.delete_one(frozencheck)
		await ctx.send(f'I unfreezed <@{user.id}>')


def setup(bot):
	bot.add_cog(Decancer(bot))
