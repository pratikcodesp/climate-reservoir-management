async function main() {
  const candidateNames = ["Alice", "Bob", "Charlie"];
  
  const Voting = await ethers.getContractFactory("Voting");
  const voting = await Voting.deploy(candidateNames);
  
  console.log(`
  🎉 Voting System Deployed!
  Address: ${voting.address}
  Admin: ${await voting.admin()}
  Candidates: ${candidateNames.join(", ")}
  `);
}