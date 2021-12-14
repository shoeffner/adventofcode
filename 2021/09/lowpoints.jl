lines = readlines()
grid = transpose(reshape(parse.(Int, convert.(String, vcat(split.(hcat(lines), "")...))), (:, length(lines))))

# padding
grid = hcat(fill(Inf, size(grid)[1], 1), grid)
grid = hcat(grid, fill(Inf, size(grid)[1], 1))
grid = vcat(grid, fill(Inf, 1, size(grid)[2]))
grid = vcat(fill(Inf, 1, size(grid)[2]), grid)

risk = 0

for c in 2:size(grid)[1]-1
    for r in 2:size(grid)[2]-1
        up = grid[c, r-1]
        down = grid[c, r+1]
        left = grid[c-1, r]
        right = grid[c+1, r]
        center = grid[c, r]
        if center < min(up, down, left, right)
            global risk += center + 1
        end
    end
end

println(convert(Int, round(risk)))
