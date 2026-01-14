import Card from "./Card";

export default function PreferencesSettings() {
  return (
    <Card title="Application Preferences">
      <div className="space-y-4 text-gray-700">
        <div>
          <label className="block mb-1 font-medium">Default Dashboard View</label>
          <select className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Dashboard</option>
            <option>Applications</option>
            <option>Profile</option>
          </select>
        </div>

        <div>
          <label className="block mb-1 font-medium">Preferred Job Type</label>
          <select className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Full-Time</option>
            <option>Part-Time</option>
            <option>Internship</option>
          </select>
        </div>
      </div>
    </Card>
  );
}
