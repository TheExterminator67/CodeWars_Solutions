from itertools import permutations

def solve_puzzle(clues):
    size = 7
    top, right = clues[0:7], clues[7:14]
    bottom, left = clues[14:21][::-1], clues[21:28][::-1]

    def get_vis(p):
        v, m = 0, 0
        for x in p:
            if x > m: v += 1; m = x
        return v

    all_p = list(permutations(range(1, 8)))
    perms_by_clue = {}
    for p in all_p:
        v1, v2 = get_vis(p), get_vis(p[::-1])
        for c1 in [v1, 0]:
            for c2 in [v2, 0]:
                perms_by_clue.setdefault((c1, c2), []).append(p)


    r_perms = [perms_by_clue[(left[i], right[i])] for i in range(7)]
    c_perms = [perms_by_clue[(top[i], bottom[i])] for i in range(7)]

    changed = True
    while changed:
        changed = False
        for r in range(7):
            for c in range(7):
                allowed_by_cols = {p[r] for p in c_perms[c]}
                original_len = len(r_perms[r])
                r_perms[r] = [p for p in r_perms[r] if p[c] in allowed_by_cols]
                if len(r_perms[r]) < original_len: changed = True
            
        for c in range(7):
            for r in range(7):
                allowed_by_rows = {p[c] for p in r_perms[r]}
                original_len = len(c_perms[c])
                c_perms[c] = [p for p in c_perms[c] if p[r] in allowed_by_rows]
                if len(c_perms[c]) < original_len: changed = True

    solve_order = sorted(range(7), key=lambda r: len(r_perms[r]))
    
    grid = [None] * 7
    col_masks = [0] * 7

    def backtrack(order_idx):
        if order_idx == 7:
            for c in range(7):
                col = [grid[i][c] for i in range(7)]
                if top[c] and get_vis(col) != top[c]: return False
                if bottom[c] and get_vis(col[::-1]) != bottom[c]: return False
            return True

        r = solve_order[order_idx]
        for p in r_perms[r]:
            conflict = False
            for c in range(7):
                if col_masks[c] & (1 << p[c]):
                    conflict = True
                    break
            if conflict: continue

            grid[r] = p
            for c in range(7): col_masks[c] |= (1 << p[c])
            if backtrack(order_idx + 1): return True
            for c in range(7): col_masks[c] &= ~(1 << p[c])
            
        return False

    backtrack(0)
    return [list(row) for row in grid]