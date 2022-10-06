from disnake import Embed
from disnake.embeds import EmptyEmbed


class ClearEmbed(Embed):
    def __init__(self, title=EmptyEmbed, description=EmptyEmbed):
        super().__init__(title=title, description=description, color=3092790)