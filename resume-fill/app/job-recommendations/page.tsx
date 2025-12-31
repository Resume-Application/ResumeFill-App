"use client";

import JobCard from "../components/jobs/JobCard";

export default function JobRecommendationsPage() {
  // Placeholder job data
  const jobs = [
    {
      id: 1,
      title: "Frontend Developer",
      company: "TechCorp Inc.",
      location: "San Francisco, CA",
      description: "Work on modern web applications with React and TypeScript.",
      url: "#",
    },
    {
      id: 2,
      title: "Backend Engineer",
      company: "DataWorks",
      location: "Remote",
      description: "Build scalable APIs and services using Python and FastAPI.",
      url: "#",
    },
    {
      id: 3,
      title: "UI/UX Designer",
      company: "Creative Studio",
      location: "New York, NY",
      description: "Design engaging and accessible user interfaces for web apps.",
      url: "#",
    },
  ];

  return (
    <div className="min-h-screen bg-stone-100 text-black p-6">
      <h1 className="text-3xl font-bold mb-6">Job Recommendations</h1>

      <div className="gap-6">
        {jobs.map((job) => (
          <JobCard key={job.id} job={job} className="flex flex-col gap-10 border-b border-gray-200"/>
        ))}
      </div>
    </div>
  );
}
