from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ, BasicAer
import math
import fuzzy_partitions as fp
from qiskit.visualization import plot_histogram

Qregisters = []

def generate_circuit(fuzzy_partitions):
    '''Function generating a quantum circuit with width required by QFS '''
    qc = QuantumCircuit()
    for partition in fuzzy_partitions:
        #print(partition.len_partition(), partition.name)
        qc.add_register(QuantumRegister(math.ceil(math.log(partition.len_partition()+1, 2)), name=partition.name))
        Qregisters.append(QuantumRegister(math.ceil(math.log(partition.len_partition()+1, 2)), name=partition.name))


    return qc

def output_register(qc, output_partition):
    qc.add_register(QuantumRegister(output_partition.len_partition(), name=output_partition.name))
    Qregisters.append(QuantumRegister(output_partition.len_partition(), name=output_partition.name))
    return qc

def select_qreg_by_name(qc, name):
    '''Function returning the quantum register in QC selected by name'''
    for qr in qc.qregs:
        if name == qr.name:
            break
    return qr


def negation_0(qc, qr, bit_string):
    '''Function which insert a NOT gate if the bit in the rule is 0'''
    for index in range(len(bit_string)):
        if bit_string[index]=='0':
            qc.x(qr[index])



def convert_rule(qc, fuzzy_rule, partitions, output_partition):
    '''Function which convert a fuzzy rule in the equivalent quantum circuit.
    You can use multiple times convert_rule to concatenate the quantum circuits related to different
    rules.'''
    all_partition = partitions.copy()
    all_partition.append(output_partition)
    #print(output_partition)
    #print(partitions)
    #print(all_partition)
    rule = fp.fuzzy_rules().add_rules(fuzzy_rule,all_partition)
    controls = []
    targs = []
    #print(fuzzy_rule)
    #print(rule)
    for index in range(len(rule)):
        if rule[index] == 'and' or rule[index] == 'then':
            qr = select_qreg_by_name(qc, rule[index-2])
            negation_0(qc, qr, rule[index-1])
            #qc.x(qr[-1])
            for i in range(select_qreg_by_name(qc, rule[index - 2]).size-1):
                #print(select_qreg_by_name(qc, rule[index-2])[i])
                controls.append(select_qreg_by_name(qc, rule[index-2])[i])
            controls.append(qr[-1])
        if rule[index] == 'then':
            #print(rule[index])
            #print(rule[index+2])
            #print('converted', int(rule[index+2],2))
            targs.append(select_qreg_by_name(qc, output_partition)[int(rule[index+2][::-1],2)])
            #print(targs)

    #print(controls, targs)
    #scratch = select_qreg_by_name(qc, 'scratch')
    qc.mcx(controls, targs[0] )
    for index in range(len(rule)):
        if rule[index] == 'and' or rule[index] == 'then':
            qr = select_qreg_by_name(qc, rule[index-2])
            negation_0(qc, qr, rule[index-1])
            #qc.x(qr[-1])



'''
#_______________________________________________________________________________
#                               DEFINE PARTITIONS
#________________________________________________________________________________


p1 = fp.fuzzy_partition(name='temp', sets=['VC','H','C','VH'])
p2 = fp.fuzzy_partition(name='umi', sets=['VL','H','L','VH'])
p3 = fp.fuzzy_partition(name='temp_out', sets=['VC','H','C'])

#_______________________________________________________________________________
#                           INITIALIZE QUANTUM CIRCUIT FOR QFS
#_______________________________________________________________________________

qc = generate_circuit([p1,p2])
qc = output_register(qc, p3)
initial_state_temp = [math.sqrt(0.45),math.sqrt(0.50), math.sqrt(0.00), math.sqrt(0)]
while len(initial_state_temp)!=2**Qregisters[0].size:
    initial_state_temp.append(0)
initial_state_temp[-1] = math.sqrt(1 - 0.95)
initial_state_umi = [math.sqrt(0.20),math.sqrt(0.60), math.sqrt(0.10), math.sqrt(0)]
while len(initial_state_umi)!=2**Qregisters[1].size:
    initial_state_umi.append(0)
initial_state_umi[-1] = math.sqrt(1 - 0.90)
qc.initialize(initial_state_temp, Qregisters[0])
qc.initialize(initial_state_umi, Qregisters[1])
#qc.u3(1.9823, 0, math.pi/2, qubit=QFS[1][0])
#qc.u3(1.9823, 0, math.pi/2, qubit=QFS[1][1])
#qc.h(qubit=Qregisters[2])

#_______________________________________________________________________________
#                               DEFINE FUZZY RULES
#_______________________________________________________________________________


convert_rule(qc=qc, fuzzy_rule='if temp is VH and umi is H then temp_out is C', partitions=[p1,p2], output_partition=p3)
#convert_rule(qc=qc, fuzzy_rule='if temp is VH and umi is VH then temp_out is VC', partitions=[p1,p2,p3])
#convert_rule(qc=qc, fuzzy_rule='if temp is C and umi is L then temp_out is H', partitions=[p1,p2,p3])
#convert_rule(qc=qc, fuzzy_rule='if temp is VC and umi is VL then temp_out is H', partitions=[p1,p2,p3])

#_______________________________________________________________________________
#                                    EXECUTE QFS
#_______________________________________________________________________________
qc.draw('mpl').show()
backend = BasicAer.get_backend('statevector_simulator')
job = execute(qc, backend)
result = job.result()
plot_histogram(job.result().get_counts(), color='midnightblue', title="New Histogram", figsize=(7, 10)).show()

outputstate = result.get_statevector(qc, decimals=3)
total_prob = 0
for i, amp in enumerate(outputstate):
    if abs(amp) > 0.000001:
        prob = abs(amp) * abs(amp)
        total_prob += prob
        print("{:6b}".format(i), round(prob * 100, 5))
print('Total probability: {}%'.format(int(round(total_prob * 100))))
'''

