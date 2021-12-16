function readinput()
    coords = []
    folds = []

    mode = 0

    for line in readlines()
        if line == ""
            mode = 1
            continue
        end
        if mode == 0
            push!(coords, parse.(Int, convert.(String, split(line, ","))))
        elseif mode == 1
            push!(folds, convert.(String, split(split(line, " ")[3], "=")))
        end
    end

    coords = transpose(reshape(hcat(coords...), 2, :)) .+ 1
    return coords, folds
end

function makegrid(coords)
    x = maximum(coords[:, 1])
    y = maximum(coords[:, 2])
    grid = zeros(Bool, y, x)
    for (x, y) in eachrow(coords)
        grid[y, x] = true
    end
    return grid
end

function foldgrid(grid, direction, index)
    # println(direction, " ", index)
    if direction == "y"
        bottom = grid[begin:index - 1, :]
        top = grid[end:-1:index + 1, :]
    else
        bottom = grid[:, begin:index - 1]
        top = grid[:, end:-1:index + 1]
    end
    # println("GRID")
    # display(grid)
    # println()
    # println("BOTTOM")
    # display(bottom)
    # println()
    # println("TOP")
    # display(top)
    # println()
    # println()
    # println()
    bottom .| top
end

function main()
    coords, folds = readinput()
    grid = makegrid(coords)

    for f in folds
         grid = foldgrid(grid, f[1], parse(Int, f[2]) + 1)
    end
    display(grid)
    println()
end

main()
