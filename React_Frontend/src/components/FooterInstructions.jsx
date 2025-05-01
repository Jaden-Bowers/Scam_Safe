// instructions below the analysis box

import React from "react";

function FooterInstructions() {
  return (
    <div className="text-center mt-8">
      <p className="text-xl sm:text-2xl font-semibold mb-2">How it works:</p>
      <ol className="list-decimal list-inside space-y-2 text-base sm:text-lg">
        <li>Generate a temporary email address</li>
        <li>Forward suspicious emails to this address</li>
        <li>Get instant AI analysis of the email content</li>
      </ol>
    </div>
  );
}

export default FooterInstructions;
