import Card from "./Card";

export default function JobMatches() {
  return (
    <Card title="Potential Job Matches">
      <div className="space-y-3 text-sm">
        <div className="bg-gray-100 p-4 rounded-xl border border-gray-200">
          <p className="font-semibold text-black">Frontend Developer</p>
          <p className="text-gray-600">Company XYZ</p>
        </div>

        <div className="bg-gray-100 p-4 rounded-xl border border-gray-200">
          <p className="font-semibold text-black">Software Engineer Intern</p>
          <p className="text-gray-600">Tech Corp</p>
        </div>

        <div className="bg-gray-100 p-4 rounded-xl border border-gray-200">
          <p className="font-semibold text-black">Full Stack Developer</p>
          <p className="text-gray-600">Startup Labs</p>
        </div>
      </div>
    </Card>
  );
}
