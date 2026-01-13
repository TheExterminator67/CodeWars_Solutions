def regex_divisible_by(n):
    if n == 1:
        return "^[01]+$"
    
    
    states = n
    matrix = [["" for _ in range(states)] for _ in range(states)]
    
    for i in range(states):
        matrix[i][(i * 2) % states] = self_add(matrix[i][(i * 2) % states], "0")
        matrix[i][(i * 2 + 1) % states] = self_add(matrix[i][(i * 2 + 1) % states], "1")

   
    for k in range(states - 1, 0, -1):
       
        for i in range(k):
            for j in range(k):
                
                r_ik = matrix[i][k]
                r_kk = matrix[k][k]
                r_kj = matrix[k][j]
                r_ij = matrix[i][j]
                
                if r_ik and r_kj:
                    inner = f"{parenthesize(r_kk)}*" if r_kk else ""
                    path_thru_k = f"{parenthesize(r_ik)}{inner}{parenthesize(r_kj)}"
                    matrix[i][j] = self_add(r_ij, path_thru_k)

    
    res = f"^({matrix[0][0]})+$"
    return res

def self_add(current, new):
    if not current: return new
    if not new: return current
    return f"{current}|{new}"

def parenthesize(r):
    if len(r) <= 1: return r
    return f"(?:{r})"