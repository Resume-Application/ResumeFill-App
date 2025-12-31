"use client";

import AccountSettings from "../components/settings/AccountSettings";
import NotificationSettings from "../components/settings/NotificationSettings";
import PreferencesSettings from "../components/settings/PreferencesSettings";

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-gray-50 text-black px-10 py-10">
      <div className="max-w-5xl mx-auto space-y-10">
        <h1 className="text-4xl font-bold">Settings</h1>

        <div className="grid grid-cols-1 gap-6">
          <AccountSettings />
          <NotificationSettings />
          <PreferencesSettings />
        </div>
      </div>
    </div>
  );
}
