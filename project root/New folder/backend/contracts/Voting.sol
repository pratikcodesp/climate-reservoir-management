// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Voting {
    address public admin;
    bool public votingOpen;
    
    struct Candidate {
        string name;
        uint voteCount;
    }
    
    Candidate[] public candidates;
    mapping(address => bool) public hasVoted;

    event Voted(address indexed voter, uint candidateId);

    constructor(string[] memory _candidateNames) {
        admin = msg.sender;
        votingOpen = true;
        
        for(uint i = 0; i < _candidateNames.length; i++) {
            candidates.push(Candidate({
                name: _candidateNames[i],
                voteCount: 0
            }));
        }
    }

    function vote(uint _candidateId) external {
        require(votingOpen, "Voting closed");
        require(!hasVoted[msg.sender], "Already voted");
        require(_candidateId < candidates.length, "Invalid candidate");
        
        candidates[_candidateId].voteCount++;
        hasVoted[msg.sender] = true;
        
        emit Voted(msg.sender, _candidateId);
    }

    function endVoting() external {
        require(msg.sender == admin, "Only admin");
        votingOpen = false;
    }
}