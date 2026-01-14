import Card from "./Card";

export default function NotificationSettings() {
  return (
    <Card title="Notification Settings">
      <div className="space-y-4 text-gray-700">
        <div className="flex items-center justify-between">
          <span>Email Notifications</span>
          <input type="checkbox" className="w-5 h-5" />
        </div>

        <div className="flex items-center justify-between">
          <span>SMS Notifications</span>
          <input type="checkbox" className="w-5 h-5" />
        </div>

        <div className="flex items-center justify-between">
          <span>Push Notifications</span>
          <input type="checkbox" className="w-5 h-5" />
        </div>
      </div>
    </Card>
  );
}
