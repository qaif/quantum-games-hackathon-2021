from qiskit import QuantumCircuit, QuantumRegister
import numpy as np

qubits_number = 1
def quantum_computer(self):
    qr = QuantumRegister(qubits_number, 'Qubits')
    qc = QuantumCircuit(qr)

    if event.type == pygame.KEYDOWN:
        if event.key == pyagme.H and game_active:
            qc.h(0)
            #now we have to split the bird
        if event.key == pygame.X and game_active:
            qc.x(0)
        if event.key == pygame.Z and game_active:
            qc.z(0)
        if event.key == pygame.R and game_active:
            qc.rx(0)
