from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Command(BaseCommand):
    help = 'Prints all active WebSocket connections'

    def handle(self, *args, **options):
        channel_layer = get_channel_layer()
        channels = async_to_sync(
            channel_layer.group_channels)('websocket_group')
        for channel_name, _ in channels:
            self.stdout.write(self.style.SUCCESS(
                f"WebSocket connection: {channel_name}"))
