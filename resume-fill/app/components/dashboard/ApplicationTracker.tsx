import Card from "./Card";

export default function ApplicationTracker() {
  return (
    <Card title="Application Tracker">
      <div className="space-y-3">
        <div className="flex justify-between text-sm text-gray-700">
          <span>Applications Sent</span>
          <span className="font-semibold">12</span>
        </div>

        <div className="flex justify-between text-sm text-gray-700">
          <span>Interviews</span>
          <span className="font-semibold">3</span>
        </div>

        <div className="flex justify-between text-sm text-gray-700">
          <span>Pending Responses</span>
          <span className="font-semibold">5</span>
        </div>
      </div>
    </Card>
  );
}
