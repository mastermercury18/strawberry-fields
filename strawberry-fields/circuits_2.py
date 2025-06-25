import strawberryfields as sf
from strawberryfields import ops

# create a 2-mode quantum program
prog = sf.Program(2)

# create a free parameter named 'a'
a = prog.params('a')

# define the program
with prog.context as q:
    ops.Dgate(a ** 2)    | q[0]  # free parameter
    ops.MeasureX         | q[0]  # measure qumode 0, the result is used in the next operation
    ops.Sgate(1 - sf.math.sin(q[0].par)) | q[1]  # measured parameter
    ops.MeasureFock()    | q[1]

# initialize the Fock backend
eng = sf.Engine('fock', backend_options={'cutoff_dim': 5})

# run the program, with the free parameter 'a' bound to the value 0.9
result = eng.run(prog, args={'a': 0.9})

prog2 = prog.compile(compiler = "gbs") # compiles circuit into canonical gaussian boson sampling form 

eng = sf.RemoteEngine("X8")  
device = eng.device_spec
prog2 = prog.compile(device=device) # run on X-series chip remote engine on Xanadu Cloud platform with default compiler

prog2 = prog.compile(device=device, compiler = 'Xunitary') # run on Xunitary compiler 


