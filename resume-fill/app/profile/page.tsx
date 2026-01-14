"use client";

import ProfileInfo from "../components/profile/ProfileInfo";
import ProfileStats from "../components/profile/ProfileStats";

export default function Profile() {
  return (
    <div className="min-h-screen bg-stone-100 text-black px-10 py-10">
      <div className="max-w-5xl mx-auto space-y-10">
        <h1 className="text-4xl font-bold">My Profile</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Profile Info */}
          <ProfileInfo />

          {/* Stats / Activity */}
          <div className="md:col-span-2">
            <ProfileStats />
          </div>
        </div>
      </div>
    </div>
  );
}
