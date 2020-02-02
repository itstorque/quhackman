"""
    Simulation file for Qu[H]ack[Wo]man
"""

from qiskit import QuantumCircuit, Aer, execute, QuantumRegister, ClassicalRegister
import numpy as np

def real_map(value, leftMin, leftMax, rightMin, rightMax):


    # Maps one range to another
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class QuantumSimulation():

    def __init__(self):

        self.gates1 = []
        self.gates2 = []
        self.qc = QuantumCircuit(2, 2)
        self.qc.h(0)
        self.qc.cx(0,1)
        self.output = []
        self.shots_num = 1
        self.result = None
        self.rng_n_qubits = 2

    def load_gates(self):

        count1 = 0

        for i in range(len(self.gates1)):
            if self.gates1[i] == 'T':
                self.qc.rx(np.pi/4,0)
                count1 += 1
            elif self.gates1[i] == 'S':
                self.qc.rx(np.pi/2,0)
                count1 += 1
            elif self.gates1[i] == 'Z':
                self.qc.x(0)
                count1 += 1

        count2 = 0

        for i in range(len(self.gates2)):
            if self.gates2[i] == 'T':
                self.qc.rx(np.pi/4,1)
                count2 += 1
            elif self.gates2[i] == 'S':
                self.qc.rx(np.pi/2,1)
                count2 += 1
            elif self.gates2[i] == 'Z':
                self.qc.x(1)
                count2 += 1

        # add the identity
        if count2 < count1:
            for i in range(count1-count2):
                self.qc.iden(1)
        elif count2 > count1:
            for i in range(count2-count1):
                self.qc.iden(0)


    def add_gate(self, player, gate):

        if str(player) == "1":
            self.gates1.append(gate.upper())
        elif str(player) == "2":
            self.gates2.append(gate.upper())

    def run(self):
        simulator = Aer.get_backend('qasm_simulator')
        self.qc.measure([0,1],[1,0])
        # Execute the circuit on the qasm simulator
        job = execute(self.qc, simulator, shots=self.shots_num)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(self.qc)
        print("\nTotal count for 00 and 11 are:",counts)
        self.output = counts

    def measure(self, ra, rb, player_number):

        self.qc = QuantumCircuit(2, 1)

        self.qc.h(0)
        self.qc.cx(0,1)

        self.qc.rx(ra,0)
        self.qc.rx(rb,0)
        self.qc.measure([player_number-1],[0])

        job = execute(self.qc, simulator, shots=1)
        result = job.result()

        counts = result.get_counts(self.qc)
        counts.setdefault('0', 0)
        counts.setdefault('1', 0)

        zero_counts = counts['0']
        one_counts = counts['1']

        self.did_win = (player_number, zero_counts > one_counts)


    def random_num_generator(self,lower_bound,higher_bound):
        q = QuantumRegister(self.rng_n_qubits, 'q')
        circ = QuantumCircuit(q)
        c0 = ClassicalRegister(2, 'c0')
        circ.add_register(c0)

        for i in range(self.rng_n_qubits):
            circ.h(q[i])

        for i in range(self.rng_n_qubits):
            circ.measure(q[i], c0)

        backend = Aer.get_backend('statevector_simulator')
        job = execute(circ, backend)

        result = job.result()
        output = result.get_statevector(circ, decimals=5)

        n1 = 0
        n2 = 0
        n3 = 0
        for i in range( output.size ):
            if abs(output[i]) != 0:
                n1 = i
                n2 = np.real(output[i])
                n3 = np.imag(output[i])

        y = real_map(n1+n2+n3, -self.rng_n_qubits, len(output)-1+self.rng_n_qubits, \
             lower_bound, higher_bound)

        return y
