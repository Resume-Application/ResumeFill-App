import Card from "./Card";

export default function ProfileInfo() {
  return (
    <Card title="Profile Information">
      <div className="flex flex-col items-center space-y-4">
        <div className="w-32 h-32 rounded-full overflow-hidden border border-gray-200">
          <img 
            src="/profile-placeholder.png" 
            alt="Profile Picture" 
            className="w-full h-full object-cover" 
          />
        </div>

        <div className="text-center space-y-1">
          <p className="text-lg font-semibold">Archit Bhatt</p>
          <p className="text-gray-600 text-sm">architbhatt@gmail.com</p>
          <p className="text-gray-600 text-sm">Software Engineer</p>
        </div>

        <button className="mt-3 px-4 py-2 bg-white  text-black rounded-lg hover:bg-stone-100 transition">
          Edit Profile
        </button>
      </div>
    </Card>
  );
}
