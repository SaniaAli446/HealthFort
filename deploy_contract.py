from brownie import Contract, accounts, project
from solcx import compile_source

# Solidity Smart Contract Code
contract_source_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Healthcare {
    struct Report {
        string patientName;
        string diagnosis;
        string treatment;
        uint256 timestamp;
    }

    address public owner;
    mapping(uint256 => Report) public reports;
    uint256 public reportCount;

    event ReportAdded(uint256 reportId, string patientName);

    constructor() {
        owner = msg.sender;
        reportCount = 0;
    }

    function addReport(string memory _patientName, string memory _diagnosis, string memory _treatment) public returns (uint256) {
        reports[reportCount] = Report(_patientName, _diagnosis, _treatment, block.timestamp);
        emit ReportAdded(reportCount, _patientName);
        reportCount++;
        return reportCount - 1;
    }

    function getReport(uint256 reportId) public view returns (string memory, string memory, string memory, uint256) {
        Report memory report = reports[reportId];
        return (report.patientName, report.diagnosis, report.treatment, report.timestamp);
    }
}
"""

def deploy_contract():
    """Compiles and deploys the Healthcare smart contract"""
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol["<stdin>:Healthcare"]

    # Deploy contract
    account = accounts.load("my_account")  # Load your Ethereum account
    healthcare_contract = project.Contract.from_abi(
        "Healthcare", account.deploy(contract_interface), contract_interface["abi"]
    )
    
    print(f"Contract deployed at: {healthcare_contract.address}")
    return healthcare_contract

def add_report(healthcare_contract, patient_name, diagnosis, treatment):
    """Adds a medical report to the blockchain"""
    account = accounts.load("my_account")
    tx = healthcare_contract.addReport(patient_name, diagnosis, treatment, {"from": account})
    tx.wait(1)
    print(f"Report added with ID: {tx.events['ReportAdded']['reportId']}")

def get_report(healthcare_contract, report_id):
    """Retrieves a medical report from the blockchain"""
    report = healthcare_contract.getReport(report_id)
    print(f"Patient: {report[0]}, Diagnosis: {report[1]}, Treatment: {report[2]}, Timestamp: {report[3]}")

def main():
    healthcare_contract = deploy_contract()
    add_report(healthcare_contract, "Alice", "Flu", "Rest & Hydration")
    get_report(healthcare_contract, 0)
