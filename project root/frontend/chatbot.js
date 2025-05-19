// chatbot.js

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('chat-input');
    const response = document.getElementById('chat-response');
  
    const responses = {
      "how do i vote": "You can vote after verifying with World ID and Aadhaar. Once verified, select your candidate and click 'Submit Vote'.",
      "who are the candidates": "Candidates are listed after verification based on your constituency.",
      "how is privacy maintained": "Your identity is protected using zero-knowledge proofs and decentralized identity protocols.",
      "can i vote twice": "No. The system only allows one vote per verified individual using Aadhaar and World ID.",
      "what if i don't have world id": "You need a World ID to verify your uniqueness. Please create one through the Worldcoin platform.",
      "what is world id": "World ID is a unique identity solution developed by Worldcoin to ensure individual verification.",
      "what is aadhaar": "Aadhaar is a 12-digit unique identity number issued by the Indian government to residents of India.",
      "how is vote stored": "Votes are stored on a decentralized ledger ensuring transparency and tamper-proofing.",
      "can i change my vote": "No, once your vote is cast and confirmed, it cannot be changed.",
      "is this system secure": "Yes, it uses advanced cryptographic techniques like zero-knowledge proofs and runs on decentralized infrastructure.",
      "how do i get a voter key": "After Aadhaar and World ID verification, you can generate a voter key by clicking 'Generate Voter Key'.",
      "what is a voter key": "A voter key is a private credential that allows you to vote securely and anonymously.",
      "how is liveness checked": "Liveness is checked using your camera to ensure a real person is present, preventing spoofing.",
      "can someone else vote for me": "No, identity is verified using facial recognition and liveness detection, preventing impersonation.",
      "is my vote anonymous": "Yes, we use zero-knowledge proofs so your vote is verifiable but not traceable to your identity.",
      "what if i face issues": "Please contact the election administrator or use the help option in the app for support."
    };
  
    window.askBot = function () {
      const question = input.value.toLowerCase().trim();
      if (question === '') return;
  
      response.textContent = responses[question] || "I'm sorry, I don't have an answer to that yet. Please try another question related to voting or verification.";
      input.value = '';
    };
  
    input.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        askBot();
      }
    });
  });
  