const hre = require("hardhat");

async function main() {
  const VotingSystem = await hre.ethers.getContractFactory("VotingSystem");
  const votingSystem = await VotingSystem.deploy(2); // 2 hours voting duration
  await votingSystem.deployed();

  console.log(`VotingSystem contract deployed at: ${votingSystem.address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
