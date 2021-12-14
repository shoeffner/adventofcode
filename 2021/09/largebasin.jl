lines = readlines()
grid = transpose(reshape(parse.(Int, convert.(String, vcat(split.(hcat(lines), "")...))), (:, length(lines))))

# padding
grid = hcat(fill(9, size(grid)[1], 1), grid)
grid = hcat(grid, fill(9, size(grid)[1], 1))
grid = vcat(grid, fill(9, 1, size(grid)[2]))
grid = vcat(fill(9, 1, size(grid)[2]), grid)

centers = []

for c in 2:size(grid)[1]-1
    for r in 2:size(grid)[2]-1
        up = grid[c, r-1]
        down = grid[c, r+1]
        left = grid[c-1, r]
        right = grid[c+1, r]
        center = grid[c, r]
        if center < min(up, down, left, right)
            push!(centers, (c, r))
        end
    end
end


function CountBasin(grid, c, r, mask)
    if grid[c, r] == 9 || mask[c, r] == 1
        return
    end
    mask[c, r] = 1
    CountBasin(grid, c, r-1, mask)
    CountBasin(grid, c, r+1, mask)
    CountBasin(grid, c-1, r, mask)
    CountBasin(grid, c+1, r, mask)
    return sum(mask)
end

sizes = []
for (c, r) in centers
    mask = zeros(Int, size(grid))
    push!(sizes, CountBasin(grid, c, r, mask))
end

println(reduce(*, sort(sizes, rev=true)[begin:3]))

