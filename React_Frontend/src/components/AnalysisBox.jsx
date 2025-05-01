// Analysis box. updates from setAnalysis function

import React from "react";
import Typewriter from "./Typewriter";

function AnalysisBox({ analysis }) {
  return (
    <div className="mb-8 w-full">
      <p className="text-xl sm:text-2xl mb-2">Analysis:</p>
      <div className="bg-[#303633] p-4 rounded-lg whitespace-pre-line min-h-[100px]">
        {analysis ? <Typewriter text={analysis} delay={8} /> : "Waiting for email analysis..."}
      </div>
    </div>
  );
}

export default AnalysisBox;