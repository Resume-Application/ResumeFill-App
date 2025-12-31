interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  url: string;
}

interface JobCardProps {
  job: Job;
  className?: string; // optional className prop
}

export default function JobCard({ job, className = "" }: JobCardProps) {
  return (
    <div
      className={`w-full py-4 flex justify-between items-start hover:bg-white border-r transition p-4 ${className}`}
    >
      {/* Job info */}
      <div className="space-y-1">
        <h2 className="text-xl font-semibold">{job.title}</h2>
        <p className="text-gray-600">
          {job.company} • {job.location}
        </p>
        <p className="text-gray-700">{job.description}</p>
      </div>

      {/* Apply button */}
      <div className="ml-4 flex-shrink-0">
        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 bg-white text-black rounded-lg hover:bg-stone-400 transition"
        >
          Apply
        </a>
      </div>
    </div>
  );
}
