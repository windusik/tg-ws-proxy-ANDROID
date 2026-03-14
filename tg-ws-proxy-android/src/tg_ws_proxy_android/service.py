from android.app import NotificationChannel, NotificationManager
from android.content import Context
from androidx.core.app import NotificationCompat

class SimpleNotificationService:
    def __init__(self, app):
        self.app_context = app._impl.native  # Получаем контекст Android Activity
        self.CHANNEL_ID = "bg_service_channel"

    def start(self):
        # 1. Создаем канал
        notification_manager = self.app_context.getSystemService(Context.NOTIFICATION_SERVICE)
        channel = NotificationChannel(
            self.CHANNEL_ID, 
            "Background Service", 
            NotificationManager.IMPORTANCE_LOW
        )
        notification_manager.createNotificationChannel(channel)

        # 2. Строим уведомление
        builder = NotificationCompat.Builder(self.app_context, self.CHANNEL_ID)
        builder.setContentTitle("Прокси работает")
        builder.setContentText("Телеграм должен тоже...")
        builder.setSmallIcon(self.app_context.getApplicationInfo().icon)
        builder.setOngoing(True)  # Постоянное уведомление

        # 3. Показываем уведомление (id=1)
        notification_manager.notify(1, builder.build())