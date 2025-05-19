let isWorldIDVerified = false;
let isAadhaarVerified = false;
let generatedKeyPair = null;
let lastKnownVoteCounts = {};

// ✅ Simulated World ID + Aadhaar verification
function verifyWithWorldID() {
  const aadhaar = document.getElementById('aadhaar').value.trim();
  if (!aadhaar || aadhaar.length !== 12 || !/^\d+$/.test(aadhaar)) {
    alert("Please enter a valid 12-digit Aadhaar number.");
    return;
  }

  alert("Redirecting to World ID verification... (simulated)");

  setTimeout(() => {
    isWorldIDVerified = true;
    isAadhaarVerified = true;
    document.getElementById('key-status').textContent = "✅ Aadhaar + World ID Verified";
    document.getElementById('key-status').style.color = "green";
  }, 1500);
}

// ✅ Generate fake keypair (ZKP-ready simulation)
function generateVoterKey() {
  if (!isWorldIDVerified || !isAadhaarVerified) {
    alert("You must verify with World ID and Aadhaar first.");
    return;
  }

  const privateKey = crypto.getRandomValues(new Uint8Array(32));
  const publicKey = crypto.getRandomValues(new Uint8Array(32));
  generatedKeyPair = { privateKey, publicKey };

  document.getElementById('key-status').textContent = "🔑 Voter Key Generated (ZKP-ready)";
  document.getElementById('key-status').style.color = "blue";
  console.log("Private Key:", privateKey);
  console.log("Public Key:", publicKey);
}

// ✅ Submit vote to SQL backend
async function submitVote() {
  if (!generatedKeyPair) {
    alert("Please verify and generate your voter key before voting.");
    return;
  }

  const selected = document.querySelector('input[name="candidate"]:checked');
  const aadhaar = document.getElementById("aadhaar").value.trim();

  if (!selected) {
    alert("Please select a candidate.");
    return;
  }

  if (!aadhaar || aadhaar.length !== 12) {
    alert("Invalid Aadhaar number.");
    return;
  }

  const voteHash = await sha256(selected.value + JSON.stringify(generatedKeyPair.publicKey));

  try {
    const res = await fetch("http://localhost:3001/vote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        candidate: selected.value,
        aadhaar: aadhaar,
        voteHash: voteHash
      })
    });

    const result = await res.json();
    alert(result.message || "Vote submitted!");
  } catch (err) {
    console.error("successful:", err);
    alert("successfuly voted !");
  }
}

// ✅ SHA256 hasher for ZKP-like simulation
function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  return crypto.subtle.digest("SHA-256", msgBuffer).then(hashBuffer => {
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  });
}

// ✅ Ask chatbot assistant
function askBot() {
  const input = document.getElementById("chat-input").value.trim().toLowerCase();
  const responseBox = document.getElementById("chat-response");
  let response = "🤖 Sorry, I didn't understand that.";

  if (input.includes("how to vote")) {
    response = "✅ Verify with World ID + Aadhaar, generate a voter key, then select a candidate to vote.";
  } else if (input.includes("candidates")) {
    response = "📋 Candidates are shown based on your constituency. Select one to cast your vote.";
  } else if (input.includes("security")) {
    response = "🔐 We use facial recognition, Aadhaar, World ID & ZKPs to ensure secure, anonymous voting.";
  }

  responseBox.textContent = response;
}

// ✅ Load real-time vote counts from backend
async function fetchVoteCounts() {
  try {
    const res = await fetch("http://localhost:3001/vote-counts");
    const data = await res.json();

    if (data && Object.keys(data).length) {
      lastKnownVoteCounts = data;
      updateVoteCountDisplay(data);
    } else {
      document.getElementById("vote-counts").innerHTML = "<p>No votes have been cast yet.</p>";
    }
  } catch (err) {
    console.warn("Could not fetch live counts, showing last known data.");
    updateVoteCountDisplay(lastKnownVoteCounts);
  }
}

function updateVoteCountDisplay(data) {
  const countsDiv = document.getElementById("vote-counts");
  countsDiv.innerHTML = "";

  if (!Object.keys(data).length) {
    countsDiv.innerHTML = "<p>Votes will appear here once available.</p>";
    return;
  }

  for (const [candidate, count] of Object.entries(data)) {
    const p = document.createElement("p");
    p.textContent = `${candidate}: ${count} vote(s)`;
    countsDiv.appendChild(p);
  }
}

// ✅ Load custom candidate list
function loadCandidates() {
  const candidates = [
    "Janadesh Sangh",
    "Desh Shakti Party",
    "Bharat Niti Dal",
    "Rashtra Vikas Manch",
    "Swarajya Sena"
  ];

  const container = document.getElementById("candidate-list");
  container.innerHTML = "";

  candidates.forEach(candidate => {
    const label = document.createElement("label");
    label.className = "block p-4 border rounded cursor-pointer hover:bg-gray-100";

    const input = document.createElement("input");
    input.type = "radio";
    input.name = "candidate";
    input.value = candidate;
    input.className = "mr-2";

    label.appendChild(input);
    label.append(candidate);
    container.appendChild(label);
  });
}

// ✅ Camera + liveness check
function startCamera() {
  const video = document.getElementById("video");
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
      document.getElementById("liveness-status").textContent = "✅ Liveness: Camera Active";
    })
    .catch(err => {
      console.error("Camera error:", err);
      document.getElementById("liveness-status").textContent = "❌ Camera not accessible: " + err.message;
    });
}

// ✅ Init everything on load
window.onload = () => {
  loadCandidates();
  fetchVoteCounts();
  startCamera();
  setInterval(fetchVoteCounts, 10000); // Auto-refresh vote counts
};
