import Card from "./Card";

export default function ProfileStats() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card title="Applications Sent">
        <p className="text-3xl font-bold">12</p>
        <p className="text-gray-600 text-sm">Total applications sent this month</p>
      </Card>

      <Card title="Interviews Scheduled">
        <p className="text-3xl font-bold">3</p>
        <p className="text-gray-600 text-sm">Interviews scheduled this month</p>
      </Card>

      <Card title="Pending Tasks">
        <p className="text-3xl font-bold">5</p>
        <p className="text-gray-600 text-sm">Tasks pending completion</p>
      </Card>

      <Card title="Profile Completeness">
        <p className="text-3xl font-bold">80%</p>
        <p className="text-gray-600 text-sm">Complete your profile to get better matches</p>
      </Card>
    </div>
  );
}
