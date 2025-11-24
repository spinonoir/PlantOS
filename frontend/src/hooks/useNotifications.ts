import * as Notifications from "expo-notifications";
import { useEffect } from "react";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

export function useNotificationBootstrap() {
  useEffect(() => {
    Notifications.requestPermissionsAsync().catch((error) => {
      console.warn("Notification permissions error", error);
    });
  }, []);
}

export async function scheduleReminder(
  title: string,
  body: string,
  seconds = 5,
) {
  await Notifications.scheduleNotificationAsync({
    content: { title, body },
    trigger: { seconds },
  });
}

export async function cancelReminder(identifier: string) {
  await Notifications.cancelScheduledNotificationAsync(identifier);
}
