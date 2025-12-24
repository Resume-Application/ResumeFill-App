import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white">
      <section className="w-full flex flex-col md:flex-row items-center justify-between px-10 py-24 max-w-7xl mx-auto">
        <div className="flex-1">
          <h1 className="text-5xl md:text-6xl font-bold leading-tight">
            Track. Apply. <span className="text-indigo-500">Win.</span>
          </h1>

          <p className="mt-6 text-gray-400 text-lg max-w-xl">
            A smart platform that helps you manage applications, autofill forms,
            discover new opportunities, and gamify your job hunt.
          </p>

          <div className="flex gap-4 mt-8">
            <button className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 transition-all rounded-lg uppercase font-semibold tracking-wide">
              Get Started
            </button>
            <button className="px-6 py-3 border border-gray-600 hover:border-white transition-all rounded-lg uppercase font-semibold tracking-wide">
              Learn More
            </button>
          </div>
        </div>

        <div className="flex-1 mt-12 md:mt-0 flex justify-center">
          <div className="w-[420px] h-[420px] bg-gradient-to-br from-indigo-600 to-purple-800 rounded-2xl shadow-2xl flex items-center justify-center">
            <span className="text-2xl font-semibold opacity-80">
              Landing Visual
            </span>
          </div>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-10 pb-24">
        <h2 className="text-3xl font-bold mb-10">Why use this platform?</h2>

        <div className="grid gap-8 md:grid-cols-3">
          <div className="bg-zinc-900 border border-gray-800 p-6 rounded-xl hover:-translate-y-1 transition-all">
            <h3 className="text-xl font-semibold mb-3">Autofill Applications</h3>
            <p className="text-gray-400">
              Save time with intelligent form filling powered by your stored resume.
            </p>
          </div>

          <div className="bg-zinc-900 border border-gray-800 p-6 rounded-xl hover:-translate-y-1 transition-all">
            <h3 className="text-xl font-semibold mb-3">Track Everything</h3>
            <p className="text-gray-400">
              Keep every application organized with progress tracking and reminders.
            </p>
          </div>

          <div className="bg-zinc-900 border border-gray-800 p-6 rounded-xl hover:-translate-y-1 transition-all">
            <h3 className="text-xl font-semibold mb-3">Smart Suggestions</h3>
            <p className="text-gray-400">
              Discover tailored opportunities based on your interests & goals.
            </p>
          </div>
        </div>
      </section>


      <footer className="border-t border-gray-800 py-6 text-center text-gray-500">
        © 2025 — Built for ambitious job hunters 🚀
      </footer>
    </div>
  );
}
