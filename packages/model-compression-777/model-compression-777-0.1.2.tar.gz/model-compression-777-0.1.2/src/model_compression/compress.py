class compress:
    def load_pruned(path):
        """
        load a pruned pytorch state file by applying weight mask.
        returns a dict where the keys are the array names (e.g. encoder.0.2.bias)
        """
        raw = torch.load(path, map_location=torch.device('cpu'))
        if 'model' in raw: raw = raw['model']
        if 'state' in raw: raw = raw['state']
        weights = {}
        for name, vec in raw.items():
            if name.find("_orig") > -1:
                mask = raw[name[:-4] + "mask"]
                weights[name[:-5]] = vec * mask
            elif name.find("_mask") == -1:
                weights[name] = vec
        return weights
    
    def load_unpruned(path):
        raw = torch.load(path + "/best.th", map_location=torch.device('cpu'))
        if 'model' in raw: raw = raw['model']
        if 'state' in raw: raw = raw["state"]
        return raw
    
    def to_relative_csr(m, index_bits):
        """
        converts m into the column-relative CSR format.
        m must be a 1D or 2D NUMPY array; use .numpy() on pytorch tensors first.
        index_bits is the bit width of relative column spacing; try around 2~8.
        returns (nonzero values (v), column offsets (c), row indices (r)).
        """
        max_spacing = 2 ** index_bits # will be stored unsigned 1-indexed (stored 0 = actual 1)
        v, c, r = [], [], [0]
        if len(m.shape) == 1: m = [m]
    
        for row in m:
            if (len(row.shape) != 1):
                print("*** abnormal row shape ***")
            nz = np.nonzero(row)[0]
            if (len(nz) == 0):
                pass
                # row of zeros; row start/end indices are equal
            else:
                nz = nz.flatten()
                prev_idx = -1
                for idx in nz:
                    while idx - prev_idx > max_spacing:
                        prev_idx += max_spacing
                        v.append(0)
                        c.append(max_spacing)
                    v.append(row[idx])
                    c.append(idx - prev_idx)
                    prev_idx = idx
            r.append(len(v))
    
        return v, c, r
    
    def from_relative_csr(v, c, r, width):
        """
        utility function that converts CSR format back into normal format.
        the purpose of this function is mostly for testing;
        note that using this for sparse matrix operations can be very inefficient.
        """
        height = len(r) - 1
        m = np.zeros((height, width))
        for i in range(height):
            row = m[i]
            v_, c_ = v[r[i]:r[i + 1]], c[r[i]:r[i + 1]]
            prev_idx = -1
            for j in range(len(c_)):
                idx = prev_idx + c_[j]
                row[idx] = v_[j]
                prev_idx = idx
        return m
    
    def compress(vec, data_bits=4, fc_idx_bits=4, conv_idx_bits=5, def_idx_bits=4, row_bits=32):
        """
        compresses common weights.
        for convolution, when kernel is size 1, it is seen as a fully-connected layer.
        returns a tuple containing compressed format and size of the compressed weight in bytes.
        """
        if (len(vec.shape) == 3): # conv1d weights
            if (vec.shape[2] == 1): # fully connected layer
                vec = vec.squeeze()
                v, c, r = to_relative_csr(vec, fc_idx_bits)
                csr_size = get_csr_size_in_bytes(v, c, r, data_bits, fc_idx_bits, row_bits)
                return (v, c, r), csr_size
            else:
                curr = []
                csr_total = 0
                for channel in vec:
                    channel = channel.transpose()
                    v, c, r = to_relative_csr(channel, conv_idx_bits)
                    curr.append((v, c, r))
                    csr_size = get_csr_size_in_bytes(v, c, r, data_bits, conv_idx_bits, row_bits)
                    csr_total += csr_size
                return curr, csr_total
        elif (len(vec.shape) == 2):
            v, c, r = to_relative_csr(vec, def_idx_bits)
            csr_size = get_csr_size_in_bytes(v, c, r, data_bits, def_idx_bits, row_bits)
            return (v, c, r), csr_size
        else:
            csr_size = len(vec) / 2
            return vec, csr_size
    
    def get_csr_size_in_bytes(v, c, r, v_width, c_width, r_width):
        return int((len(v) * v_width + len(c) * c_width + len(r) * r_width) / 8 + 0.5)
    
    def print_weight_info(weights_normalized):
        """
        prints some info about a weights dict. for each weight matrix, this prints its min,
        max, total number of elements, and sparsity.
        returns global sparsity.
        """
        count_nz, count = 0, 0
        for name, vec in weights_normalized.items():
            print(name, "\t%.4f\t\t%.4f\t\t%d" % (vec.min(), vec.max(), int(vec.flatten().size()[0])))
            if name.find("weight") > -1:
                count_nz += np.count_nonzero(vec)
                count += vec.nelement()
                print("\t\t\t%.4f%%" % (np.count_nonzero(vec) / vec.nelement() * 100))
        print(count_nz / count)
        return 1 - count_nz / count
