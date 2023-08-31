import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from discord import Member, Permissions
from .subscribe import subscribe


class CustomMockContext:
    def __init__(self, author):
        self.author = author

    async def respond(self, message, view=None):
        pass


class SubscribeTest(IsolatedAsyncioTestCase):
    async def test_subscribe(self):
        # Create a mock author object with guild_permissions
        author = MagicMock(spec=Member)
        author.guild_permissions = MagicMock(spec=Permissions)
        author.guild_permissions.manage_guild = True

        # Create a mock channel object
        channel = MagicMock()
        channel.id = 123456789

        # Create a mock bot object
        bot = MagicMock()

        # Create a mock view object
        view = MagicMock()

        # Set up the mock view object
        view.add_item.return_value = None

        # Set up the mock bot's slash_command decorator
        bot.slash_command.return_value = MagicMock()

        # Create a custom mock context using the author object
        ctx = CustomMockContext(author)

        # Patch the respond method as a MagicMock object
        with patch.object(ctx, 'respond', new_callable=AsyncMock) as mock_respond:
            # Call the subscribe function
            await subscribe(ctx, channel)

            # Assert that the respond method was called with the expected arguments
            mock_respond.assert_called_once()
            call_args = mock_respond.call_args[0]
            self.assertEqual(call_args[0], f"Pick the channel you'd like to subscribe {channel} to:")
            self.assertEqual(len(call_args), 1)  # Only the message argument was passed


if __name__ == '__main__':
    unittest.main()