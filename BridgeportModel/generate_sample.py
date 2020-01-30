import numpy as np

def generate_from_multinormial(dist, size):
    #np.random.seed(seed=0)
    samples = np.random.sample(size)
    #print samples
    num = len(dist)
    
    result = np.zeros((size, num))

    for i, s in enumerate(samples):
        for j, p in enumerate(dist):
            if s < p:
                result[i][j] = 1
                break
    return result

def generate_from_Gaussian(mu, sigma, size):
    pass

def write_sample(data, dist):
    output_fp = "sample.csv"
    labels = []
    for k in dist:
        if len(dist[k]) == 1:
            labels.append(k)
        else:
            labels.extend(["%s_%d" % (k, i) for i in range(len(dist[k]))])
    labels.append('evac')
    #np.savetxt(output_fp, data, fmt='%d', delimiter=",", header=','.join(labels))
    np.savetxt(output_fp, data, fmt='%s', delimiter=",", header=','.join(labels))