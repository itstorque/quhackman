"""
    Simulation file for Qu[H]ackMan
"""

from qiskit import QuantumCircuit, Aer, execute

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
