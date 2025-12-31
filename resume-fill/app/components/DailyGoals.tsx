import Card from "./Card";

export default function DailyGoals() {
  return (
    <Card title="Daily Goals">
      <ul className="space-y-2 text-sm text-gray-700">
        <li>• Apply to 3 Jobs</li>
        <li>• Update Resume</li>
        <li>• Practice LeetCode</li>
      </ul>
    </Card>
  );
}
