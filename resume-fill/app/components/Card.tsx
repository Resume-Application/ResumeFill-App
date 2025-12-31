export default function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition">
      <h2 className="text-xl font-semibold mb-4 text-black">{title}</h2>
      {children}
    </div>
  );
}
