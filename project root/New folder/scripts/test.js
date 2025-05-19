const hre = require("hardhat");

async function main() {
  // 1. Get test accounts
  const [owner, voter1, voter2] = await hre.ethers.getSigners();
  
  // 2. Attach to deployed contract
  const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // REPLACE WITH YOUR ADDRESS
  const Voting = await hre.ethers.getContractAt("Voting", contractAddress);
  
  console.log("Testing with:");
  console.log("- Owner:", owner.address);
  console.log("- Voter 1:", voter1.address);
  console.log("- Voter 2:", voter2.address);

  // 3. Test voting
  console.log("\nVoter 1 voting for Alice (candidate 0)");
  const tx1 = await Voting.connect(voter1).vote(0);
  await tx1.wait(); // Wait for transaction to mine
  console.log("Transaction hash:", tx1.hash);

  console.log("\nVoter 2 voting for Bob (candidate 1)");
  const tx2 = await Voting.connect(voter2).vote(1);
  await tx2.wait();
  console.log("Transaction hash:", tx2.hash);

  // 4. Get results
  console.log("\nFinal Results:");
  console.log("Alice votes:", (await Voting.candidates(0)).votes.toString());
  console.log("Bob votes:", (await Voting.candidates(1)).votes.toString());
  console.log("Voter 1 has voted:", await Voting.hasVoted(voter1.address));
  console.log("Voting ends at:", new Date((await Voting.votingEnd()).toNumber() * 1000));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Test failed:", error);
    process.exit(1);
  });