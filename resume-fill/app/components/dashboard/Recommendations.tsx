import Card from "./Card";

export default function Recommendations() {
  return (
    <Card title="Recommendations">
      <p className="text-sm text-gray-700">
        Based on your progress, here’s what you should focus on next:
      </p>

      <div className="mt-4 space-y-2 text-sm text-gray-800">
        <p>- Add measurable achievements to resume</p>
        <p>- Tailor resume per application</p>
        <p>- Strengthen LinkedIn profile</p>
      </div>
    </Card>
  );
}
