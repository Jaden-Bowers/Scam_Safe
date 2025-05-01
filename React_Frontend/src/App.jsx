import React, { useState } from "react";
import Header from "./components/Header";
import TempEmailBar from "./components/TempEmailBar";
import AnalysisBox from "./components/AnalysisBox";
import FooterInstructions from "./components/FooterInstructions";

function App() {
  const [analysis, setAnalysis] = useState(
    "Push the reload button to generate an email to forward your suspicious email to."
  );

  return (
    <div className="min-h-screen bg-[#222724] text-white font-jersey text-2xl">
      <Header />
      <main className="max-w-3xl mx-auto px-4 py-8 flex flex-col items-center text-center">
        <h1 className="text-4xl md:text-5xl mb-4">
          Is Your Email a Scam
          <span className="text-[#0054FF]">?</span>
        </h1>
        <p className="mb-8 text-lg md:text-2xl">
          Forward suspicious emails to a temporary address below <br />
          and get instant AI analysis
        </p>

        <TempEmailBar setAnalysis={setAnalysis} />

        <AnalysisBox analysis={analysis} />

        <FooterInstructions />
      </main>
    </div>
  );
}

export default App;
