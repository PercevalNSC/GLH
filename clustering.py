from GLHMongoDB import OPTICSConstruct


eps = 0.0001
min_samples = 4
obj = OPTICSConstruct(min_samples)
obj.set_eps(eps)
print(obj.polygon())
eps = 0.01
obj.set_eps(eps)
print(obj.polygon())
