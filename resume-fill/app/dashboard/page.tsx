"use client";
import ApplicationTracker from "../components/dashboard/ApplicationTracker";
import DailyGoals from "../components/dashboard/DailyGoals";
import Recommendations from "../components/dashboard/Recommendations";
import JobMatches from "../components/dashboard/JobMatches";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-stone-100 text-black px-10 py-10">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 font-mono">
          Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

          {/* Application Tracker */}
          <div className="col-span-1 xl:col-span-2">
            <ApplicationTracker />
          </div>

          {/* Daily Goals */}
          <DailyGoals />

          {/* Recommendations */}
          <Recommendations />

          {/* Job Matches */}
          <div className="col-span-1 xl:col-span-2">
            <JobMatches />
          </div>

        </div>
      </div>
    </div>
  );
}
